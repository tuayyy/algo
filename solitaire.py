SOLITAIRE_WIDTH = 1000
SOLITAIRE_HEIGHT = 500

import random
import time  # To track time
import flet as ft
from card import Card
from slot import Slot
from dev import save_winner_data  # Import function to save winner data

class Suite:
    def __init__(self, suite_name, suite_color):
        self.name = suite_name
        self.color = suite_color

class Rank:
    def __init__(self, card_name, card_value):
        self.name = card_name
        self.value = card_value

class Solitaire(ft.Stack):
    def __init__(self, username=None, page=None):
        super().__init__()
        self.controls = []
        self.width = SOLITAIRE_WIDTH
        self.height = SOLITAIRE_HEIGHT
        self.username = username  # Store player's username
        self.start_time = time.time()  # Track game start time
        self.page = page  # Store a reference to the page object

        # Register the keyboard event handler with the page
        if self.page:
            self.page.on_keyboard_event = self.keyboard_event
            print("Keyboard event listener registered.")  # Debugging line

        # Create and position the button
        self.create_button()

    def create_button(self):
        # Create a button and set its properties
        button = ft.ElevatedButton(
            text="Finish Game",
            on_click=self.finish_game,  # Set the action for the button click
            width=150,
            height=50,
        )

        # Add the button to the bottom corner
        self.controls.append(
            ft.Row(
                [button],
                alignment=ft.MainAxisAlignment.END,
                spacing=10,
                expand=True,
            )
        )

    def finish_game(self, e):
        """Function to finish the game when the button is clicked."""
        print("Finish Game button clicked!")
        self.winning_sequence()  # Call the winning sequence to end the game

    def did_mount(self):
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()

    def create_card_deck(self):
        suites = [
            Suite("hearts", "RED"),
            Suite("diamonds", "RED"),
            Suite("clubs", "BLACK"),
            Suite("spades", "BLACK"),
        ]
        ranks = [
            Rank("Ace", 1),
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("Jack", 11),
            Rank("Queen", 12),
            Rank("King", 13),
        ]

        self.cards = []

        for suite in suites:
            for rank in ranks:
                self.cards.append(Card(solitaire=self, suite=suite, rank=rank))

    def create_slots(self):
        self.stock = Slot(solitaire=self, top=0, left=0, border=ft.border.all(1))
        self.waste = Slot(solitaire=self, top=0, left=100, border=None)

        self.foundations = []
        x = 300
        for i in range(4):
            self.foundations.append(
                Slot(solitaire=self, top=0, left=x, border=ft.border.all(1, "outline"))
            )
            x += 100

        self.tableau = []
        x = 0
        for i in range(7):
            self.tableau.append(Slot(solitaire=self, top=150, left=x, border=None))
            x += 100

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundations)
        self.controls.extend(self.tableau)
        self.update()

    def deal_cards(self):
        random.shuffle(self.cards)
        self.controls.extend(self.cards)

        # deal to tableau
        first_slot = 0
        remaining_cards = self.cards

        while first_slot < len(self.tableau):
            for slot in self.tableau[first_slot:]:
                top_card = remaining_cards[0]
                top_card.place(slot)
                remaining_cards.remove(top_card)
            first_slot += 1

        # place remaining cards to stock pile
        for card in remaining_cards:
            card.place(self.stock)
            print(f"Card in stock: {card.rank.name} {card.suite.name}")

        self.update()

        for slot in self.tableau:
            slot.get_top_card().turn_face_up()

        self.update()

    def check_foundations_rules(self, card, slot):
        top_card = slot.get_top_card()
        if top_card is not None:
            return (
                card.suite.name == top_card.suite.name
                and card.rank.value - top_card.rank.value == 1
            )
        else:
            return card.rank.name == "Ace"

    def check_tableau_rules(self, card, slot):
        top_card = slot.get_top_card()
        if top_card is not None:
            return (
                card.suite.color != top_card.suite.color
                and top_card.rank.value - card.rank.value == 1
                and top_card.face_up
            )
        else:
            return card.rank.name == "King"

    def restart_stock(self):
        while len(self.waste.pile) > 0:
            card = self.waste.get_top_card()
            card.turn_face_down()
            card.move_on_top()
            card.place(self.stock)

    def check_win(self):
        cards_num = 0
        for slot in self.foundations:
            cards_num += len(slot.pile)
        return cards_num == 52  # Return True if all cards are in foundations

    def winning_sequence(self):
        # Calculate winning time
        winning_time = time.time() - self.start_time

        # Save winner data
        save_winner_data(self.username, winning_time)
        print("Winner Sequence Runned")

        # Animate winning cards
        for slot in self.foundations:
            for card in slot.pile:
                card.animate_position = 2000  # Duration of the animation
                card.move_on_top()             # Bring the card to the top of the stack
                card.top = random.randint(0, SOLITAIRE_HEIGHT)  # Randomize vertical position
                card.left = random.randint(0, SOLITAIRE_WIDTH)  # Randomize horizontal position
                self.update()  # Refresh the UI to reflect the changes
        
        # Display winning message
        self.controls.append(
            ft.AlertDialog(title=ft.Text(f"Congratulations {self.username}! You won in {winning_time:.2f} seconds!"), open=True)
        )

    def keyboard_event(self, e):
        print(f"Key pressed: {e.key}")  # Print the key pressed for debugging
        if e.key == "w":  # Detect if "w" key is pressed
            print("Hidden key 'w' pressed, you win the game!")
            self.winning_sequence()  # Call the winning sequence
