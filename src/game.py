from typing import Tuple
from src.ship import Ship
from src.grid import Grid


class Game:
    """
    The Game class manages the overall game state, including the grid_coordinates, ships, and the game's progress.

    Attributes:
    - grid_coordinates (Grid): The grid_coordinates object that represents the game world.
    - ships (List[Ship]): A list of ships in the game.
    - rules (dict): A dictionary defining the rules for cell survival and birth.

    Methods:
    - initialize(): Initializes the game with an empty grid_coordinates.
    - update(): Updates the game state (grid_coordinates) based on the Game of Life rules.
    - place_ship(ship, position): Places a ship on the grid_coordinates at a specified position.
    - clear(): Resets the game grid_coordinates to its initial state.
    """

    def __init__(self, rows: int, cols: int) -> None:
        """
        Initializes the game with the given grid_coordinates size and sets up the grid_coordinates.

        Args:
        - rows (int): The number of rows in the grid_coordinates.
        - cols (int): The number of columns in the grid_coordinates.
        """
        self.grid = Grid(rows, cols)
        self.ships = []

    def initialize(self) -> None:
        """
        Initializes the game by resetting the grid_coordinates and clearing any placed ships.

        Returns:
        - None
        """
        self.grid.clear()
        self.ships.clear()

    def update(self) -> None:
        """
        Updates the game state by updating the grid_coordinates according to the Game of Life rules.

        Returns:
        - None
        """
        self.grid.update()

    def place_ship(self, ship: Ship, position: Tuple[int, int]) -> None:
        """
        Places a ship on the grid_coordinates at a specific position.

        Args:
        - ship (Ship): The ship to place.
        - position (Tuple[int, int]): The position (row, column)
            on the grid_coordinates where the ship should be placed.
        """
        self.grid.place_ship(ship, position)
        self.ships.append(ship)

    def clear(self) -> None:
        """
        Resets the game, clearing the grid_coordinates and removing all ships.

        Returns:
        - None
        """
        self.grid.clear()
        self.ships.clear()
