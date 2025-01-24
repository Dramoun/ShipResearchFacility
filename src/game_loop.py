import time
from typing import Tuple, Optional, List

import pygame

from src.game import Game
from src.ship import Ship
from src.ship_detector import ShipDetector


class GameLoop:
    def __init__(self, rows: int, cols: int, cell_size: int, ships: Optional[List[Ship]] = None,
                 delay: float = 1.0, window_size: Tuple[int, int] = (800, 600), timer_limit: float = None):
        self.game = Game(rows, cols)
        self.ships = ships  # List of ships
        self.delay = delay
        self.timer_limit = timer_limit
        self.start_time = pygame.time.get_ticks()
        self.window_size = window_size
        self.ship_detector = ShipDetector(self.game.grid.grid_coordinates)

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Game of Life with Ship Movement")

        # Cell size (adjust this for the resolution of the grid)
        self.cell_size = cell_size

        # Place the ships on the grid initially
        if ships:
            for ship in self.ships:
                ship.place(self.game.grid.grid_coordinates)

    def update(self):
        """Updates the game grid and processes the game state."""
        # Update the grid with the Game of Life rules
        self.game.grid.update()  # Call the grid's update method

        # Detect moving ships after the grid update
        self.ship_detector.grid = self.game.grid.grid_coordinates
        moving_ships = self.ship_detector.detect_and_classify_ships()

        # Display moving ships' direction information
        if moving_ships:
            x = 1
            for ship_info in moving_ships:
                print(x, ship_info)
                x += 1
        # Handle Pygame events (e.g., quitting the game)
        self.handle_events()

        # Draw the grid and ships
        self.draw_grid()

    @staticmethod
    def handle_events():
        """Handles Pygame events (e.g., quit, key press)."""
        pass

    def draw_grid(self):
        """Draws the grid and ships on the Pygame window."""
        self.screen.fill((255, 255, 255))  # Fill the screen with white
        # Draw the cells of the grid
        for r in range(len(self.game.grid.grid_coordinates)):
            for c in range(len(self.game.grid.grid_coordinates[0])):
                color = (0, 0, 0) if self.game.grid.grid_coordinates[r][c] == 1 else (255, 255, 255)
                pygame.draw.rect(self.screen, color,
                                 (c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size))

        # Update the display
        pygame.display.flip()

    def add_ship(self, ship: Ship):
        """Adds a new ship to the game."""
        if not self.ships:
            self.ships = []
        self.ships.append(ship)
        ship.place(self.game.grid.grid_coordinates)

    def run(self):
        """Runs the game loop."""
        running = True
        while running:
            self.update()
            time.sleep(self.delay)  # Wait before the next update

            # Check for quit event and time limit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Exit the loop
                    break  # No more events should be processed after quitting

        # Quit Pygame safely after the loop ends
        self.quit_game()

    @staticmethod
    def quit_game():
        """Handles quitting the game after the time limit is reached."""
        print("Game time has ended!")
        pygame.quit()  # This safely quits the Pygame system after the loop
        exit()  # Exit the program

    def clear_grid(self):
        """Just clears the grid, making way for new ship or runs."""
        self.game.grid.clear()

    def clear_ships(self):
        """Clears the list of ships."""
        self.ships = []


if __name__ == '__main__':
    #https://conwaylife.com/patterns/163p4h1v0.rle
    rle_data = """
x = 19, y = 37, rule = b3/s23
7bobobo7b$6b7o6b$5bo7bo5b$b3ob3o3b3ob3ob$o17bo$bo7bo7bob$bob2o9b2obob
2$2b3o9b3o2b$2b3o9b3o2b$5bo7bo5b$bo4bo5bo4bob$bobo11bobob$7bo3bo7b$7bo
3bo7b$5bo2bobo2bo5b$5bo7bo5b$4bo9bo4b$4bobo5bobo4b$4b2obo3bob2o4b$5bob
2ob2obo5b$7bobobo7b$8bobo8b$6bobobobo6b$5b2obobob2o5b$8bobo8b$7b2ob2o
7b$4b3obobob3o4b$4bobobobobobo4b$4bo3bobo3bo4b$8bobo8b$4bo2b5o2bo4b$3b
4o5b4o3b$b2o13b2ob$b2obo9bob2ob$2bobo4bo4bobo2b$4b2o7b2o!
    """

    from typing import List

    import re


    def rle_to_2d_grid(rle_data: str) -> list:
        """
        Convert RLE data for a Game of Life pattern into a 2D grid.

        Args:
            rle_data (str): The RLE-encoded pattern data.

        Returns:
            list: A 2D grid representing the pattern.
        """
        # Extract the grid size from the RLE header (x, y dimensions)
        match = re.match(r"x = (\d+), y = (\d+), rule = .*$", rle_data.strip().splitlines()[0])
        if not match:
            raise ValueError("Invalid RLE header")

        width, height = int(match.group(1)), int(match.group(2))

        # Remove the header from the RLE data
        rle_data = '\n'.join(rle_data.strip().splitlines()[1:])

        # Initialize an empty grid with all cells set to 0 (dead)
        grid = [[0] * width for _ in range(height)]

        x = y = 0  # Starting position on the grid

        # Loop through the RLE data and populate the grid
        for line in rle_data.splitlines():
            idx = 0
            while idx < len(line):
                # Check if it's a number (repetition count) or character (cell type)
                if line[idx].isdigit():
                    # Handle the run-length (repetition)
                    count = 0
                    while idx < len(line) and line[idx].isdigit():
                        count = count * 10 + int(line[idx])
                        idx += 1
                else:
                    # Handle the cells (one unit for each character 'b' or 'o')
                    count = 1

                char = line[idx]

                if char == 'b':  # 'b' is for a dead cell (0)
                    for _ in range(count):
                        if 0 <= y < height and 0 <= x < width:
                            grid[y][x] = 0
                        x += 1
                elif char == 'o':  # 'o' is for an alive cell (1)
                    for _ in range(count):
                        if 0 <= y < height and 0 <= x < width:
                            grid[y][x] = 1
                        x += 1
                elif char == '$':  # End of a row
                    y += 1
                    x = 0
                idx += 1

        # Return the grid after populating all cells
        return grid


    # Decode and format the RLE
    decoded_grid = grid = rle_to_2d_grid(rle_data)
    for row in grid:
        print(row)

    # Initialize ships (examples)
    glider_direction = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0,
         0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0,
         0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0]
    ]
    glider_ship = Ship("glider", "Lightweight Spaceship", "Glider",
                       decoded_grid, position=(50, 50))
    glider_ship.rotate(2)

    spaceship_direction = [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1]
    ]
    spaceship_ship = Ship("spaceship", "Heavy Spaceship", "Spaceship",
                          spaceship_direction, position=(40, 60))

    # Initialize the game loop and run the simulation
    game_loop = GameLoop(
        rows=200, cols=200, cell_size=5,
        ships=[glider_ship],
        delay=0.05
    )
    game_loop.run()
