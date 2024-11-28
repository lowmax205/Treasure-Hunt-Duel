class TreasureHuntGameLogic:
    def __init__(self, grid_size, treasure_location):
        self.grid_size = grid_size
        self.treasure_location = treasure_location

    def calculate_distance(self, cell1, cell2):
        return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

    def determine_payoff(self, player1, player2, mode):
        if player1 == player2:  # Both chose the same cell
            return (50, 50)
        else:
            dist1 = self.calculate_distance(player1, self.treasure_location)
            dist2 = self.calculate_distance(player2, self.treasure_location)
            if mode == "Classic":
                if dist1 < dist2:  # Player 1 is closer
                    return (75, 25)
                elif dist2 < dist1:  # Player 2 is closer
                    return (25, 75)
                else:  # Equal distance, split evenly
                    return (50, 50)
            elif mode == "Advanced":
                if dist1 < dist2:  # Player 1 is closer
                    return (80, 20)
                elif dist2 < dist1:  # Player 2 is closer
                    return (20, 80)
                else:  # Equal distance, split evenly
                    return (50, 50)
