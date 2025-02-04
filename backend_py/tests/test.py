import time
from typing import List
from utils.general_utils import GeneralUtils
from typing import List, Tuple
from src.game_loop import GameLoop
from src.ship import Ship


def import_ships(file_name: str) -> List[dict]:
    return GeneralUtils.load_from_json(file_name=file_name)


if __name__ == '__main__':
    #todo something usefull here, this is not working,
    # probably update game loop function to be more lative for out game and have
    # mode with non pygame and only in background for faster calculations
    # Import ship data
    game_rows = 400
    game_cols = 400
    game_center = (int(game_rows / 2), int(game_cols / 2))
    print(game_center)

    game_loop = GameLoop(
        rows=game_rows, cols=game_cols, cell_size=5,
        delay=0.1, timer_limit=5
    )
    ship_list = import_ships("./ships.json")
    print(len(ship_list))
    game_loop.run()
    # Create a new game loop for each ship
    for ship_data in ship_list:
        game_loop.clear_grid()
        # Define the ship size based on its direction
        ship_size_x = len(ship_data['initial_direction'])
        ship_size_y = len(ship_data['initial_direction'][0])

        # Create the ship object and place it in the center
        print(ship_data['initial_direction'])
        ship_obj = Ship(
            _id=ship_data['id'],
            name=ship_data['name'],
            designation=ship_data['designation'],
            direction=ship_data['initial_direction'],
            position=game_center  # Place ship in the middle of the grid
        )

        # Add the ship to the game loop (each game has its own ship)
        game_loop.add_ship(ship=ship_obj)

        # Run the game loop for this ship

        time.sleep(5)
        game_loop.clear_ships()
