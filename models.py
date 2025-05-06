class Player:
    """
    Player model representing a player in the game.
    This is used for type hints and data validation.
    """
    
    def __init__(self, id=None, name=None, age=None, games_played=0, highest_score=0, current_score=0):
        self.id = id
        self.name = name
        self.age = age
        self.games_played = games_played
        self.highest_score = highest_score
        self.current_score = current_score
    
    @classmethod
    def from_dict(cls, data):
        """Create a Player instance from a dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            age=data.get('age'),
            games_played=data.get('games_played', 0),
            highest_score=data.get('highest_score', 0),
            current_score=data.get('current_score', 0)
        )
    
    def to_dict(self):
        """Convert a Player instance to a dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'games_played': self.games_played,
            'highest_score': self.highest_score,
            'current_score': self.current_score
        }
    
    def __repr__(self):
        return f"Player(id={self.id}, name={self.name}, age={self.age})" 