from Dice import Dice
from Game import Game
from Player import Player
from Tile import Tile


class HumanPlayer(Player):
    def choose_tile_to_take(self, game: Game, dice_sum: int) -> None:
        print(game)
        print(f"you rolled {dice_sum}, choose a tile to take")
    
        choice: int = int(input())
        while choice not in game.valid_choices(dice_sum, self):
            print(f"{choice} is not a valid choice. Please choose a valid choice")
            choice = int(input())
        
        if choice in game.valid_choices_from_board(dice_sum):
            self.acquire_tile(game.remove_tile(choice))
            return
        
        for player in game.players:
            tile: Tile|None = player.get_top_tile()
            if isinstance(tile, Tile):
                if tile.dice_score == choice:
                    self.acquire_tile(player.remove_top_tile())

    def player_turn(self, game: Game) -> None:
        dice_sum: int = self.determine_dice_sum(game)

        if game.can_take_tile(dice_sum, self):
            self.choose_tile_to_take(game, dice_sum)
        else:
            print(f"Your score is {dice_sum}, You cant take a tile with this score")
            game.handle_not_able_to_take_tile(self)

    def determine_dice_sum(self, game: Game) -> int:
        """ Does the dice rolling part of a players turn, and returns the sum 
    
        Args:
            player (Player): The player whos turn it is
    
        Returns:
            int: the sum of the dice the player have selected this turn.
    
        Author:
            Magnus Rein
        """
        print(f"{self.name}'s turn")
        dice: Dice = Dice()
        while True:
            print(game)
            dice.roll_dice()
            print(dice)
            if not dice.have_valid_choice():
                print("No valid choice, you lose your turn")
                return 0
            while not dice.select_face_of_dice(input("select a set of dice to keep (w for worm(s)): ")):
                pass
            print(dice)
            answer: str = input("roll again (y/n)")
            while answer not in ["y", "n"]:
                print(f"{answer} is not a valid choice, please choose a valid choice")
                answer = input("roll again (y/n)")
            if answer == "n":
                return dice.get_score()