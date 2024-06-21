from Dice import Dice
from Game import Game
from Player import Player
from typing import Union
from Tile import Tile


dice_face_value = Union[int, str]


class CPU(Player):
    
    def select_dice(self, game: Game, dice: Dice) -> tuple[dice_face_value, bool]:
        score_dict: dict = self.calculate_conversion_dice_score_to_worms(game)
        possible_choices: list[dice_face_value] = self.find_possible_choices(dice)

        return(possible_choices[0],False)
    
    
    def find_possible_choices(self, dice: Dice) -> list[dice_face_value]:
        possible_choices: list[dice_face_value] = []

        for die in dice.unselected_dice:
            if self.is_possible_choices(possible_choices, dice, die):
                possible_choices.append(die)
        
        return possible_choices
    
    
    def is_possible_choices(self, possible_choices: list[dice_face_value], dice: Dice, die: dice_face_value) -> bool:
        if die in dice.selected_dice:
            return False
        if die in possible_choices:
            return False
        return True


    def calculate_conversion_dice_score_to_worms(self, game: Game) -> dict[int, int]:
        
        tile: Tile|None = self.get_top_tile()
        if isinstance(tile, Tile):
            loss: int = tile.worms
        else:
            loss = 0
        dice_score_to_worms: dict[int, int] = { i:-loss for i in range(0,21)}

        for tile in game.board_tiles:
            if not tile.is_turned:
                dice_score_to_worms[tile.dice_score] = tile.worms
    
        for dice_score in range(21,41):
            if dice_score not in dice_score_to_worms.keys():
                dice_score_to_worms[dice_score] = dice_score_to_worms[dice_score - 1]

        for player in game.players:
            if player is self:
                continue
            tile = player.get_top_tile()
            if isinstance(tile, Tile):
                dice_score_to_worms[tile.dice_score] = tile.worms
        
        return dice_score_to_worms
    
    def choose_tile_to_take(self, game: Game, dice_sum: int) -> None:
        for player in game.players:
            if player is self:
                continue
            tile: Tile|None = player.get_top_tile()
            if isinstance(tile, Tile):
                if tile.dice_score == dice_sum:
                    self.acquire_tile(player.remove_top_tile())
                    return None

        possible_choices: list[int] = game.valid_choices_from_board(dice_sum)
        possible_choices.sort(reverse=True)
        self.acquire_tile(game.remove_tile(possible_choices[0]))

    
    def player_turn(self, game: Game) -> None:
        dice_sum: int = self.roll_dice(game)

        if game.can_take_tile(dice_sum, self):
            self.choose_tile_to_take(game, dice_sum)
        else:
            game.handle_not_able_to_take_tile(self)
    

    def roll_dice(self, game: Game) -> int:
        dice: Dice = Dice()
        roll_again: bool = True
        while roll_again:
            dice.roll_dice()
            print(dice)
            if not dice.have_valid_choice():
                return 0
            choice: dice_face_value
            (choice, roll_again) = self.select_dice(game, dice)
            dice.select_face_of_dice(choice)
        return dice.get_score()
    

if __name__ == "__main__":
    pass