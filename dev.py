import os

# File path to store user data
USER_DATA_FILE = os.path.join(os.path.dirname(__file__), "player_data.txt")

def get_stored_username():
    """This function returns the stored username if available, otherwise returns None."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            data = file.readline().strip()
            return data if data else None
    return None

def save_winner_data(username, winning_time):
    """Save the winner's data to a text file."""
    try:
        print(f"Current working directory: {os.getcwd()}")  # Print current directory
        with open(USER_DATA_FILE, "a") as file:
            file.write(f"{username},{winning_time:.2f} seconds\n")
    except Exception as e:
        print(f"Failed to save winner data: {e}")
