import tkinter as tk
from tkinter import messagebox
import random as rd
from game_logic import TreasureHuntGameLogic
from PIL import Image, ImageTk
import sys
import os

# Constants
LARGE_FONT = ("Helvetica", 16, "bold")
MEDIUM_FONT = ("Helvetica", 12)
SMALL_FONT = ("Helvetica", 10)
COLOR_PLAYER1 = "blue"
COLOR_PLAYER2 = "red"


def show_instructions(self):
    instructions = (
        "Welcome to Treasure Hunt Duel!\n\n"
        "**Description:**\n"
        "Two players search for treasure hidden in a grid. Each player selects a grid cell simultaneously.\n"
        "- If both choose the same cell, they split the treasure equally.\n"
        "- If they choose different cells, the player closer to the treasure gets a larger share.\n\n"
        "**Rules:**\n"
        "1. The grid size varies by mode (Classic: 3x3, Advanced: 5x5).\n"
        "2. Players cannot see each other's choices until after selecting.\n"
        "3. Payoff distribution:\n"
        "   - Same cell: 50/50 split.\n"
        "   - Different cells: Closer player gets 75%, farther player gets 25%.\n\n"
        "**How to Play:**\n"
        "1. Click on a grid cell to select it.\n"
        "2. Click 'Play' to reveal the treasure location and results.\n"
        "3. Ensure your choices are within the grid size for the selected mode.\n"
    )

    # Display the instructions in a pop-up
    messagebox.showinfo("Game Instructions", instructions)


def setup_ui(self):
    # Title Label with design
    tk.Label(
        self.root,
        text="Treasure Hunt Duel",
        font=LARGE_FONT,
        fg="gold",
        bg="darkblue",
    ).pack(pady=10)

    # Description Label
    tk.Label(
        self.root,
        text="A two-player game where players search for treasure hidden in a grid.",
        font=MEDIUM_FONT,
        wraplength=380,
        justify="center",
    ).pack(pady=5)

    # Instructions Button with design
    tk.Button(
        self.root,
        text="Instructions",
        command=lambda: show_instructions(self),
        font=MEDIUM_FONT,
        bg="lightgreen",
        fg="black",
    ).pack(anchor=tk.NE, padx=10, pady=10)

    # Mode Selection
    mode_frame = tk.Frame(self.root, bg="lightgrey")
    mode_frame.pack(pady=5, anchor=tk.CENTER, expand=True)
    tk.Label(mode_frame, text="Select Mode:", font=MEDIUM_FONT).pack(pady=5)
    self.mode_var = tk.StringVar(value="Classic")
    modes = ["Classic", "Advanced"]
    for mode in modes:
        tk.Radiobutton(
            mode_frame,
            text=mode,
            variable=self.mode_var,
            value=mode,
            command=lambda: update_grid_size(self),
            font=MEDIUM_FONT,
            bg="lightgrey",
        ).pack(anchor=tk.CENTER, side="left", padx=5)

    # Instructions
    tk.Label(
        self.root,
        text="Players, select your grid cells:",
        font=MEDIUM_FONT,
    ).pack(pady=5)

    # Grid for both players
    self.grid_frame = tk.Frame(self.root, bg="white")
    self.grid_frame.pack(pady=10, padx=10)
    create_grid(self, grid_color="lightblue")

    # Player Indicator
    self.player_indicator = tk.Label(
        self.root, text="Player 1's turn", font=MEDIUM_FONT, fg=COLOR_PLAYER1
    )
    self.player_indicator.pack(pady=5)

    # Play and Reset Buttons Frame
    button_frame = tk.Frame(self.root)
    button_frame.pack(pady=10)

    # Play Button with design
    self.play_button = tk.Button(
        button_frame,
        text="Play",
        command=lambda: play_game(self),
        font=MEDIUM_FONT,
        bg="lightblue",
        fg="black",
    )
    self.play_button.pack(side=tk.LEFT)

    # Reset Button with design
    self.reset_button = tk.Button(
        button_frame,
        text="Reset",
        command=lambda: reset_game(self),
        font=MEDIUM_FONT,
        bg="orange",
        fg="black",
    )
    self.reset_button.pack(side=tk.LEFT)

    # Result Display
    self.result_label = tk.Label(self.root, text="", font=MEDIUM_FONT)
    self.result_label.pack(pady=5)

    # Quit Button with design
    tk.Button(
        self.root,
        text="Quit",
        command=self.root.quit,
        font=MEDIUM_FONT,
        bg="red",
        fg="white",
    ).pack(pady=5)


