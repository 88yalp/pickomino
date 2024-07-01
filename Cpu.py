from functools import cache
from itertools import product
from multiprocessing import Pool
from time import perf_counter
from Dice import Dice
from Game import Game
from Player import Player
from typing import Iterable, Union, Tuple
from Tile import Tile




class CPU(Player):
    
    def select_dice(self, game: Game, dice: Dice) -> tuple[int, bool]:
        score_dict: dict = self.calculate_conversion_dice_score_to_worms(game)
        possible_choices: list[int] = self.find_possible_choices(dice)

        max_expected_delta_worms: float = -10 #will be updated, needed to be lower then the minimum expected value
        choice: int = 0
        for possible_choice in set(possible_choices):
            count: int = dice.unselected_dice.count(possible_choice)
            score_gained: int = 5 * count if possible_choice == 6 else possible_choice * count

            for i in range(1,41 - dice.get_score() - score_gained):
                probability: float
                _, probability = self.p(i,used = frozenset({*dice.selected_dice, possible_choice}), dices = len(dice.unselected_dice) - count)
                expected_delta_worms: float = score_dict.get(i, 0) * probability
                if max_expected_delta_worms <= expected_delta_worms:
                    max_expected_delta_worms = expected_delta_worms
                    choice = possible_choice
                    
        print(max_expected_delta_worms)
        count = dice.unselected_dice.count(choice)
        score_gained: int = 5 * count if choice == 6 else choice * count
        new_score: int = dice.get_score() + score_gained

        re_roll: bool = score_dict.get(new_score, 0) < max_expected_delta_worms

        return (choice, re_roll)
    
    
    def find_possible_choices(self, dice: Dice) -> list[int]:
        possible_choices: list[int] = []

        for die in dice.unselected_dice:
            if self.is_possible_choices(possible_choices, dice, die):
                possible_choices.append(die)
        
        return possible_choices
    
    
    def is_possible_choices(self, possible_choices: list[int], dice: Dice, die: int) -> bool:
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
            choice: int
            (choice, roll_again) = self.select_dice(game, dice)
            dice.select_face_of_dice(choice)
        return dice.get_score()


    @staticmethod
    @cache
    def p(target: int, used = None, dices: int = 8) -> Tuple[int, float]  :
        # idea: return 0 if it is not possible to reach the target (i.e have target of 35, and have used 2 die)
        if used is None:
            used = {}
        if target == 0:
            return target, 1
        if target < 0 or dices == 0 or len(used) == 6:
            return target, 0
        # print(target, used, dices)
        s: float = 0
        c :int = 0
        for throw in product(*(dices * [[1, 2, 3, 4, 5, 6]])):
            m :float = 0
            c += 1
            for i in range(1, 7):
                if i in used:
                    continue
                selected = throw.count(i)
                if selected == 0:
                    continue
                score: int = 5 if i == 6 else i
                new_target: int = target - selected * score
                pc : float
                _, pc = CPU.p(new_target, frozenset({*used, i}), dices - selected)
                # print(i, selected, pc, new_target, throw)
                m = max(m, pc)
            s += m
        return (target, s / c)


if __name__ == "__main__":

    time_start = perf_counter()

    with Pool() as pool:
        results = pool.map(CPU.p, (i for i in range(1, 41)))
    
        for target, probability in results:
            print(f"{target}   {probability}")

    
    time_end = perf_counter()
    # calculate the duration
    time_duration = time_end - time_start
    # report the duration
    print(f'Took {time_duration:.3f} seconds')