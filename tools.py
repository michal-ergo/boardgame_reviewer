""" tools.py - BOARDGAME REVIEWER """

assistant_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_boardgame_info",
            "description": "Retrieve information about a board game from BoardGameGeek.",
            "parameters": {
                "type": "object",
                "properties": {
                    "boardgame_name": {
                        "type": "string",
                        "description": "Name of the board game to retrieve information about."
                    },
                    "boardgamegeek_data": {
                        "type": "object",
                        "description": "Additional data from BoardGameGeek required for the request."
                    }
                },
                "required": ["boardgame_name", "boardgamegeek_data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "make_review",
            "description": "Write a personalized review for a board game using given data",
            "parameters": {
                "type": "object",
                "properties": {
                    "boardgame_review": {
                        "type": "string",
                        "description": "Review of a game using data obtained by get_boardgame_info from boardgamegeek.com, including its name, description, rating, categories, etc. Use BGG rating and compare the game's categories and user's submitted categories to predict whether the user will like the game."
                    }
                },
                "required": ["boardgame_review"]
            }
        }
    }
]