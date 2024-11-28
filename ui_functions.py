import tkinter as tk
from tkinter import messagebox
import random as rd
from game_logic import TreasureHuntGameLogic

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
    # Title Label
    tk.Label(self.root, text="Treasure Hunt Duel", font=LARGE_FONT).pack(pady=10)

    # Instructions Button
    tk.Button(
        self.root, text="Instruction!", command=lambda: show_instructions(self)
    ).pack(anchor=tk.NE, padx=10, pady=10)

    # Mode Selection
    mode_frame = tk.Frame(self.root)
    mode_frame.pack(pady=5, anchor=tk.CENTER, expand=True)
    tk.Label(mode_frame, text="Select Mode:").pack(pady=5)
    self.mode_var = tk.StringVar(value="Classic")
    modes = ["Classic", "Advanced"]
    for mode in modes:
        tk.Radiobutton(
            mode_frame,
            text=mode,
            variable=self.mode_var,
            value=mode,
            command=lambda: update_grid_size(self),
        ).pack(anchor=tk.CENTER)

    # Instructions
    tk.Label(self.root, text="Players, select your grid cells:").pack(pady=5)

    # Grid for both players
    self.grid_frame = tk.Frame(self.root)
    self.grid_frame.pack()
    create_grid(self, grid_color="lightblue")

    # Player Indicator
    self.player_indicator = tk.Label(
        self.root, text="Player 1's turn", font=MEDIUM_FONT, fg=COLOR_PLAYER1
    )
    self.player_indicator.pack(pady=5)

    # Play Button
    self.play_button = tk.Button(
        self.root, text="Play", command=lambda: play_game(self)
    )
    self.play_button.pack(pady=10)

    # Reset Button
    self.reset_button = tk.Button(
        self.root, text="Reset", command=lambda: reset_game(self)
    )
    self.reset_button.pack(pady=10)

    # Result Display
    self.result_label = tk.Label(self.root, text="", font=MEDIUM_FONT)
    self.result_label.pack(pady=5)

    # Quit Button
    tk.Button(self.root, text="Quit", command=self.root.quit).pack(pady=5)


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

    # Create row and column labels
    for row in range(self.grid_size + 1):
        row_buttons = []
        for col in range(self.grid_size + 1):
            if row == 0 and col == 0:
                label = tk.Label(self.grid_frame, text="")
            elif row == 0:
                label = tk.Label(self.grid_frame, text=str(col - 1))
            elif col == 0:
                label = tk.Label(self.grid_frame, text=str(row - 1))
            else:
                button = tk.Button(
                    self.grid_frame,
                    text="",
                    width=4,
                    height=2,
                    bg=grid_color,
                    command=lambda r=row - 1, c=col - 1: select_cell(self, r, c),
                )
                button.grid(row=row, column=col)
                row_buttons.append(button)
                continue
            label.grid(row=row, column=col)
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

        # Show player choices
        self.buttons[self.player1_choice[0]][self.player1_choice[1]].config(
            bg=COLOR_PLAYER1
        )
        self.buttons[self.player2_choice[0]][self.player2_choice[1]].config(
            bg=COLOR_PLAYER2
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
            self.buttons[row][col].config(bg=self.grid_color, state=tk.NORMAL)
