from typing import List, Tuple


class Grid:
    """
    Represents the game grid_coordinates where cells can be alive or dead, and ships can be placed.

    Attributes:
    - rows (int): Number of rows in the grid_coordinates.
    - cols (int): Number of columns in the grid_coordinates.
    - grid_coordinates (List[List[int]]): 2D grid_coordinates of cells (0 = dead, 1 = alive).

    Methods:
    - initialize(): Initializes the grid_coordinates to be all dead cells (0).
    - update(): Updates the grid_coordinates based on the Game of Life rules.
    - place_ship(ship, position): Places a ship on the grid_coordinates at the specified position.
    - clear(): Clears the grid_coordinates (resets to all dead cells).
    """

    def __init__(self, rows: int, cols: int) -> None:
        """
        Initializes the grid_coordinates with the specified size and an empty state.

        Args:
        - rows (int): Number of rows in the grid_coordinates.
        - cols (int): Number of columns in the grid_coordinates.
        """
        self.rows = rows
        self.cols = cols
        self.grid_coordinates = self.initialize()

    def initialize(self) -> List[List[int]]:
        """
        Initializes the grid_coordinates to be all dead cells (0).

        Returns:
        - List[List[int]]: A 2D list representing the empty grid_coordinates.
        """
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def update(self) -> None:
        """
        Updates the grid_coordinates based on the Game of Life rules.

        Rules:
        - A cell survives if it has 2 or 3 neighbors.
        - A dead cell becomes alive if it has 3 neighbors.

        Returns:
        - None
        """
        new_grid = self.initialize()

        for r in range(self.rows):
            for c in range(self.cols):
                alive_neighbors = self.count_alive_neighbors(r, c)
                if self.grid_coordinates[r][c] == 1:  # Alive cell
                    new_grid[r][c] = 1 if alive_neighbors in [2, 3] else 0
                else:  # Dead cell
                    new_grid[r][c] = 1 if alive_neighbors == 3 else 0

        self.grid_coordinates = new_grid

    def count_alive_neighbors(self, row: int, col: int) -> int:
        """
        Counts the number of alive neighbors for a given cell.

        Args:
        - row (int): Row index of the cell.
        - col (int): Column index of the cell.

        Returns:
        - int: The number of alive neighbors.
        """
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),         (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        count = 0

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                count += self.grid_coordinates[r][c]

        return count

    def place_ship(self, ship, position: Tuple[int, int]) -> None:
        """
        Places a ship on the grid_coordinates at the specified position.

        Args:
        - ship (Ship): The ship object to place on the grid_coordinates.
        - position (Tuple[int, int]): The (row, column) position where the ship will be placed.
        """
        cells = ship.get_cells()
        for dr, dc in cells:
            r, c = position[0] + dr, position[1] + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                self.grid_coordinates[r][c] = 1  # Mark the cell as occupied by the ship

    def clear(self) -> None:
        """
        Clears the grid_coordinates (resets it to all dead cells).

        Returns:
        - None
        """
        self.grid_coordinates = self.initialize()
