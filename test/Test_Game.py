import unittest
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from Game import Game
from Player import Player


class TestAddPlayer(unittest.TestCase):
    def test_one_player(self) -> None:
        game: Game = Game()
        player: Player = Player("Per")
        game.add_player(player)
        self.assertEqual(game.players, [player])

class TestNextPlayer(unittest.TestCase):
    def test_one_player(self) -> None:
        game: Game = Game()
        player: Player = Player("Per")
        game.add_player(player)
        self.assertEqual(game.next_player(), player)
        self.assertEqual(game.next_player(), player)

    def test_two_player(self) -> None:
        game: Game = Game()
        player1: Player = Player("Per")
        game.add_player(player1)
        player2: Player = Player("pål")
        game.add_player(player2)
        self.assertEqual(game.next_player(), player1)
        self.assertEqual(game.next_player(), player2)
        self.assertEqual(game.next_player(), player1)
        self.assertEqual(game.next_player(), player2)

class TestGameIsActive(unittest.TestCase):
    def test_game_is_active_new_game(self) -> None:
        game: Game = Game()
        game.setup()
        self.assertTrue(game.is_active())

    def test_game_is_active_some_tiles_is_turned(self) -> None:
        game: Game = Game()
        game.setup()
        for index, tile in enumerate(game.board_tiles):
            if index % 2 == 0:
                tile.turn()
        self.assertTrue(game.is_active())

    def test_game_is_active_all_tiles_is_turned(self) -> None:
        game: Game = Game()
        game.setup()
        for tile in game.board_tiles:
            tile.turn()
        self.assertFalse(game.is_active())

class TestGameSetup(unittest.TestCase):
    def test_game_setup_tile_creation(self) -> None:
        game: Game = Game()
        game.setup()
        
        self.assertEqual(len(game.board_tiles),16)
        for index, dice_score in enumerate(range(21, 37), start=0):
            self.assertEqual(game.board_tiles[index].dice_score, dice_score)


