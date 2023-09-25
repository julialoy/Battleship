# Author: Julia Loy
# GitHub username: julialoy
# Date: 03/11/2022
# Description: This project allows two users to play a game of Battleship. Players first place their ships then
# fire torpedoes at their opponent, attempting to sink all of their opponent's ships. The player who sinks all of their
# opponents ships wins the game. The game tracks the current game state, validates and places ships, fires torpedoes,
# and can display a player's 10 x 10 game board. In this version of Battleship, players place as many ships on their
# boards as like as long as all ships have valid lengths (no less than 2, no more than 10), are placed completely on
# the game board, and don't overlap any part of another ship. Turn taking is not tracked until a torpedo is fired;
# the player designated "first" always takes the first turn.


class GameGrid:
    """A class that represents a player's 10 x 10 game board. This class is used by the Player class to hold the
    Player’s game board. The ShipGame class accesses each Player’s GameGrid for piece validation and torpedo coordinate
    validation.

    This class is responsible for validating coordinates used to place ships and fire torpedoes, it also displays the
    placement of a player’s ships and the coordinates of where the player’s opponent fired a torpedo.
    """
    def __init__(self):
        """Creates a new, empty instance of the GameGrid object, stored in the private data member _grid.

        Parameters: None

        Returns: None
        """
        self._grid = self._create_new_grid()

    def _create_new_grid(self):
        """A private method used by the __init__() method to create a blank game grid.
        The grid is represented by a 2D list.

        Parameters: None

        Returns: game grid (2D list)
        """
        grid = [[str(num) for num in range(0, 11)]]  # Create a list of numbers up to 10
        for letter in "ABCDEFGHIJ":
            row = [" " for num in range(0, 10)]  # Create a list of "empty" spaces to represent a blank board
            row.insert(0, letter)
            grid.append(row)
        return grid

    def get_grid(self):
        """Returns the game grid.

        Parameters: None

        Returns: 2D list representing a player’s 10 x 10 game grid
        """
        return self._grid

    def _validate_row(self, row):
        """A private method that takes the row as a letter, turns it into the correct integer, and determines whether
        the row is on the grid. It is used by the add_ship_to_grid() method.

        Parameters: row (str)

        Returns: None if provided row is invalid, row as integer if provided row is valid
        """
        if row not in "ABCDEFGHIJ":
            return None
        else:
            valid_row = "ABCDEFGHIJ".index(row)
            return valid_row+1      # Add one since row 0 on game grid is the "top" row of column numbers

    def _validate_column(self, column):
        """A private method that takes the column as a string and casts it to an integer, then determines whether the
        column is on the grid. It is used by the add_ship_to_grid() method.

        Parameters: Column (str)

        Returns: None if provided column is invalid, column as integer if provided column is valid
        """
        valid_column = int(column)
        if 1 <= valid_column <= 10:
            return valid_column
        else:
            return None

    def _validate_ship_placement(self, coord_list):
        """A private method that determines whether a player’s ship placement is valid. Ship placement is invalid if
        the ship goes off the edge of the player's grid or overlaps a ship already on the player’s grid. This method
        is used by the add_ship_to_grid() method.

        Parameters: a list of all coordinates the ship will occupy

        Returns: True (bool) if the ship can be placed in the specified location, False (bool) if the ship cannot be
        placed in the specified location.
        """
        # Each coordinate is a tuple in the format (row, column)
        for coord in coord_list:
            row = coord[0]
            col = coord[1]
            if 0 <= row > 10 or 0 <= col > 10:
                return False
            # Ships must not overlap any other ship
            elif self._grid[row][col] == "S":
                return False

        # If none of the coordinates of the new ship invalidate the placement, add ship to grid
        for coord in coord_list:
            row = coord[0]
            col = coord[1]
            self._grid[row][col] = "S"
        return True

    def add_ship_to_grid(self, coord, orientation, length):
        """Attempts to place the player’s ship on the game grid. It uses the private methods _validate_row(),
        _validate_column(), and _validate_ship_placement() to ensure that a ship placement is legal per the rules of
        this Battleship game---that is, a ship cannot be placed so that any part of the ship will be off the player’s
        grid and a ship cannot overlap another ship. If the ship placement is valid, the method will update _grid data
        member, marking the positions occupied by the ship with an S in each spot.

        Parameters: A single coordinate as a string, representing a Ship’s starting coordinate; orientation as a string,
        indicating whether the Ship will be placed horizontally or vertically on the grid; length as an int.

        Returns: If the ship placement was valid and the ship was placed on the grid:
                    returns list of valid ship coordinates
                 If the ship placement was invalid:
                    returns empty list
        """
        row = self._validate_row(coord[0])
        column = self._validate_column(coord[1:])
        if row is None or column is None:
            return []   # Empty lists are falsy

        # Coordinates stored as tuples in format (row, column)
        coords_list = []
        # Create a list of all coordinates occupied by the ship
        if orientation == 'C':
            for num in range(row, row + length):
                coord_tuple = (num, column)
                coords_list.append(coord_tuple)
        elif orientation == 'R':
            for num in range(column, column + length):
                coord_tuple = (row, num)
                coords_list.append(coord_tuple)
        # Ensure all coordinates occupied by ship are valid/not already occupied
        is_ship_placed = self._validate_ship_placement(coords_list)
        if is_ship_placed:
            return coords_list
        else:
            return []

    def add_torpedo_hit(self, torpedo_coord):
        """Handles validating and adding a torpedo hit to a Player’s grid. It uses the private methods _validate_row()
        and _validate_column() to ensure that the given coordinates are on the grid and then adds the torpedo hit to
        the grid. A torpedo that missed and hit the water is represented by an asterisk (*) and a hit on a Ship is
        represented by an X. Note that this method only validates the torpedo coordinates and updates the graphic
        representation of the Player’s grid, it does not actually determine whether a Ship was hit/sunk.

        Parameters: A single coordinate as a string to represent where the torpedo hit.

        Returns: If the torpedo coordinate is valid, returns valid row, column (tuple).
                 If the torpedo coordinate is invalid, returns None.

        Note that the return value is not dependent on whether a ship was hit, only on whether the torpedo coordinates
        are valid.
        """
        row = self._validate_row(torpedo_coord[0])
        col = self._validate_column(torpedo_coord[1:])
        if row is None or col is None:
            return None

        # Update the player's grid to show the torpedo hit
        grid_square = self._grid[row][col]
        if grid_square == "S":
            self._grid[row][col] = "X"
        elif grid_square == " ":
            self._grid[row][col] = "*"

        return row, col


