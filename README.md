# Google Sheets REST API

This is a REST API application that syncs data with Google Sheets. It provides CRUD operations for managing player data.

## Project Structure

```
/
├── run.py              # Main application server
├── client.py           # Google Sheets client for data operations
├── models.py           # Data models for the application
├── api_client.py       # Example API client for interacting with the REST API
├── credentials.json    # Google API credentials (keep this secure!)
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
└── README.md           # This documentation
```

## Features

* REST API for managing player data
* Google Sheets integration for data storage
* Full CRUD operations (Create, Read, Update, Delete)
* API client for easy integration with other applications
* Proper error handling
* Clean code structure with separation of concerns

## Requirements

* Python 3.6+
* Required dependencies listed in requirements.txt

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv env`
3. Activate the virtual environment:

   * Windows: `env\Scripts\activate`
   * Linux/Mac: `source env/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up Google Sheets API credentials:

   * Create a project in the Google Developer Console
   * Enable the Google Sheets API
   * Create service account credentials
   * Download the `credentials.json` file and place it in the project root
6. Configure the `.env` file with your spreadsheet information
7. Run the application: `python run.py`

## API Endpoints

* `GET /players` - Get all players
* `GET /players/<id>` - Get player by ID
* `POST /players` - Create a new player
* `PATCH /players/<id>` - Update a player
* `DELETE /players/<id>` - Delete a player

## Usage via Curl

Below are examples of how to interact with the API using `curl` commands. Make sure your Flask app is running (default at `http://127.0.0.1:5000`).

1. **Run your Flask app**

   ```bash
   # From your project directory
   export FLASK_APP=app.py
   flask run --host=127.0.0.1 --port=5000
   ```

2. **Fetch all players**

   ```bash
   curl -X GET http://127.0.0.1:5000/players
   ```

3. **Fetch a single player by ID (e.g. ID = 2)**

   ```bash
   curl -X GET http://127.0.0.1:5000/players/2
   ```

4. **Create a new player**

   ```bash
   curl -X POST http://127.0.0.1:5000/players \
        -H "Content-Type: application/json" \
        -d '{
              "name": "Lewis",
              "age": 25,
              "games_played": 10,
              "highest_score": 200,
              "current_score": 50
            }'
   ```

5. **Update an existing player** (e.g. change age and current\_score for ID = 1)

   ```bash
   curl -X PATCH http://127.0.0.1:5000/players/1 \
        -H "Content-Type: application/json" \
        -d '{
              "age": 190,
              "current_score": 70
            }'
   ```

6. **Delete a player by ID** (e.g. ID = 1)

   ```bash
   curl -X DELETE http://127.0.0.1:5000/players/1
   ```

## API Client Usage

```python
# Import the API client
from api_client import get_all_players, get_player_by_id, create_player, update_player, delete_player

# Get all players
all_players = get_all_players()

# Create a player
new_player = create_player("John Doe", 25, 10, 1200, 800)

# Get a specific player
player = get_player_by_id(1)

# Update a player
updated_player = update_player(1, current_score=950)

# Delete a player
success = delete_player(1)
```

## Demo

You can run the demo in `api_client.py` to see the API in action:

```bash
python api_client.py
```
