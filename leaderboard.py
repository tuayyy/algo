import flet as ft

# Function to read and parse the leaderboard from a text file
def read_leaderboard(file_path):
    leaderboard = []
    with open(file_path, 'r') as file:
        for line in file:
            username, time_str = line.strip().split(',')
            time_seconds = float(time_str.split()[0])  # Convert the time to float
            leaderboard.append((username.strip(), time_seconds))
    # Sort the leaderboard by time (fastest first)
    leaderboard.sort(key=lambda x: x[1])
    return leaderboard

def main(page: ft.Page):
    # Set the page title and theme
    page.title = "Leaderboard"
    page.theme_mode = ft.ThemeMode.LIGHT  # or DARK for dark mode
    
    # Set page background color
    page.bgcolor = ft.colors.BLUE_GREY_50

    # Read the leaderboard data from the text file
    leaderboard_data = read_leaderboard("player_data.txt")
    
    # Create a list to hold leaderboard items
    leaderboard_items = []
    for username, time in leaderboard_data:
        leaderboard_items.append(
            ft.Row(
                [
                    ft.Text(username, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700),
                    ft.Spacer(),
                    ft.Text(f"{time:.2f} seconds", size=20, weight=ft.FontWeight.NORMAL, color=ft.colors.BLUE_800),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                padding=ft.padding.symmetric(vertical=5),
                bgcolor=ft.colors.WHITE,
                border_radius=5,
                width=400,
                height=50,
                margin=ft.margin.symmetric(vertical=2),
            )
        )

    # Add the leaderboard header and items to the page
    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Leaderboard", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(vertical=10),
                ),
                ft.Container(
                    content=ft.Column(
                        controls=leaderboard_items
                    ),
                    bgcolor=ft.colors.WHITE,
                    border_radius=10,
                    padding=ft.padding.all(10),
                    width=420,
                    alignment=ft.MainAxisAlignment.START,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    # Run the Flet app
    ft.app(target=main)
