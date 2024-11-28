import tkinter as tk
from ui_functions import setup_ui
import random as rd

import sys
import os


def resource_path(relative_path):
    # Get the absolute path to resources
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


icon_path = resource_path("assets/TreasureHunt.ico")


class TreasureHuntGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Treasure Hunt Duel")
        self.root.geometry("400x800")
        self.root.iconbitmap(icon_path)
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
