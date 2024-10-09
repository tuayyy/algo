# player_data.py

import time

# Function to record player data
def save_player_data(username, winning_time):
    """
    Save the player data including username and winning time to a text file.
    
    Args:
        username (str): The username of the player.
        winning_time (str): The time when the player won the game.
    """
    with open("player_data.txt", "a") as file:  # Open in append mode to add data
        file.write(f"{username},{winning_time}\n")
    print(f"Player data saved: {username}, {winning_time}")

# Function to display all player records
def display_player_data():
    """
    Display all player records stored in the text file.
    """
    try:
        with open("player_data.txt", "r") as file:
            records = file.readlines()
            print("Player Records:")
            for record in records:
                username, winning_time = record.strip().split(",")
                print(f"Username: {username} | Winning Time: {winning_time}")
    except FileNotFoundError:
        print("No player records found. The file 'player_data.txt' does not exist yet.")

# Testing the save function
if __name__ == "__main__":
    username = input("Enter your username: ")
    # Simulating a win and getting the current time as the winning time
    winning_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # Format: YYYY-MM-DD HH:MM:SS
    
    save_player_data(username, winning_time)
    display_player_data()
