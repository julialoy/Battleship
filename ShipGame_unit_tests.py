# Unit tests for ShipGame

import unittest
from ShipGame import ShipGame, Player, GameGrid, Ship


class TestShipGame(unittest.TestCase):
    """Contains unit tests for the class ShipGame."""

    def test_create_new_game_instance(self):
        """Confirm that new game instances are unique and are instances of the class ShipGame."""
        new_game = ShipGame()
        self.assertIsInstance(new_game, ShipGame)
        new_game_2 = ShipGame()
        self.assertIsInstance(new_game_2, ShipGame)
        self.assertNotEqual(new_game, new_game_2)
        self.assertIsNot(new_game, new_game_2)


class TestPlayer(unittest.TestCase):
    """Contains unit tests for the class Player."""

    def test_create_new_player_instance(self):
        """Confirm that new player instances are unique and are instances of the class Player.

        Players are created through the ShipGame class.
        """
        new_game = ShipGame()
        self.assertEqual(new_game.get_current_state(), "UNFINISHED")
        player_dict = new_game.__getattribute__("_players")
        self.assertIs(type(player_dict), dict)
        self.assertIsInstance(player_dict["first"], Player)
        self.assertIsInstance(player_dict["second"], Player)
        with self.assertRaises(KeyError):
            player_dict["third"]
        self.assertEqual(len(player_dict), 2)


class TestShipPlacement(unittest.TestCase):
    """Test placement of ships with ShipGame."""
    def setUp(self) -> None:
        self.new_game = ShipGame()
        self.ship_test_1 = self.new_game.place_ship("first", 2, "A9", "C")
        self.ship_test_2 = self.new_game.place_ship("first", 3, "A10", "R")
        self.ship_test_3 = self.new_game.place_ship("second", 3, "A9", "C")
        self.ship_test_4 = self.new_game.place_ship("second", 2, "A8", "R")
        self.ship_test_5 = self.new_game.place_ship("second", 11, "J10", "R")
        self.ship_test_6 = self.new_game.place_ship("first", 10, "A1", "C")
        self.ship_test_7 = self.new_game.place_ship("first", 7, "A2", "R"),
        self.ship_test_8 = self.new_game.place_ship("first", 2, "A10", "C")
        self.ship_test_9 = self.new_game.place_ship("first", 7, "B2", "R")
        self.ship_test_10 = self.new_game.place_ship("first", 9, "C2", "R")
        self.ship_test_11 = self.new_game.place_ship("first", 7, "D2", "C")
        self.ship_test_12 = self.new_game.place_ship("first", 7, "D3", "C")
        self.ship_test_13 = self.new_game.place_ship("first", 7, "D4", "C")
        self.ship_test_14 = self.new_game.place_ship("first", 7, "D5", "C")
        self.ship_test_15 = self.new_game.place_ship("first", 7, "D6", "C")
        self.ship_test_16 = self.new_game.place_ship("first", 7, "D7", "C")
        self.ship_test_17 = self.new_game.place_ship("first", 7, "D8", "C")
        self.ship_test_18 = self.new_game.place_ship("first", 7, "D9", "C")
        self.ship_test_19 = self.new_game.place_ship("first", 7, "D10", "C")

    def test_valid_ship_placement(self) -> None:
        self.assertTrue(self.ship_test_1)
        self.assertTrue(self.ship_test_1)
        self.assertTrue(self.ship_test_3)
        self.assertTrue(self.ship_test_6)
        self.assertTrue(self.ship_test_7)
        self.assertTrue(self.ship_test_8)
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertTrue(self.ship_test_9)
        self.assertTrue(self.ship_test_10)
        self.assertTrue(self.ship_test_11)
        self.assertTrue(self.ship_test_12)
        self.assertTrue(self.ship_test_13)
        self.assertTrue(self.ship_test_14)
        self.assertTrue(self.ship_test_15)
        self.assertTrue(self.ship_test_16)
        self.assertTrue(self.ship_test_17)
        self.assertTrue(self.ship_test_18)
        self.assertTrue(self.ship_test_19)
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")

    def test_invalid_ship_placement(self) -> None:
        self.assertFalse(self.ship_test_2)
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertFalse(self.ship_test_4)
        self.assertFalse(self.ship_test_5)
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")

    def test_ship_placement_separate_boards(self) -> None:
        """Make sure that ships are not placed on both game boards."""
        player_dict = self.new_game.__getattribute__("_players")
        player_1 = player_dict["first"]
        player_2 = player_dict["second"]
        self.assertNotEqual(player_1.get_player_grid(), player_2.get_player_grid())


