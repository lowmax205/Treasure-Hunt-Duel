import tkinter as tk
from tkinter import messagebox
import random

class TreasureHuntGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Treasure Hunt Duel")
        self.root.geometry("400x450")
        self.grid_size = 5
        self.treasure_location = (random.randint(0, 4), random.randint(0, 4))
        self.player1_choice = None
        self.player2_choice = None

        self.show_instructions()

    def show_instructions(self):
        instructions = (
            "Welcome to Treasure Hunt Duel!\n\n"
            "**Description:**\n"
            "Two players search for treasure hidden in a 5x5 grid. Each player selects a grid cell simultaneously.\n"
            "- If both choose the same cell, they split the treasure equally.\n"
            "- If they choose different cells, the player closer to the treasure gets a larger share.\n\n"
            "**Rules:**\n"
            "1. The grid size is 5x5 (rows and columns range from 0 to 4).\n"
            "2. Players cannot see each other's choices until after selecting.\n"
            "3. Payoff distribution:\n"
            "   - Same cell: 50/50 split.\n"
            "   - Different cells: Closer player gets 75%, farther player gets 25%.\n\n"
            "**How to Play:**\n"
            "1. Enter your grid cell choice (row, column) in the input fields.\n"
            "2. Click 'Play' to reveal the treasure location and results.\n"
            "3. Ensure your choices are within the 5x5 grid (0-4 for both row and column).\n"
        )

        # Display the instructions in a pop-up
        messagebox.showinfo("Game Instructions", instructions)
        self.setup_ui()

    def setup_ui(self):
        # Title Label
        tk.Label(self.root, text="Treasure Hunt Duel", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Instructions
        tk.Label(self.root, text="Players, select your grid cells (row, column):").pack(pady=5)

        # Player 1 Input
        frame1 = tk.Frame(self.root)
        tk.Label(frame1, text="Player 1 (row,col): ").pack(side=tk.LEFT, padx=5)
        self.player1_entry = tk.Entry(frame1, width=5)
        self.player1_entry.pack(side=tk.LEFT)
        frame1.pack(pady=5)

        # Player 2 Input
        frame2 = tk.Frame(self.root)
        tk.Label(frame2, text="Player 2 (row,col): ").pack(side=tk.LEFT, padx=5)
        self.player2_entry = tk.Entry(frame2, width=5)
        self.player2_entry.pack(side=tk.LEFT)
        frame2.pack(pady=5)

        # Play Button
        tk.Button(self.root, text="Play", command=self.play_game).pack(pady=10)

        # Result Display
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=20)

        # Quit Button
        tk.Button(self.root, text="Quit", command=self.root.quit).pack(pady=5)

    def calculate_distance(self, cell1, cell2):
        return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

    def determine_payoff(self, player1, player2):
        if player1 == player2:  # Both chose the same cell
            return (50, 50)
        else:
            dist1 = self.calculate_distance(player1, self.treasure_location)
            dist2 = self.calculate_distance(player2, self.treasure_location)
            if dist1 < dist2:  # Player 1 is closer
                return (75, 25)
            elif dist2 < dist1:  # Player 2 is closer
                return (25, 75)
            else:  # Equal distance, split evenly
                return (50, 50)

    def play_game(self):
        try:
            # Parse Player Choices
            self.player1_choice = tuple(map(int, self.player1_entry.get().strip().split(',')))
            self.player2_choice = tuple(map(int, self.player2_entry.get().strip().split(',')))

            # Validate Inputs
            if not (0 <= self.player1_choice[0] < self.grid_size and 0 <= self.player1_choice[1] < self.grid_size):
                raise ValueError("Player 1's choice is out of bounds.")
            if not (0 <= self.player2_choice[0] < self.grid_size and 0 <= self.player2_choice[1] < self.grid_size):
                raise ValueError("Player 2's choice is out of bounds.")
            
            # Determine Payoff
            payoff = self.determine_payoff(self.player1_choice, self.player2_choice)
            result_text = (
                f"Treasure is at: {self.treasure_location}\n"
                f"Player 1 chose: {self.player1_choice}\n"
                f"Player 2 chose: {self.player2_choice}\n"
                f"Payoff -> Player 1: {payoff[0]}%, Player 2: {payoff[1]}%"
            )
            self.result_label.config(text=result_text)
        
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception:
            messagebox.showerror("Error", "Invalid input format! Use row,col (e.g., 2,3).")

    def run(self):
        self.root.mainloop()

# Run the game
if __name__ == "__main__":
    game = TreasureHuntGame()
    game.run()
