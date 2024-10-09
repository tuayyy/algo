import flet as ft
from solitaire import Solitaire
from dev import save_winner_data

def main(page: ft.Page):
    # Enable keyboard event listener
    page.window_event_listener = True
    page.on_keyboard_event = lambda e: print(f"Key pressed: {e.key}")

    # Create an input field for the username and a button to start the game
    username_input = ft.TextField(label="Enter your username", autofocus=True)
    
    def start_game(e):
        # Get the player's username from the input field
        player_username = username_input.value.strip()
        if player_username:
            # Create the Solitaire game with the player's username and pass the page reference
            solitaire = Solitaire(username=player_username, page=page)
            
            # Clear the page and add the Solitaire game
            page.clean()
            page.add(solitaire)
        else:
            page.add(ft.Text("Please enter a username before starting the game.", color="red"))

    # Display the input field and the button
    page.add(username_input, ft.ElevatedButton("Start Game", on_click=start_game))

ft.app(target=main, assets_dir="assets")