class TestTorpedo(unittest.TestCase):
    """Contains unit tests for firing torpedo functionality."""

    def setUp(self) -> None:
        self.new_game = ShipGame()
        self.ship_test_1 = self.new_game.place_ship("first", 2, "A9", "C")
        self.ship_test_3 = self.new_game.place_ship("second", 3, "A9", "C")
        self.ship_test_6 = self.new_game.place_ship("first", 2, "A1", "C")

    def test_valid_torpedo(self) -> None:
        self.assertTrue(self.new_game.fire_torpedo("first", "F5"))
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertTrue(self.new_game.fire_torpedo("second", "A9"))
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertFalse(self.new_game.fire_torpedo("second", "A1"))
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertFalse(self.new_game.fire_torpedo("first", "A11"))
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertTrue(self.new_game.fire_torpedo("first", "J10"))
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertTrue(self.new_game.fire_torpedo("second", "F5"))
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertTrue(self.new_game.fire_torpedo("first", "F5"))
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")

    def test_torpedo_sinks_ship(self) -> None:
        self.assertTrue(self.new_game.fire_torpedo("first", "A9"))
        self.assertEqual(self.new_game.get_num_ships_remaining("second"), 1)
        self.assertTrue(self.new_game.fire_torpedo("second", "B2"))
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertEqual(self.new_game.get_num_ships_remaining("first"), 2)
        self.assertTrue(self.new_game.fire_torpedo("first", "B9"))
        self.assertEqual(self.new_game.get_num_ships_remaining("second"), 1)
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertTrue(self.new_game.fire_torpedo("second", "J1"))
        self.assertEqual(self.new_game.get_num_ships_remaining("first"), 2)
        self.assertTrue(self.new_game.fire_torpedo("first", "C9"))
        self.assertEqual(self.new_game.get_num_ships_remaining("first"), 2)
        self.assertEqual(self.new_game.get_current_state(), "FIRST_WON")
        self.assertEqual(self.new_game.get_num_ships_remaining("second"), 0)


    def test_second_win(self):
        self.assertTrue(self.new_game.fire_torpedo("first", "A9"))
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertTrue(self.new_game.fire_torpedo("second", "A9"))
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertTrue(self.new_game.fire_torpedo("first", "D9"))
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertTrue(self.new_game.fire_torpedo("second", "B9"))
        self.assertTrue(self.new_game.fire_torpedo("first", "G1"))
        self.assertTrue(self.new_game.fire_torpedo("second", "A1"))
        self.assertTrue(self.new_game.fire_torpedo("first", "G2"))
        #print(self.new_game.show_game_grid("first"))
        #print(self.new_game.show_game_grid("second"))
        self.assertTrue(self.new_game.fire_torpedo("second", "B1"))
        #print(self.new_game.__getattribute__("_current_turn"))
        self.assertEqual(self.new_game.get_current_state(), "SECOND_WON")
        self.assertEqual(self.new_game.__getattribute__("_current_turn"), "second")


class TestTurnTracking(unittest.TestCase):
    """Contains unit tests for turn tracking."""

    def setUp(self) -> None:
        self.new_game = ShipGame()
        self.ship_test_1 = self.new_game.place_ship("first", 2, "A9", "C")
        self.ship_test_3 = self.new_game.place_ship("second", 3, "A9", "C")
        self.ship_test_6 = self.new_game.place_ship("first", 10, "A1", "C")

    def test_turn_tracking(self):
        current_player = self.new_game.__getattribute__("_current_turn")
        self.assertEqual(current_player, "first")
        self.assertTrue(self.new_game.place_ship("second", 4, "B3", "R"))
        self.assertEqual(self.new_game.__getattribute__("_current_turn"), "first")
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")
        self.assertTrue(self.new_game.fire_torpedo("first", "J1"))
        self.assertEqual(self.new_game.__getattribute__("_current_turn"), "second")
        self.assertTrue(self.new_game.fire_torpedo("second", "A1"))
        self.assertEqual(self.new_game.__getattribute__("_current_turn"), "first")
        self.assertEqual(self.new_game.get_current_state(), "UNFINISHED")


if __name__ == '__main__':
    unittest.main()
