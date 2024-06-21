import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import unittest
from Tile import Tile 



class TestTurnTile(unittest.TestCase):
    def test_new_tile_is_unturned(self) -> None:
        tile: Tile = Tile(25)
        self.assertFalse(tile.is_turned)
    
    def test_unturned_tile_is_turnable(self) -> None:
        tile: Tile = Tile(25)
        self.assertFalse(tile.is_turned)
        self.assertTrue(tile.turn())
        self.assertTrue(tile.is_turned)
        
    def test_turned_tile_is_not_turnable(self) -> None:
        tile: Tile = Tile(25)
        tile.turn()
        self.assertTrue(tile.is_turned)
        self.assertFalse(tile.turn())
        self.assertTrue(tile.is_turned)


class TestCalculateWorms(unittest.TestCase):
    def test_one_worm(self) -> None:
        self.assertEqual(Tile.calculate_worms(21), 1)
        self.assertEqual(Tile.calculate_worms(22), 1)
        self.assertEqual(Tile.calculate_worms(23), 1)
        self.assertEqual(Tile.calculate_worms(24), 1)
        
    def test_two_worm(self) -> None:
        self.assertEqual(Tile.calculate_worms(25), 2)
        self.assertEqual(Tile.calculate_worms(26), 2)
        self.assertEqual(Tile.calculate_worms(27), 2)
        self.assertEqual(Tile.calculate_worms(28), 2)

    def test_tree_worm(self) -> None:
        self.assertEqual(Tile.calculate_worms(29), 3)
        self.assertEqual(Tile.calculate_worms(30), 3)
        self.assertEqual(Tile.calculate_worms(31), 3)
        self.assertEqual(Tile.calculate_worms(32), 3)

    def test_four_worm(self) -> None:
        self.assertEqual(Tile.calculate_worms(33), 4)
        self.assertEqual(Tile.calculate_worms(34), 4)
        self.assertEqual(Tile.calculate_worms(35), 4)
        self.assertEqual(Tile.calculate_worms(36), 4)
    
    def test_invalid_low(self) -> None:
        with self.assertRaises(ValueError):
            Tile.calculate_worms(20)

    def test_invalid_high(self) -> None:
        with self.assertRaises(ValueError):
            Tile.calculate_worms(37)