def update_grid_size(self):
    mode = self.mode_var.get()
    if mode == "Classic":
        self.grid_size = 3
        self.grid_color = "lightblue"
    elif mode == "Advanced":
        self.grid_size = 5
        self.grid_color = "lightgreen"
    self.treasure_location = (
        rd.randint(0, self.grid_size - 1),
        rd.randint(0, self.grid_size - 1),
    )
    create_grid(self, self.grid_color)
    self.result_label.config(text="")

    # Change grid color
    for row in range(self.grid_size):
        for col in range(self.grid_size):
            self.buttons[row][col].config(bg=self.grid_color)

    # Reset game state
    self.player_indicator.config(text="Player 1's turn", fg=COLOR_PLAYER1)
    self.play_button.config(bg="SystemButtonFace", state=tk.NORMAL)
    self.player1_choice = None
    self.player2_choice = None
    self.player1_clicked = False
    self.player2_clicked = False


def create_grid(self, grid_color="SystemButtonFace"):
    for widget in self.grid_frame.winfo_children():
        widget.destroy()
    self.buttons = []

    # Create row and column labels with design
    for row in range(self.grid_size + 1):
        row_buttons = []
        for col in range(self.grid_size + 1):
            if row == 0 and col == 0:
                label = tk.Label(self.grid_frame, text="", bg="white")
            elif row == 0:
                label = tk.Label(
                    self.grid_frame,
                    text=str(col - 1),
                    font=MEDIUM_FONT,
                    bg="lightgrey",
                    padx=10,
                    pady=5,
                )
            elif col == 0:
                label = tk.Label(
                    self.grid_frame,
                    text=str(row - 1),
                    font=MEDIUM_FONT,
                    bg="lightgrey",
                    padx=10,
                    pady=5,
                )
            else:
                button = tk.Button(
                    self.grid_frame,
                    text="",
                    width=4,
                    height=2,
                    bg=grid_color,
                    font=MEDIUM_FONT,
                    command=lambda r=row - 1, c=col - 1: select_cell(self, r, c),
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                row_buttons.append(button)
                continue
            label.grid(row=row, column=col, padx=5, pady=5)
        if row > 0:
            self.buttons.append(row_buttons)


def select_cell(self, row, col):
    if self.current_player == 1 and not self.player1_clicked:
        self.player1_choice = (row, col)
        self.current_player = 2
        self.player1_clicked = True
        self.player_indicator.config(text="Player 2's turn", fg=COLOR_PLAYER2)
    elif self.current_player == 2 and not self.player2_clicked:
        self.player2_choice = (row, col)
        self.current_player = 1
        self.player2_clicked = True
        self.player_indicator.config(text="Player 1's turn", fg=COLOR_PLAYER1)

    # Check if both players have made their choices
    if self.player1_clicked and self.player2_clicked:
        self.player_indicator.config(text="All set", fg="green")
        self.play_button.config(bg="green")
        for row_buttons in self.buttons:
            for button in row_buttons:
                button.config(state=tk.DISABLED)


def play_game(self):
    try:
        # Validate Inputs
        if self.player1_choice is None:
            raise ValueError("Player 1 has not selected a cell.")
        if self.player2_choice is None:
            raise ValueError("Player 2 has not selected a cell.")

        # Determine Payoff
        game_logic = TreasureHuntGameLogic(self.grid_size, self.treasure_location)
        payoff = game_logic.determine_payoff(
            self.player1_choice, self.player2_choice, self.mode_var.get()
        )
        result_text = (
            f"Treasure is at: {self.treasure_location}\n"
            f"Player 1 chose: {self.player1_choice}\n"
            f"Player 2 chose: {self.player2_choice}\n"
            f"Payoff -> Player 1: {payoff[0]}%, Player 2: {payoff[1]}%\n"
        )

        # Determine the winner
        if payoff[0] > payoff[1]:
            result_text += "Winner: Player 1"
        elif payoff[1] > payoff[0]:
            result_text += "Winner: Player 2"
        else:
            result_text += "It's a tie!"

        self.result_label.config(text=result_text)

        # Make play button unclickable
        self.play_button.config(state=tk.DISABLED)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception:
        messagebox.showerror("Error", "An unexpected error occurred.")


def reset_game(self):
    self.player_indicator.config(text="Player 1's turn", fg=COLOR_PLAYER1)
    self.play_button.config(bg="SystemButtonFace", state=tk.NORMAL)
    self.result_label.config(text="")
    self.player1_choice = None
    self.player2_choice = None
    self.player1_clicked = False
    self.player2_clicked = False
    self.treasure_location = (
        rd.randint(0, self.grid_size - 1),
        rd.randint(0, self.grid_size - 1),
    )
    for row in range(self.grid_size):
        for col in range(self.grid_size):
            self.buttons[row][col].config(
                bg=self.grid_color,
                state=tk.NORMAL,
                image="",
                compound="none",
                width=4,
                height=2,
            )


def resource_path(relative_path):
    # Get the absolute path to resources
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
