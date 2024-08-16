""" boardgamegeek_client.py - BOARDGAME REVIEWER """
import logging
import xml.etree.ElementTree as ET
import requests

class BoardGameGeekClient:
    """Class for extracting data from BoardGameGeek.com"""
    def __init__(self):
        self.base_url = 'https://www.boardgamegeek.com/xmlapi2/'

    def get_game_info(self, searched_game_name):
        """Method gets formatted game info from BoardGameGeek.com"""
        searched_game_id = self.get_game_id(searched_game_name)
        if searched_game_id:
            searched_game_details = self.get_boardgame_details(searched_game_id)
            return self.format_boardgame_details(searched_game_details)
        return None

    def get_game_id(self, searched_game_name):
        """Method gets game ID from BoardGameGeek.com"""
        url = self.base_url + 'search?query=' + searched_game_name + '&type=boardgame'

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses
        except requests.exceptions.RequestException as e:
            logging.error("HTTP error occurred: %s", str(e))
            return None

        try:
            root = ET.fromstring(response.content) # Parsing XML data
        except ET.ParseError as e:
            logging.error("XML parsing error: %s", str(e))
            return None

        # Search results and return the ID of the first match
        for item in root.findall('.//item'):
            name_element = item.find('name')
            if name_element is not None:
                current_name = name_element.attrib.get('value', '')
                if current_name.lower() == searched_game_name.lower():
                    return item.attrib['id']

        # If no match is found, return the ID of the first result
        first_item = root.find('.//item')
        if first_item is not None:
            first_item_id = first_item.attrib['id']
            return first_item_id

        logging.warning("No matching game found for %s", searched_game_name)
        return None

    def get_boardgame_details(self, game_id):
        """Gets game details from BoardGameGeek.com by game ID"""
        url = self.base_url + 'thing?id=' + game_id + '&stats=1'

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error("HTTP error occurred while fetching game details: %s", str(e))
            return {
                'name': None,
                'description': None,
                'minplayers': None,
                'maxplayers': None,
                'playingtime': None,
                'minage': None,
                'average_rating': None,
                'categories': []
            }

        try:
            # Parsing XML data
            root = ET.fromstring(response.content)
        except ET.ParseError as e:
            logging.error("XML parsing error in game details: %s", {str(e)})
            return {
                'name': None,
                'description': None,
                'minplayers': None,
                'maxplayers': None,
                'playingtime': None,
                'minage': None,
                'average_rating': None,
                'categories': []
            }

        # Create dictionary with game details
        game_details = {
            "name": root.find('.//name[@type="primary"]').attrib.get('value', 'Název nenalezen'),
            "description": root.find('.//description').text or "Popis nenalezen",
            "minplayers": root.find('.//minplayers').attrib.get('value', 'Minimální počet hráčů nenalezen'),
            "maxplayers": root.find('.//maxplayers').attrib.get('value', 'Maximální počet hráčů nenalezen'),
            "playingtime": root.find('.//playingtime').attrib.get('value', 'Herní čas nenalezen') + " minut",
            "minage": root.find('.//minage').attrib.get('value', 'Minimální věk nenalezen'),
            "average_rating": root.find('.//average').attrib.get('value', 'Rating nenalezen'),
            "categories": [link.attrib['value'] for link in root.findall('.//link[@type="boardgamecategory"]')]
        }

        return game_details
    
    def format_boardgame_details(self, game_details):
        """Format game details"""
        if not game_details:
            return {}

        formatted_boardgame_info = {
            "Název hry": game_details["name"] or "Název nenalezen",
            "Popis": game_details["description"] or "Popis nenalezen",
            "Počet hráčů": (game_details["minplayers"] or "Minimální počet hráčů nenalezen")
                + "-" + (game_details["maxplayers"] or "Maximální počet hráčů nenalezen"),
            "Průměrná délka hry": (game_details["playingtime"] or "Herní čas nenalezen"),
            "Minimální věk": (game_details["minage"] or "Minimální věk nenalezen"),
            "Průměrné hodnocení": (game_details["average_rating"] or "Rating nenalezen"),
            "Kategorie": ", ".join(game_details["categories"]) or "Žádné kategorie"
        }

        return formatted_boardgame_info

# Example usage
if __name__ == "__main__":

    bgg_client = BoardGameGeekClient()
    GAME_NAME = "Scythe"
    new_game_details = bgg_client.get_game_info(GAME_NAME)

    if new_game_details:
        print(new_game_details)
    else:
        print("Hra nebyla nalezena.")
