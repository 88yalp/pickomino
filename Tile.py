class Tile:

    def __init__(self, dice_score: int) -> None:
        """Makes a new tile.

        Makes a new tile with the dice_score, a number of worms, and unturned. 

        Args:
            dice_score (int): the dice_score of the tile. is used to determine the number of worms 
        Author:
            Magnus Rein
        """
        # Tested: False
        self.dice_score: int = dice_score
        self.worms: int = self.calculate_worms(dice_score)
        self.is_turned: bool = False

    def __str__(self) -> str:
        """ Makes a string representation of a tile 

        format is the " 25/2 " where 25 is the dice_score, and 2 is the number worms that it is worth. if it is turned, it returns " ■■/■ "

        Returns:
            str: the string representation of the tile. 
        
        Author:
            Magnus Rein
        """
        # Tested: False
        blank: str = "\u25A0"
        if self.is_turned:
            return f"  {2*blank}/{blank}"
        return f" {self.dice_score}/{self.worms} "

    def turn(self) -> bool:
        """ If possible turns the tile over. 

        The tile is only turnable if it has not been turned.

        Returns:
            bool: Specifying if the turning was successful

        Author:
            Magnus Rein
        """
        # Tested: True
        if self.is_turned:
            return False
        self.is_turned = True
        return True

    @staticmethod
    def calculate_worms(score: int) -> int:
        """ Calculates number of worms a tile is worth.

        Args:
            score (int): The diceScore of the tile. Should be in range(21,37)

        Raises:
            ValueError: Raised if the score is given is outside of the valid diceScores.

        Returns:
            int: the number of worms for the given score 

        Author:
            Magnus Rein
        """
        # Tested: True
        if score <= 20:
            raise ValueError(f"{score} is not a valid value for the diceScore of a tile. Must be natural number between 21 and 36, including endpoints")
        elif score <= 24:
            return 1
        elif score <= 28:
            return 2
        elif score <= 32:
            return 3
        elif score <= 36:
            return 4
        else:
            raise ValueError(f"{score} is not a valid value for the diceScore of a tile. Must be natural number between 21 and 36, including endpoints")

if __name__ == "__main__":
    pass

    