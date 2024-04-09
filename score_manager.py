import json
from datetime import datetime


class ScoreManager:
    """A manager for handling high scores in a typing speed test application.

    Attributes:
        filepath (str): The path to the file where high scores are stored.
        high_scores (list of dict): A list of high score records.
    """

    def __init__(self, filepath='high_scores.json'):
        """Initialize the ScoreManager with a file path for high scores."""
        self.filepath = filepath
        self.high_scores = self.load_scores()

    def load_scores(self):
        """Load high scores from a JSON file.

        Returns:
            A list of high score records. If the file doesn't exist or an error
            occurs, it returns an empty list.
        """
        try:
            with open(self.filepath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            # If the file does not exist, it's not necessarily an error, so we can start with an empty list
            return []
        except json.JSONDecodeError:
            # File is corrupt or not valid JSON
            print(f"Corrupt high score file! Starting fresh.")
            return []
        except Exception as e:
            # Handle other exceptions such as file permission issues
            print(f"Failed to load high scores due to an unexpected error: {e}")
            return []

    def save_scores(self):
        """Save the high scores to a JSON file.

        This method writes the list of high scores to a file in JSON format.
        """
        try:
            with open(self.filepath, 'w') as file:
                json.dump(self.high_scores, file, indent=4)
        except Exception as e:
            print(f"Failed to save high scores due to an unexpected error: {e}")

    def add_score(self, name, score, accuracy):
        """Add a new high score record and save the updated list.

        The high score list is sorted in descending order and truncated to
        maintain only the top 10 scores.

        Args:
            name (str): The name of the player.
            score (float): The WPM score of the player.
            accuracy (float): The typing accuracy percentage of the player.
        """
        # Create a new score record
        new_score = {
            "name": name,
            "score": score,
            "accuracy": accuracy,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        self.high_scores.append(new_score)
        # Sort and keep top 10 scores
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        self.high_scores = self.high_scores[:10]
        self.save_scores()  # Persist the changes

    def get_top_scores(self):
        """Get the list of high scores.

        Returns:
            A list of high score records.
        """
        return self.high_scores
