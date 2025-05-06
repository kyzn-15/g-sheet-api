import requests

BASE_URL = "http://127.0.0.1:5000/players"

def get_all_players():
    """Retrieve all players from the API"""
    response = requests.get(BASE_URL)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        players = response.json()
        print(f"Retrieved {len(players)} players.")
        for player in players:
            print(f"ID: {player['id']}, Name: {player['name']}, Age: {player['age']}, "
                  f"Games: {player['games_played']}, Highest Score: {player['highest_score']}, "
                  f"Current Score: {player['current_score']}")
        return players
    else:
        print(f"Error: {response.json()}")
        return None

def get_player_by_id(player_id):
    """Retrieve a specific player by ID"""
    response = requests.get(f"{BASE_URL}/{player_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        player = response.json()
        print(f"Player Details:")
        print(f"ID: {player['id']}")
        print(f"Name: {player['name']}")
        print(f"Age: {player['age']}")
        print(f"Games Played: {player['games_played']}")
        print(f"Highest Score: {player['highest_score']}")
        print(f"Current Score: {player['current_score']}")
        return player
    else:
        print(f"Error: {response.json()}")
        return None

def create_player(name, age, games_played=0, highest_score=0, current_score=0):
    """Create a new player"""
    payload = {
        "name": name,
        "age": age,
        "games_played": games_played,
        "highest_score": highest_score,
        "current_score": current_score
    }
    
    response = requests.post(BASE_URL, json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print(f"Player created successfully!")
        return response.json()
    else:
        print(f"Error creating player: {response.json()}")
        return None

def update_player(player_id, **updates):
    """Update a player's information
    
    Args:
        player_id: The ID of the player to update
        updates: Keyword arguments for fields to update (name, age, games_played, etc.)
    """
    if not updates:
        print("No updates provided")
        return None
    
    # Make sure we're only updating valid fields
    valid_fields = ['name', 'age', 'games_played', 'highest_score', 'current_score']
    payload = {k: v for k, v in updates.items() if k in valid_fields}
    
    if not payload:
        print("No valid fields to update")
        return None
    
    response = requests.patch(f"{BASE_URL}/{player_id}", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Player {player_id} updated successfully!")
        return response.json()
    else:
        print(f"Error updating player: {response.json()}")
        return None

def delete_player(player_id):
    """Delete a player by ID"""
    response = requests.delete(f"{BASE_URL}/{player_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Player {player_id} deleted successfully!")
        return True
    else:
        print(f"Error deleting player: {response.json()}")
        return False

def demo():
    """Demonstrate the API client functionality"""
    print("\n=== Getting all players ===")
    get_all_players()
    
    print("\n=== Creating a new player ===")
    new_player = create_player("John Doe", 25, 10, 1200, 800)
    
    if new_player:
        player_id = new_player['id']
        
        print(f"\n=== Getting player {player_id} ===")
        get_player_by_id(player_id)
        
        print(f"\n=== Updating player {player_id} ===")
        update_player(player_id, current_score=950, games_played=11)
        
        print(f"\n=== Getting updated player {player_id} ===")
        get_player_by_id(player_id)
        
        print(f"\n=== Deleting player {player_id} ===")
        delete_player(player_id)
        
        print("\n=== Verifying deletion ===")
        get_player_by_id(player_id)
    
    print("\n=== Demo complete ===")

if __name__ == "__main__":
    demo() 