class Ship:
    """Represents a ship in the game Battleship. The Ship class is responsible for keeping track of its own length,
    its coordinates on the grid (once it is placed), how many torpedo hits it has and where the torpedo hit, and
    whether it has been sunk.

    This class is used by the ShipGame class and the Player class when placing Ships on the game board, firing
    torpedoes, and determining whether a win has occurred.
    """
    def __init__(self, length):
        """Creates a new Ship object and initializes the private data members _length, _is_sunk, _hits,
        and _coords_on_grid.

        Parameters: ship length (int)
        """
        self._length = length
        self._is_sunk = False
        self._hits = []
        self._coords_on_grid = []

    def get_is_sunk(self):
        """Returns whether a ship has been sunk.

        Parameters: None

        Returns: Value of data member _is_sunk: True (bool) or False (bool)
        """
        return self._is_sunk

    def get_hits(self):
        """Returns the hits a Ship has taken.

        Parameters: None

        Returns: List of coordinates at which the ship has been hit
        """
        return self._hits

    def get_length(self):
        """Returns the length of the Ship.

        Parameters: None

        Returns: length of the ship (int)
        """
        return self._length

    def get_coords_on_grid(self):
        """"Returns the coordinates occupied by the Ship.

        Parameters: None

        Returns: List of the coordinates occupied by the ship.
        """
        return self._coords_on_grid

    def add_hit(self, hit_coord):
        """Adds a torpedo hit to the Ship, adding to the data member _hits. It also determines whether the hit
        sank the Ship.

        Parameters: coordinate where the torpedo hit

        Returns: None
        """
        # Ensure that coordinate is not duplicated in list of hits
        if hit_coord not in self._hits:
            self._hits.append(hit_coord)
        if len(self._hits) == self._length:
            self._is_sunk = True

    def set_coords_on_grid(self, coord_list):
        """This is the setter method for the data member _coords_on_grid. Once a ship is placed on a player’s GameGrid,
        the coordinates occupied by the ship are added to _coords_on_grid.

        Parameters: List of coordinates occupied by the ship

        Returns: None
        """
        self._coords_on_grid = coord_list


class Player:
    """Represents a player for the Battleship game. The class is responsible for tracking the player number (“first”
    or “second”) and the number of Ships a player has on their GameGrid, it also holds the player’s GameGrid. This
    class uses the GameGrid class for the Player’s game board, the Ship class when tracking how many Ships the Player
    has. It is used by the ShipGame class.
    """
    def __init__(self, player):
        """Creates a new Player object and initializes the private data members _player_grid, _player_number,
        and _ships.
        """
        self._player_grid = GameGrid()
        self._player_number = player    # Number is the string "first" or "second"
        self._ships = []

    def get_player_grid(self):
        """Returns the player's game grid.

        Parameters: None

        Returns: GameGrid object
        """
        return self._player_grid

    def get_player_number(self):
        """Returns the player number: “first” or “second”.

        Parameters: None

        Returns: player number (str)
        """
        return self._player_number

    def add_ship(self, ship_obj):
        """""Adds a new Ship to the player’s _ships data member. It is used by ShipGame after a ship has been placed
        on a player’s GameGrid.

        Parameters: Ship object

        Returns: None
        """
        self._ships.append(ship_obj)

    def get_ships(self):
        """Returns a Player’s ships. It is used by ShipGame to determine whether a win has occurred.

        Parameters: None

        Returns: List of Ship objects
        """
        return self._ships

    def remove_sunken_ships(self):
        """Removes any sunken ships from player's list of ships.

        Parameters: None

        Returns: None
        """
        for ship in self._ships:
            if ship.get_is_sunk():
                self._ships.remove(ship)


