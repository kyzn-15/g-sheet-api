import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from models import Player
import time

class GoogleSheetsClient:
    def __init__(self):
        
        self.SCOPE = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
        
        
        self.creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_path, self.SCOPE)
        self.client = gspread.authorize(self.creds)
        self.SPREADSHEET_NAME = "Tugas Informatika"
        self.SHEET_NAME = "Sheet1"
        self.sheet = None
        
        
        self.connect()
    
    def connect(self):
        """Establish connection to Google Sheets and prepare the sheet"""
        try:
            self.sheet = self.client.open(self.SPREADSHEET_NAME).worksheet(self.SHEET_NAME)
            print(f"Successfully connected to spreadsheet '{self.SPREADSHEET_NAME}' and sheet '{self.SHEET_NAME}'")
            
            
            if not self.sheet.get_all_values():
                self.sheet.append_row(['id', 'name', 'age', 'games_played', 'highest_score', 'current_score'])
                print("Added header row to empty sheet.")
            else:
                
                header = self.sheet.row_values(1)
                expected_header = ['id', 'name', 'age', 'games_played', 'highest_score', 'current_score']
                if header != expected_header:
                    print(f"Warning: Header row {header} does not match expected {expected_header}")
            
            return True
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Error: Spreadsheet '{self.SPREADSHEET_NAME}' not found. Please ensure the name is correct and the service account has access.")
            return False
        except gspread.exceptions.WorksheetNotFound:
            print(f"Error: Worksheet '{self.SHEET_NAME}' not found in spreadsheet '{self.SPREADSHEET_NAME}'.")
            return False
        except Exception as e:
            print(f"An error occurred during Google Sheets setup: {e}")
            return False
    
    def row_to_dict(self, row, header):
        """Convert sheet rows to dictionaries"""
        player_dict = {}
        for i, key in enumerate(header):
            value = row[i]
            if key in ['id', 'age', 'games_played', 'highest_score', 'current_score']:
                try:
                    player_dict[key] = int(value) if value else 0  
                except ValueError:
                    player_dict[key] = value  
            else:
                player_dict[key] = value
        return player_dict
    
    def get_next_id(self):
        """Find the next available ID"""
        try:
            ids = self.sheet.col_values(1)[1:]  
            numeric_ids = [int(id_val) for id_val in ids if id_val.isdigit()]
            return max(numeric_ids) + 1 if numeric_ids else 1
        except Exception as e:
            print(f"Error getting next ID: {e}")
            
            return 1 
    
    def get_all_players(self):
        """Get all players from the sheet"""
        try:
            all_values = self.sheet.get_all_values()
            if len(all_values) <= 1:  
                return []
            header = all_values[0]
            players_dicts = [self.row_to_dict(row, header) for row in all_values[1:]]  
            return [Player.from_dict(player_dict).to_dict() for player_dict in players_dicts]
        except gspread.exceptions.APIError as e:
            print(f"Error fetching players: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred in get_all_players: {e}")
            raise
    
    def get_player_by_id(self, player_id):
        """Get a specific player by ID"""
        try:
            header = self.sheet.row_values(1)
            
            cell = self.sheet.find(str(player_id), in_column=1)
            if cell:
                player_row = self.sheet.row_values(cell.row)
                player_dict = self.row_to_dict(player_row, header)
                return Player.from_dict(player_dict).to_dict()
            return None
        except gspread.exceptions.CellNotFound:
            return None
        except Exception as e:
            print(f"An unexpected error occurred in get_player_by_id: {e}")
            raise
    
    def create_player(self, data):
        """Create a new player record"""
        try:
            
            next_id = self.get_next_id()
            data['id'] = next_id
            player = Player.from_dict(data)
            
            
            new_row = [
                player.id,
                player.name,
                player.age,
                player.games_played,
                player.highest_score,
                player.current_score,
            ]
            self.sheet.append_row(new_row)
            
            
            cell = self.sheet.find(str(next_id), in_column=1)
            if cell:
                header = self.sheet.row_values(1)
                created_player_data = self.sheet.row_values(cell.row)
                player_dict = self.row_to_dict(created_player_data, header)
                return Player.from_dict(player_dict).to_dict()
            else:
                
                return player.to_dict()
        except Exception as e:
            print(f"An unexpected error occurred in create_player: {e}")
            raise
    
    def refresh_connection(self):
        """Refresh the connection to Google Sheets if token expired"""
        try:
            print("Refreshing Google Sheets connection...")
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_path, self.SCOPE)
            self.client = gspread.authorize(self.creds)
            self.sheet = self.client.open(self.SPREADSHEET_NAME).worksheet(self.SHEET_NAME)
            print("Connection refreshed successfully")
            return True
        except Exception as e:
            print(f"Error refreshing connection: {e}")
            return False
            
    def update_player(self, player_id, data):
        """Update an existing player record"""
        try:
            # Try to refresh connection to avoid token expired issues
            self.refresh_connection()
            
            header = self.sheet.row_values(1)
            cell = self.sheet.find(str(player_id), in_column=1)
            if cell:
                row_index = cell.row
                current_row_values = self.sheet.row_values(row_index)
                current_player_dict = self.row_to_dict(current_row_values, header)
                
                print(f"Current data before update: {current_player_dict}")
                
                
                current_player_dict.update(data)
                updated_player = Player.from_dict(current_player_dict)
                
                
                updated_row = [
                    updated_player.id,
                    updated_player.name,
                    updated_player.age,
                    updated_player.games_played,
                    updated_player.highest_score,
                    updated_player.current_score
                ]
                
                self.sheet.update(f'A{row_index}:F{row_index}', [updated_row])
                
                print(f"Updated row: {updated_row}")
                
                time.sleep(1)  
                
                try:
                    updated_values = self.sheet.row_values(row_index)
                    print(f"Values after update: {updated_values}")
                    
                    if len(updated_values) == len(header):
                        updated_dict = self.row_to_dict(updated_values, header)
                        return Player.from_dict(updated_dict).to_dict()
                    else:
                        print("Warning: Retrieved values don't match expected length. Returning object data.")
                        return updated_player.to_dict()
                except Exception as fetch_error:
                    print(f"Error fetching updated data: {fetch_error}. Returning object data.")
                    return updated_player.to_dict()
            
            return None
        except gspread.exceptions.CellNotFound:
            return None
        except gspread.exceptions.APIError as e:
            print(f"Google Sheets API error: {e}")
            if "invalid_grant" in str(e) or "token expired" in str(e).lower():
                print("Token may have expired. Refreshing connection and retrying...")
                if self.refresh_connection():
                    return self.update_player(player_id, data)
            raise
        except Exception as e:
            print(f"An unexpected error occurred in update_player: {e}")
            raise
    
    def delete_player(self, player_id):
        """Delete a player record"""
        try:
            cell = self.sheet.find(str(player_id), in_column=1)
            if cell:
                self.sheet.delete_rows(cell.row)
                print(f"Player {player_id} deleted.")
                return True
            return False
        except gspread.exceptions.CellNotFound:
            return False
        except Exception as e:
            print(f"An unexpected error occurred in delete_player: {e}")
            raise 