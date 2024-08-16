# Boardgame Reviewer

Boardgame Reviewer is a Python application that provides personalized board game reviews in czech language using data from BoardGameGeek.com and user preferences. The application features a Streamlit-based frontend for user interaction.

## Installation

To install the necessary dependencies, use the package manager pip.

```bash
pip install -r requirements.txt

pip install foobar
```

You will also need to set up a .env file with your OpenAI API key.

## Usage

### Run the Application:

Start the Streamlit app using the following command:

```bash
streamlit run main.py
```

### Interact with the App:

Enter the name of the board game you are interested in.

Select your favorite categories from the provided list.

The app will generate a personalized review of the game based on your input and the game's data from BoardGameGeek.com.


```python
import foobar

### returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Project Structure

### main.py
Contains the main logic for running the Streamlit frontend and handling user interactions.

### boardgamegeek_client.py
A client for fetching board game data from BoardGameGeek.com.

### assistant_manager.py
Manages the interaction with OpenAI's API, including sending prompts and receiving responses.

### tools.py
Defines the tools used by the OpenAI assistant to retrieve game information and generate reviews.

### requirements.txt
Lists all Python dependencies needed for the project.

## Planned Features

Possible future features include:

### SQL Database for Reviews
Implementing an SQL database to store all generated reviews, allowing for easy access, searching, and analysis of past reviews.

### Unit Testing
Adding comprehensive unit tests to ensure the reliability and accuracy of the application's components.

### Display Additional Results
If the exact board game name provided by the user is not found, the application will offer alternative results to choose from, improving user experience and ensuring more accurate reviews.

## License

[MIT](https://choosealicense.com/licenses/mit/)