class ShipGame:
    """Represents a game of Battleship. It uses the Player and Ship classes and makes use of a Player’s GameGrid to
    allow players to place ships and fire torpedoes.

    A Battleship game ends when a player sinks all of their opponents’ ships.

    The ShipGame class is responsible for tracking the current state of the game (unfinished or which player won),
    the current turn, and the game players.
    """
    def __init__(self):
        """Creates a new Battleship game and initializes the private data members _game_state, _current_turn,
        and _players.
        """
        self._game_state = "UNFINISHED"     # Game always starts as unfinished
        self._current_turn = "first"        # First player always starts
        self._players = {"first": Player("first"), "second": Player("second")}

    def show_game_grid(self, player):
        """Prints the GameGrid for the specified player.

        Parameters: player (str)

        Returns: None (prints the player’s GameGrid but does not return it)
        """
        current_player = self._players[player]
        current_grid = current_player.get_player_grid().get_grid()
        print(f"Current game board for the {current_player.get_player_number()} player:")
        for row in current_grid:
            print(" ".join(row))

    def place_ship(self, player, ship_length, ship_coords, ship_orientation):
        """Attempts to place a ship on a player’s GameGrid. It ensures that the ship is a valid length, creates a new
        Ship object, and uses the Player’s GameGrid to validate the coordinates for the Ship. If the ship length and
        coordinates are valid, a new Ship is placed on the Player’s GameGrid and added to the Player’s list of ships.
        A ship may not be placed such that any part of it is off the GameGrid or overlaps part of another ship.

        Turn taking is not checked during ship placement.

        Parameters: player (str); ship_length (int); ship_coords (str); ship_orientation (str)

        Returns: True (bool) if the ship length and coordinates are valid and the ship is successfully placed on the
        Player’s GameGrid or False (bool) if the ship length or coordinates are invalid.
        """
        if 2 > ship_length or ship_length > 10:
            return False

        new_ship = Ship(ship_length)
        current_player = self._players[player]
        if current_player:
            ship_validation = current_player.get_player_grid().add_ship_to_grid(ship_coords,
                                                                                ship_orientation,
                                                                                ship_length
                                                                                )
            if not ship_validation:
                return False
            else:
                complete_coords = ship_validation
                new_ship.set_coords_on_grid(complete_coords)
                current_player.add_ship(new_ship)
                return True
        else:
            # If the player number was not "first" or "second", player is invalid
            return False

    def get_current_state(self):
        """Returns the current state of the game. Either the game is unfinished or a player has won.
        The game cannot end in a draw.

        Parameters: None

        Returns: FIRST_WON (str), SECOND_WON (str), or UNFINISHED (str)
        """
        return self._game_state

    def fire_torpedo(self, player, target_coords):
        """Attempts to fire a torpedo at an opponent’s board. The opponent’s GameGrid is used to validate the torpedo
        coordinates. If one of the opponent’s ships was hit, the opponent’s Ship object is updated with the coordinate
        and the Ship determines whether or not the hit resulted in the Ship sinking. If the ship sinks, it is removed
        from the opponent’s ship list. If the hit results in the opponent’s final ship sinking, the game state is
        updated to reflect that the current player won.

        Parameters: player (str), target_coords (str)

        Returns: True (bool) if the torpedo coordinates are valid or False (bool) if the torpedo coordinates are
        invalid or if the torpedo was fired out of turn or after a game finished.

        Note that the return value is not dependent on whether the torpedo hit a ship.
        """
        if self.get_current_state() != "UNFINISHED" or self._current_turn != player:
            return False

        # Target_player is the opponent of the player who is taking a turn/firing the torpedo
        target_player = self._players["second"] if player == "first" else self._players["first"]
        torpedo_valid = target_player.get_player_grid().add_torpedo_hit(target_coords)
        if not torpedo_valid:
            return False
        else:
            # Coordinates are a tuple in the format (row, column)
            validated_coords = torpedo_valid
            for player_ship in target_player.get_ships():
                if validated_coords in player_ship.get_coords_on_grid():
                    # The ship object ensures that coordinates are not duplicated when adding a hit
                    player_ship.add_hit(validated_coords)
            target_player.remove_sunken_ships()
            if self.get_num_ships_remaining(target_player.get_player_number()) == 0:
                self._game_state = "SECOND_WON" if player == "second" else "FIRST_WON"
            else:
                # Swap turns if the game was not won
                self._current_turn = "first" if self._current_turn == "second" else "second"
            return True

    def get_num_ships_remaining(self, player):
        """Returns the number of ships the specified player has left on their GameGrid. This uses the Player class’s
        get_ships() method to determine how many ships a Player has.

        Parameters: player (str)

        Returns: Number of ships player has left (int)
        """
        selected_player = self._players[player]
        if selected_player is not None:
            return len(selected_player.get_ships())
