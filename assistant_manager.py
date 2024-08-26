""" assistant_manager.py - OPENAI ASSISTANT MANAGER """

import logging
import json
from boardgamegeek_client import BoardGameGeekClient

class AssistantManager:
    """AssistantManager - OPENAI ASSISTANT MANAGER"""
    def __init__(self, client, assistant, thread):
        self.client = client
        self.assistant = assistant
        self.thread = thread
        self.run = None
        self.review = None
        self.bgg_client = BoardGameGeekClient()

    def add_message_to_thread(self, role, content):
        """Add message to thread if run is not active"""
        if not self.is_run_active():
            self.client.beta.threads.messages.create(
                self.thread.id, content=content, role=role
            )
        else:
            logging.error("Cannot add message to thread while a run is active.")

    def is_run_active(self):
        """Check if run is active"""
        if self.run is not None:
            run_status = self.check_run()
            if run_status.status not in ['completed', 'failed']:
                return True
        return False

    def run_assistant(self):
        """Run assistant if run is not active"""
        if not self.is_run_active():
            self.run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id, assistant_id=self.assistant.id
            )
        else:
            logging.error("Cannot start a new run while another is active.")

    def check_run(self):
        """Check run status"""
        run_status = self.client.beta.threads.runs.retrieve(
            run_id=self.run.id, thread_id=self.thread.id
        )
        return run_status

    def wait_for_run_to_complete(self):
        """Wait for run to complete and get latest response"""
        while True:
            run = self.check_run()

            if run.status == "completed":
                self.get_latest_response()
                break
            if run.status == "requires_action":
                tools_output = self.prepare_tool_outputs(
                    run.required_action.submit_tool_outputs.model_dump())
                if tools_output:
                    self.client.beta.threads.runs.submit_tool_outputs(
                        run_id=self.run.id,
                        thread_id=self.thread.id,
                        tool_outputs=tools_output
                    )
                else:
                    logging.error("Error - tool outputs not found.")
            elif run.status == "failed":
                logging.error("Run failed.")
                break

    def get_review(self):
        """Get final review"""
        return self.review

    def get_latest_response(self):
        """Get the latest response from the thread"""
        messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        last_message = messages.data[0].content[0].text.value
        self.review = last_message

    def get_boardgame_info(self, boardgame_name):
        """Get boardgame info from BGG using BoardGameGeekClient"""
        game_info = self.bgg_client.get_game_info(boardgame_name)
        return game_info

    def prepare_tool_outputs(self, tool_calls):
        """Prepare ChatGPT tool outputs"""
        tools_outputs = []

        if "tool_calls" in tool_calls:
            for call in tool_calls["tool_calls"]:
                if call["function"]["name"] == "get_boardgame_info":
                    boardgame_load = json.loads(call["function"]["arguments"])
                    boardgame = boardgame_load["boardgame_name"]
                    boardgame_output = self.get_boardgame_info(boardgame)

                    tools_outputs.append({
                        "tool_call_id": call["id"], "output": json.dumps(boardgame_output)})

                elif call["function"]["name"] == "make_review":
                    review_output = json.loads(call["function"]["arguments"])["boardgame_review"]
                    tools_outputs.append({"tool_call_id": call["id"], "output": review_output})

            return tools_outputs

        return None
