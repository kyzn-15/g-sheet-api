from flask import Flask, request, jsonify
import os
from client import GoogleSheetsClient

app = Flask(__name__)

gs_client = GoogleSheetsClient()

@app.route("/players", methods=["GET"])
def get_players():
    try:
        players = gs_client.get_all_players()
        return jsonify(players), 200
    except Exception as e:
        print(f"Error fetching players: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route("/players/<int:player_id>", methods=["GET"])
def get_player(player_id):
    try:
        player = gs_client.get_player_by_id(player_id)
        if player:
            return jsonify(player)
        return jsonify({"status": "not found"}), 404
    except Exception as e:
        print(f"Error fetching player {player_id}: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route("/players", methods=["POST"])
def create_player():
    data = request.json
    if not data or 'name' not in data or 'age' not in data:
         return jsonify({"error": "Missing required fields 'name' and 'age'"}), 400

    try:
        created_player = gs_client.create_player(data)
        return jsonify(created_player), 201
    except Exception as e:
        print(f"Error creating player: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/players/<int:player_id>', methods=['PATCH'])
def update_player(player_id):
    data = request.json
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    try:
        
        print(f"Updating player {player_id} with data: {data}")
        
        
        updated_player = gs_client.update_player(player_id, data)
        
        if updated_player:
            verified_player = gs_client.get_player_by_id(player_id)
            if verified_player:
                print(f"Player {player_id} updated successfully. New data: {verified_player}")
                return jsonify(verified_player)
            else:
                print(f"Warning: Updated player successfully but could not verify new data. Returning update result.")
                return jsonify(updated_player)
        
        return jsonify({"error": "Player not found"}), 404
    except Exception as e:
        print(f"Error updating player {player_id}: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route("/players/<int:player_id>", methods=["DELETE"])
def delete_player(player_id):
    try:
        delete_status = gs_client.delete_player(player_id)
        if delete_status:
            return jsonify({"message": "Player deleted"}), 200
        return jsonify({"error": "Player not found"}), 404
    except Exception as e:
        print(f"Error deleting player {player_id}: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='127.0.0.1', port=port)