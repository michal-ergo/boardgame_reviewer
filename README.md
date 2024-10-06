# Boardgame Reviewer

Boardgame Reviewer is a Python application that provides personalized board game reviews in czech language using data from BoardGameGeek.com and user preferences. The application features a Streamlit-based frontend for user interaction.

## Installation

To install the necessary dependencies, use the package manager pip.

```bash
pip install -r requirements.txt
```

You will also need to set up a .env file with your OpenAI API key.

```bash
OPENAI_API_KEY = "..."
```

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

## Future Work

Possible future features include:

### Iproved SQL functionalities
Current version stores some fetched info about boardgames into a SQL database. Future goal is to store not only basic info, but also all generated reviews
into an SQL database for easy access, searching, and analysis.

### Unit Testing
Adding comprehensive unit tests to ensure the reliability and accuracy of the application's components.

### Display Additional Results
If the exact board game name provided by the user is not found, the application will offer alternative results to choose from, improving user experience and ensuring more accurate reviews.

## License

[MIT](https://choosealicense.com/licenses/mit/)