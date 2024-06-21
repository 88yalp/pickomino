import random
from typing import Union

dice_face_value = Union[int, str]

class Dice:

    def __init__(self) -> None:
        self.selected_dice: list[dice_face_value] = []
        self.unselected_dice: list[dice_face_value] = [0 for _ in range(8)]
        self.worm: str = "\U0001FAB1"
    
    def __str__(self) -> str:
        """ Makes a string representation of the Dice

        Format: Sum now: (the sum of the chosen dice). Chosen dice: (list of the chosen dice). Rolled dice: (list of th rolled dice)

        Returns:
            str: The sting representation of the Dice. 
        
        Author:
            Magnus Rein
        """
        return f"Sum now: {self.get_score()}. Chosen dice: {self.selected_dice}. Rolled dice: {self.unselected_dice}"

    def roll_dice(self) -> None:
        """ Rolls the unselected dices

        Author:
            Magnus Rein
        """
        for index, _ in enumerate(self.unselected_dice):
            die: Union[int, str] = random.randint(1,6)
            self.unselected_dice[index] = die
        self.unselected_dice.sort()

        for index, die in enumerate(self.unselected_dice):
            if die == 6:
                die = self.worm
            self.unselected_dice[index] = die

    def select_face_of_dice(self, choice: dice_face_value) -> bool:
        """ Selects one of faces of the dices 

        Selects one of the faces of the rolled dice, and adds those dice to the selected dices. 

        Args:
            choice (Union[int, str]): The choice that has been made (1,2,3,4,5,w)

        Returns:
            bool: Returns True for a valid choice of face, else False

        Author:
            Magnus Rein
        """
        # Tested: True
        if choice == "w":
            choice = self.worm
        else:
            choice = int(choice)
        if not self.is_valid_choice(choice):
            print(f"{choice} is not a valid choice, pleas select a valid choice")
            return False

        for index in range(len(self.unselected_dice) - 1, -1, -1):
            if self.unselected_dice[index] == choice:
                self.selected_dice.append(self.unselected_dice.pop(index)) 
        
        return True

    def is_valid_choice(self, choice: dice_face_value) -> bool:
        """ Checks if the given choice is a valid choice

        Args:
            choice (dice_face_value): The choice that has been made

        Returns:
            bool: True if choice is a valid choice, else False

        Author:
            Magnus Rein
        """
        if choice in self.unselected_dice and choice not in self.selected_dice:
            return True
        return False
        

    def get_score(self) -> int:
        """ Gets the sum of the selected dice

        Returns:
            int: the sum of the selected dice
        
        Author:
            Magnus Rein
        """
        score: int = 0
        for die in self.selected_dice:
            score += self.get_value(die)
        return score
    
    def get_value(self, symbol: dice_face_value) -> int:
        """ gets the value of a symbol 

        Args:
            symbol (dice_face_value): what gets determined the value of 

        Returns:
            int: the value of the symbol
        
        Author:
            Magnus Rein
        """
        if isinstance(symbol, str):
            return 5
        else:
            return symbol

    def have_valid_choice(self) -> bool:
        """ Checks if there is a valid choice of dice

        Returns:
            bool: True if there is a valid choice, else False
        
        Author:
            Magnus Rein
        """
        for die in self.unselected_dice:
            if die not in self.selected_dice:
                return True
        return False

    def no_rng_roll(self, rolled: list[dice_face_value]) -> None:
        """ For Writing tests, rolls dice without rng

        Args:
            rolled (list[dice_face_value]): The new values of the unselected dice

        Raises:
            Exception: raised if the number of new values is different the the number of old values
        
        Author:
            Magnus Rein
        """
        # Tested: True
        if len(rolled) != len(self.unselected_dice):
            raise Exception("the number of predetermined dice is wrong, need to match number of unselected dice")
        for index, value in enumerate(rolled):
            self.unselected_dice[index] = value

if __name__ == "__main__":
    dice: Dice = Dice()
    dice.roll_dice()
    while dice.have_valid_choice():
        print(dice)
        while not dice.select_face_of_dice(input("select a set of dice to keep (w for worm): ")):
            pass
        dice.roll_dice()
    