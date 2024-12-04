import tkinter as tk
from ui_functions import setup_ui
import random as rd
from PIL import Image, ImageTk

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
        self.root.geometry("400x700")
        self.root.iconbitmap(icon_path)

        # Load and resize the background image
        bg_image_path = resource_path("assets/bg_game.png")
        self.bg_image_original = Image.open(bg_image_path)
        self.bg_image = self.bg_image_original.resize((400, 700), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Bind the resize event to a function with a delay
        self.resize_id = None
        self.root.bind("<Configure>", self.on_resize)

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
        self.bg_label.lower()

    def on_resize(self, event):
        if self.resize_id is not None:
            self.root.after_cancel(self.resize_id)
        self.resize_id = self.root.after(0, self.resize_bg_image, event)

    def resize_bg_image(self, event):
        # Get the new dimensions of the window
        width = event.width
        height = event.height

        # Resize the background image
        self.bg_image = self.bg_image_original.resize((width, height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Update the background label
        self.bg_label.config(image=self.bg_photo)
        self.bg_label.image = self.bg_photo

    def run(self):
        self.root.mainloop()


# Run the game
if __name__ == "__main__":
    game = TreasureHuntGame()
    game.run()
