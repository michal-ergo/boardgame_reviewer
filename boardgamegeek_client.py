""" boardgamegeek_client.py - BOARDGAME REVIEWER """
import logging
import xml.etree.ElementTree as ET
import sqlite3
import requests

class BoardGameGeekClient:
    """Class for extracting data from BoardGameGeek.com"""
    def __init__(self):
        self.base_url = "https://www.boardgamegeek.com/xmlapi2/"
        self.game_details = {
            "name": "Název nenalezen",
            "description": "Popis nenalezen",
            "minplayers": "Minimální počet hráčů nenalezen",
            "maxplayers": "Maximální počet hráčů nenalezen",
            "playingtime": "Herní čas nenalezen",
            "minage": "Minimální věk nenalezen",
            "average_rating": "Rating nenalezen",
            "categories": []
        }

        self.create_table_if_not_exists()

    def fetch_data(self, url):
        """Fetch data from BoardGameGeek.com and return the response content"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            logging.error("HTTP error occurred: %s", str(e))
            return None

    def get_game_info(self, searched_game_name):
        """Method gets formatted game info from BoardGameGeek.com"""
        searched_game_id = self.get_game_id(searched_game_name)
        if searched_game_id:
            self.get_boardgame_details(searched_game_id)
            self.save_game_to_db(self.game_details)
            return self.format_boardgame_details(self.game_details)

        return None

    def get_game_id(self, searched_game_name):
        """Method gets game ID from BoardGameGeek.com"""
        url = self.base_url + "search?query=" + searched_game_name + "&type=boardgame"
        content = self.fetch_data(url)

        if not content:
            return None

        try:
            root = ET.fromstring(content) # Parsing XML data
        except ET.ParseError as e:
            logging.error("XML parsing error: %s", str(e))
            return None

        # Search results and return the ID of the first match
        for item in root.findall(".//item"):
            name_element = item.find("name")
            if name_element is not None:
                current_name = name_element.attrib.get("value", "")
                if current_name.lower() == searched_game_name.lower():
                    return item.attrib["id"]

        # If no match is found, return the ID of the first result
        first_item = root.find(".//item")
        if first_item is not None:
            return first_item.attrib["id"]

        logging.warning("No matching game found for %s", searched_game_name)
        return None

    def get_boardgame_details(self, game_id):
        """Gets game details from BoardGameGeek.com by game ID"""
        url = self.base_url + "thing?id=" + game_id + "&stats=1"
        content = self.fetch_data(url)
        if content:
            try:
                root = ET.fromstring(content)
            except ET.ParseError as e:
                logging.error("XML parsing error: %s", str(e))
                return

            self.game_details["name"] = root.find('.//name[@type="primary"]').attrib.get(
                'value', 'Název nenalezen')
            self.game_details["description"] = root.find('.//description').text or "Popis nenalezen"
            self.game_details["minplayers"] = root.find('.//minplayers').attrib.get(
                                                'value', 'Minimální počet hráčů nenalezen')
            self.game_details["maxplayers"] = root.find('.//maxplayers').attrib.get(
                                                'value', 'Maximální počet hráčů nenalezen')
            self.game_details["playingtime"] = root.find('.//playingtime').attrib.get(
                                                'value', 'Herní čas nenalezen')
            self.game_details["minage"] = root.find('.//minage').attrib.get(
                                                'value', 'Minimální věk nenalezen')
            self.game_details["average_rating"] = root.find('.//average').attrib.get(
                                                'value', 'Rating nenalezen')
            self.game_details["categories"] = [link.attrib['value'] for link in root.findall(
                                                './/link[@type="boardgamecategory"]')]

    def format_boardgame_details(self, game_details):
        """Format game details"""
        formatted_boardgame_info = {
            "Název hry": game_details["name"] or "Název nenalezen",
            "Popis": game_details["description"] or "Popis nenalezen",
            "Počet hráčů": (game_details["minplayers"] or "Minimální počet hráčů nenalezen")
                + "-" + (game_details["maxplayers"] or "Maximální počet hráčů nenalezen"),
            "Průměrná délka hry": (game_details["playingtime"] + " minut" or "Herní čas nenalezen"),
            "Minimální věk": (game_details["minage"] or "Minimální věk nenalezen"),
            "Průměrné hodnocení": (game_details["average_rating"] or "Rating nenalezen"),
            "Kategorie": ", ".join(game_details["categories"]) or "Žádné kategorie"
        }

        return formatted_boardgame_info

    def create_table_if_not_exists(self):
        """Create table if it doesn't exist"""
        conn = sqlite3.connect('searched_games.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS boardgames (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        playingtime INTEGER,
                        maxplayers INTEGER,
                        average_rating FLOAT
                    )''')
        conn.commit()
        conn.close()

    def save_game_to_db(self, boardgame_output):
        """Save game details to SQLite database"""
        if boardgame_output:
            conn = sqlite3.connect('searched_games.db')
            c = conn.cursor()

            c.execute("SELECT 1 FROM boardgames WHERE name = :name", {
                "name": boardgame_output["name"]})
            result = c.fetchone()

            if result:
                pass
            else:
                c.execute("INSERT INTO boardgames(name, description, playingtime, maxplayers, average_rating) VALUES (:name, :description, :playingtime, :maxplayers, :average_rating)",
                          {"name": boardgame_output["name"],
                           "description": boardgame_output["description"],
                           "playingtime": boardgame_output["playingtime"],
                           "maxplayers": boardgame_output["maxplayers"], 
                           "average_rating": boardgame_output["average_rating"]})
            conn.commit()
            conn.close()

# Example usage
if __name__ == "__main__":

    bgg_client = BoardGameGeekClient()
    GAME_NAME = "Expedice"
    new_game_details = bgg_client.get_game_info(GAME_NAME)

    if new_game_details:
        print(new_game_details)
    else:
        print("Hra nebyla nalezena.")
