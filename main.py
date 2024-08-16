""" main.py - BOARDGAME REVIEWER with StreamLit frontend """
import logging
import openai
import streamlit as st
from dotenv import load_dotenv
from tools import assistant_tools
from assistant_manager import AssistantManager

def read_instructions(file_path):
    """Read AI assistant instructions from file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error("File not found: %s. Assistant instructions not available.", file_path)
        raise

def main():
    """Main function."""
    load_dotenv()
    logging.basicConfig(filename='app.log')

    client = openai.OpenAI()
    model = 'gpt-4o-mini'

    st.title(":game_die: Boardgame Reviewer :game_die:")
    st.write("Jsem tu, abych vám poskytl recenzi na vámi hledanou deskovou hru. \
                Na základě vašich oblíbených kategorií a hodnocení hráčů z celého světa zkusím odhadnout, \
                zda by se vám hra mohla líbit.")

    # Keeping track of selected categories
    if "selected_categories" not in st.session_state:
        st.session_state.selected_categories = []

    with st.form(key="user_input_form"):
        boardgame = st.text_input("Jaká desková hra vás zajímá?",
                                  placeholder="Napište název hry (např. Mars: Teraformace)")

        # Předpřipravené kategorie
        categories = ["Abstraktní strategie", "Blafování", "Bojové hry", "Budování měst",
                      "Budování teritoria", "Civilizace", "Dobrodružné hry", "Ekonomické hry",
                      "Fantasy", "Gamebooky", "Historie", "Horor", "Hry s miniaturami",
                      "Hry s kostkami", "Humor", "Karetní hry", "Mytologie", "Párty hry",
                      "Politické hry", "Průzkum", "Sci-Fi", "Vzdělávací hry", "Zvířata"]
        selected_categories = st.multiselect(
            "Vyberte své oblíbené kategorie:",
            categories,
            default=st.session_state.selected_categories,
            placeholder="Vyberte kategorie"
        )

        submit_button = st.form_submit_button(label="Hledat")

        if submit_button:

            if "assistant" not in st.session_state:
                assistant = client.beta.assistants.create(name="BoardGameReviewer",
                    model=model,
                    instructions=read_instructions("assistant_instructions.txt"),
                    tools=assistant_tools)
                st.session_state["assistant"] = assistant

            if "thread" not in st.session_state:
                thread = client.beta.threads.create()
                st.session_state["thread"] = thread

            manager = AssistantManager(
                client, st.session_state["assistant"], st.session_state["thread"])

            manager.add_message_to_thread(
                role="user", content=f"Napiš recenzi o deskové hře {boardgame}.\
                Mé oblíbené kategorie her jsou: {', '.join(selected_categories)}.")
            manager.run_assistant()
            manager.wait_for_run_to_complete()

            st.write(manager.get_review())

if __name__ == "__main__":
    main()
