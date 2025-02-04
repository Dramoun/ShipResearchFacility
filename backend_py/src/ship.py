from typing import Tuple


class Ship:
    def __init__(self, _id: str, name: str, designation: str, direction: list, position: Tuple[int, int] = (0, 0)):
        self.id = _id
        self.name = name
        self.designation = designation
        self.direction = direction
        self.position = position  # Set initial position
        self.cells = []

    def rotate(self, times: int = 1):
        """Rotates the ship's direction by 90 degrees clockwise."""
        # Transpose and reverse the rows to rotate 90 degrees clockwise
        for _ in range(times):
            self.direction = [list(row) for row in zip(*self.direction[::-1])]
        self.cells = []  # Reset the cells as the direction has changed

    def place(self, grid: list):
        """Places the ship on the grid at the current position."""
        self.cells = []
        for r, row in enumerate(self.direction):
            for c, cell in enumerate(row):
                if cell == 1:
                    #occupied_r = r + self.position[0]
                    #occupied_c = c + self.position[1]
                    self.cells.append((r + self.position[0], c + self.position[1]))
                    #print(f"Placing at ({occupied_r}, {occupied_c})")

        # Mark the cells on the grid as alive
        for r, c in self.cells:
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                grid[r][c] = 1

    def get_cells(self):
        """Returns the list of cells occupied by the ship."""
        return self.cells
