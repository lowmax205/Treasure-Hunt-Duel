import tkinter as tk
from ui_functions import setup_ui
import random as rd


class TreasureHuntGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Treasure Hunt Duel")
        self.root.geometry("400x800")
        self.grid_size = 3
        self.grid_color = "lightblue"  # Initialize grid_color
        self.treasure_location = (
            rd.randint(0, self.grid_size - 1),
            rd.randint(0, self.grid_size - 1),
        )
        self.player1_choice = None
        self.player2_choice = None
        self.current_player = 1
        self.mode = "Classic"
        self.player1_clicked = False
        self.player2_clicked = False

        setup_ui(self)

    def run(self):
        self.root.mainloop()


# Run the game
if __name__ == "__main__":
    game = TreasureHuntGame()
    game.run()
