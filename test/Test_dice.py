import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))


import unittest
from Dice import Dice
from typing import Union

dice_face_value = Union[int, str]

class TestRollDice(unittest.TestCase):
    def test_first_roll(self) -> None:
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        dice.roll_dice()
        self.assertEquals(len(dice.unselected_dice), 8)
        self.assertEquals(len(dice.selected_dice), 0)
        for die in dice.unselected_dice:
            if isinstance(die, int):
                self.assertLess(die, 6)
                self.assertGreater(die, 0)
            else:
                self.assertEqual(die, worm)
    
class TestSelectFace(unittest.TestCase):
    def test_chose_one_dice(self) -> None:
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        testcase: list[dice_face_value] = [1,2,5,3,worm,3,4,2]
        dice.no_rng_roll(testcase)
        dice.select_face_of_dice(5)
        expected_unselected: list[dice_face_value] = [1,2,3,worm,3,4,2]
        expected_selected: list[dice_face_value] = [5]

        for actual_die, expected_die in zip(dice.unselected_dice, expected_unselected):
            self.assertEqual(actual_die, expected_die)
        for actual_die, expected_die in zip(dice.selected_dice, expected_selected):
            self.assertEqual(actual_die, expected_die)

    
    def test_chose_multiple_dice(self) -> None:
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        testcase: list[dice_face_value] = [1,2,5,3,worm,3,4,2]
        dice.no_rng_roll(testcase)
        dice.select_face_of_dice(2)
        expected_unselected: list[dice_face_value] = [1,5,3,worm,3,4]
        expected_selected: list[dice_face_value] = [2,2]

        for actual_die, expected_die in zip(dice.unselected_dice, expected_unselected):
            self.assertEqual(actual_die, expected_die)
        for actual_die, expected_die in zip(dice.selected_dice, expected_selected):
            self.assertEqual(actual_die, expected_die)
    
    def test_chose_all_dice(self) -> None:
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        testcase: list[dice_face_value] = [2 for _ in range(8)]
        dice.no_rng_roll(testcase)
        dice.select_face_of_dice(2)
        expected_unselected: list[dice_face_value] = []
        expected_selected: list[dice_face_value] = [2 for _ in range(8)]

        for actual_die, expected_die in zip(dice.unselected_dice, expected_unselected):
            self.assertEqual(actual_die, expected_die)
        for actual_die, expected_die in zip(dice.selected_dice, expected_selected):
            self.assertEqual(actual_die, expected_die)

    def test_no_valid_dice(self) -> None:
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        testcase: list[dice_face_value] = [1,2,3,3,worm,3,4,2]
        dice.no_rng_roll(testcase)
        self.assertFalse(dice.select_face_of_dice(5))

    def test_chose_one_dice_second(self) -> None:
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        testcase: list[dice_face_value] = [1,2,5,3,worm,3,4,2]
        dice.no_rng_roll(testcase)
        dice.select_face_of_dice(5)
        testcase = [1,5,3,worm,3,4,2]
        dice.no_rng_roll(testcase)
        dice.select_face_of_dice(3)
        expected_unselected: list[dice_face_value] = [1,5,worm,4,2]
        expected_selected: list[dice_face_value] = [5,3,3]

        for actual_die, expected_die in zip(dice.unselected_dice, expected_unselected):
            self.assertEqual(actual_die, expected_die)
        for actual_die, expected_die in zip(dice.selected_dice, expected_selected):
            self.assertEqual(actual_die, expected_die)
    
    def test_chose_multiple_dice_second(self) -> None:
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        testcase: list[dice_face_value] = [1,2,5,3,worm,3,4,2]
        dice.no_rng_roll(testcase)
        dice.select_face_of_dice(2)
        testcase = [2,5,3,worm,3,2]
        dice.no_rng_roll(testcase)
        dice.select_face_of_dice(3)
        expected_unselected: list[dice_face_value] = [2,5,worm,2]
        expected_selected: list[dice_face_value] = [2,2,3,3]

        for actual_die, expected_die in zip(dice.unselected_dice, expected_unselected):
            self.assertEqual(actual_die, expected_die)
        for actual_die, expected_die in zip(dice.selected_dice, expected_selected):
            self.assertEqual(actual_die, expected_die)
    
    def test_chose_all_dice_second(self) -> None:
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        testcase: list[dice_face_value] = [1,2,5,3,worm,3,4,2]
        dice.no_rng_roll(testcase)
        dice.select_face_of_dice(3)
        testcase = [2,2,2,2,2,2]
        dice.no_rng_roll(testcase)
        dice.select_face_of_dice(2)
        expected_unselected: list[dice_face_value] = []
        expected_selected: list[dice_face_value] = [3,3,2,2,2,2,2,2]

        for actual_die, expected_die in zip(dice.unselected_dice, expected_unselected):
            self.assertEqual(actual_die, expected_die)
        for actual_die, expected_die in zip(dice.selected_dice, expected_selected):
            self.assertEqual(actual_die, expected_die)


    def test_no_repeat(self) -> None:
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        testcase: list[dice_face_value] = [1,2,5,3,worm,3,4,2]
        dice.no_rng_roll(testcase)
        dice.select_face_of_dice(3)
        testcase = [2,worm,5,3,2,1]
        dice.no_rng_roll(testcase)
        self.assertFalse(dice.select_face_of_dice(3))


class TestNoRNGRoll(unittest.TestCase):
    def test_sanity_check(self) -> None:
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        dice.roll_dice()
        testcase: list[dice_face_value] = [1,2,5,3,worm,3,4,2]
        dice.no_rng_roll(testcase)
        for die, setvalue in zip(dice.unselected_dice, testcase):
            self.assertEqual(die, setvalue)
    
    def test_multiple_uses(self) -> None: 
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        testcase: list[dice_face_value] = [1,2,5,3,worm,3,4,2]
        dice.no_rng_roll(testcase)
        dice.select_face_of_dice(2)
        testcase = [2,3,worm,3,4,2]
        dice.no_rng_roll(testcase)
        for die, setvalue in zip(dice.unselected_dice, testcase):
            self.assertEqual(die, setvalue)


    def test_too_few_7(self) -> None:
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        dice.roll_dice()
        testcase: list[dice_face_value] = [1,2,worm,3,3,4,2]
        with self.assertRaises(Exception):
            dice.no_rng_roll(testcase)

    def test_too_few_6(self) -> None:
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        testcase: list[dice_face_value] = [1,4,5,3,worm,3,4,2]
        dice.select_face_of_dice(2)
        testcase = [1,2,3,worm,4,2]
        with self.assertRaises(Exception):
            dice.no_rng_roll(testcase)
    

    def test_too_many_9(self) -> None:
        worm: str = "\U0001FAB1"
        dice: Dice = Dice()
        dice.roll_dice()
        testcase: list[dice_face_value] = [1,2,5,3,worm, worm,3,4,2]
        with self.assertRaises(Exception):
            dice.no_rng_roll(testcase)
    

