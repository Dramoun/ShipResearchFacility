from typing import List, Dict, Tuple
import numpy as np


class ShipDetector:
    #TODO : moving bolean output
    #TODO : add detector if its completely the same, and stop checking cuz simulation is dead
    #TODO : separate if one smaler part separated and is moving rest is stationary or just separate totaly in parts

    # TODO : posible way to go, have a patern history where we store patterns, if its been repeating same couple paterns in a loop, its a nice moving ship, we dont need to check anymroe, same logic as ded simulation we can move on
    def __init__(self, grid: np.ndarray, max_history: int = 7):
        """
        Initializes the ShipDetector with the grid and an optional maximum history for grid states.
        """
        self.grid = grid
        self.past_states = []  # Stores past grid states for comparison
        self.max_history = max_history
        self.patterns = {}  # Stores detected patterns and their repeat counts

    def detect_and_classify_ships(self) -> List[Dict]:
        """
        Detects moving ships in the current grid state by comparing it with past grid states.
        Identifies repeating patterns and waits for them to repeat at least twice.
        """
        moving_ships = []

        # Step 1: Compare current grid with past states to identify movement and repeating patterns
        for past_state in self.past_states:
            _, pattern = self.compare_grids(past_state, self.grid)

            # If a repeating pattern is detected
            if pattern:
                # Convert the pattern to a tuple for hashing
                pattern_tuple = tuple(pattern)

                # Increment the pattern count, or initialize it
                if pattern_tuple in self.patterns:
                    self.patterns[pattern_tuple] += 1
                else:
                    self.patterns[pattern_tuple] = 1

                # Only add the pattern if it has been repeated more than once
                if self.patterns[pattern_tuple] > 1:
                    moving_ships.append({'pattern': pattern_tuple, 'repeated': self.patterns[pattern_tuple]})
                    # Optional: Remove the pattern after it has been returned to avoid redundant results

        # Step 2: Store the current grid state for future comparisons
        self.past_states.append(np.copy(self.grid))  # Ensure deep copy

        # Limit the history of past states
        if len(self.past_states) > self.max_history:
            self.past_states.pop(0)

        return moving_ships

    def get_live_cells(self, grid: np.ndarray) -> List[Tuple[int, int]]:
        """
        Extracts live cells (value 1) from the grid.
        """
        return [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == 1]

    def compare_grids(self, grid_a: np.ndarray, grid_b: np.ndarray) -> Tuple[bool, List[Tuple[int, int]]]:
        """
        Compares two grids to detect movement of cells based on their relative positions.
        Also detects repeating patterns by comparing relative positions.
        """
        # Extract live cells from both grids
        live_cells_a = self.get_live_cells(grid_a)
        live_cells_b = self.get_live_cells(grid_b)

        # If number of live cells is different, definitely moved
        if len(live_cells_a) != len(live_cells_b):
            return False, []

        # Find the reference cell in grid_a (for example, top-left-most cell)
        ref_cell_a = live_cells_a[0]

        # Calculate relative positions of live cells in grid_a based on the reference
        rel_positions_a = [(r - ref_cell_a[0], c - ref_cell_a[1]) for (r, c) in live_cells_a]

        # Find the reference cell in grid_b (top-left-most cell)
        ref_cell_b = live_cells_b[0]

        # Calculate relative positions of live cells in grid_b based on the reference
        rel_positions_b = [(r - ref_cell_b[0], c - ref_cell_b[1]) for (r, c) in live_cells_b]

        # If relative positions match, there has been no movement (or the movement is consistent)
        if sorted(rel_positions_a) == sorted(rel_positions_b):
            return True, rel_positions_a  # Identified a repeating pattern

        return False, []  # No movement or no repeating pattern
