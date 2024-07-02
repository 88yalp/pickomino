from functools import cache
from itertools import product
from multiprocessing import Pool
from time import perf_counter
from Dice import Dice
from Game import Game
from Player import Player
from typing import Iterator, Tuple
from Tile import Tile


class CPU(Player):

    def select_dice(self, game: Game, dice: Dice) -> tuple[int, bool]:
        score_dict: dict = self.calculate_conversion_dice_score_to_worms(game)
        possible_choices: set[int] = self.find_possible_choices(dice)

        max_expected_delta_worms: float = float("-inf")
        choice: int = 0
        for possible_choice in possible_choices:
            count: int = dice.unselected_dice.count(possible_choice)
            score_gained: int = 5 * count if possible_choice == 6 else possible_choice * count

            new_score: int = dice.get_score() + score_gained
            used_dice_faces: frozenset[int] = frozenset(
                {*dice.selected_dice, possible_choice})
            dice_left: int = len(dice.unselected_dice) - count
            with Pool() as pool:
                results: list[Tuple[int, float]] = pool.starmap(
                    self.p, self.probability_args_generator(new_score, used_dice_faces, dice_left))

            added_score: int
            probability: float
            expected_delta_worms: float = 0
            # print(f"for a choice of {count} {possible_choice}s")
            for added_score, probability in results:
                # print(f"new score: {new_score + added_score}, with probability: {probability}")
                expected_delta_worms += score_dict.get(
                    new_score + added_score, 0) * probability

            print(
                f"expected delta worms is {expected_delta_worms} with a choice of {count} {possible_choice}.")

            if max_expected_delta_worms < expected_delta_worms:
                max_expected_delta_worms = expected_delta_worms
                choice = possible_choice

        count = dice.unselected_dice.count(choice)
        score_gained = 5 * count if choice == 6 else choice * count
        new_score = dice.get_score() + score_gained

        re_roll: bool = score_dict.get(new_score, 0) < max_expected_delta_worms

        print(
            f"max expected delta worms is {max_expected_delta_worms} with a choice of {count} {choice}. Change if stop now is {score_dict.get(new_score, 0)}, Therefor {'reroll' if re_roll else 'end'}")
        return (choice, re_roll)

    def probability_args_generator(self, new_score: int, used_dice_faces: frozenset[int], dice_left: int) -> Iterator[Tuple[int, frozenset, int]]:
        for i in range(1, 41 - new_score):
            yield (i, used_dice_faces, dice_left)

    def find_possible_choices(self, dice: Dice) -> set[int]:
        possible_choices: set[int] = set()

        for die in dice.unselected_dice:
            if die not in dice.selected_dice:
                possible_choices.add(die)

        return possible_choices

    def calculate_conversion_dice_score_to_worms(self, game: Game) -> dict[int, int]:

        tile: Tile | None = self.get_top_tile()
        if isinstance(tile, Tile):
            loss: int = tile.worms
        else:
            loss = 0
        dice_score_to_worms: dict[int, int] = {i: -loss for i in range(0, 21)}

        for tile in game.board_tiles:
            if not tile.is_turned:
                dice_score_to_worms[tile.dice_score] = tile.worms

        for dice_score in range(21, 41):
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
            tile: Tile | None = player.get_top_tile()
            if isinstance(tile, Tile):
                if tile.dice_score == dice_sum:
                    print(f"{self.name} tok tile {tile} from {player.name}")
                    self.acquire_tile(player.remove_top_tile())
                    return None

        possible_choices: list[int] = game.valid_choices_from_board(dice_sum)
        possible_choices.sort(reverse=True)
        tile_from_board: Tile = game.remove_tile(possible_choices[0])
        print(f"{self.name} tok tile: {tile_from_board}")
        self.acquire_tile(tile_from_board)

    def player_turn(self, game: Game) -> None:
        print(f"{self.name}'s turn")
        dice_sum: int = self.roll_dice(game)

        if game.can_take_tile(dice_sum, self):
            self.choose_tile_to_take(game, dice_sum)
        else:
            game.handle_not_able_to_take_tile(self)

    def roll_dice(self, game: Game) -> int:
        print(game)
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
    def p(target: int, used: frozenset, dices: int) -> Tuple[int, float]:
        # idea: return 0 if it is not possible to reach the target (i.e have target of 35, and have used 2 die)
        if target == 0:
            return target, 1
        if target < 0 or dices == 0 or len(used) == 6:
            return target, 0
        # print(target, used, dices)
        s: float = 0
        c: int = 0
        for throw in product(*(dices * [[1, 2, 3, 4, 5, 6]])):
            m: float = 0
            c += 1
            for i in range(1, 7):
                if i in used:
                    continue
                selected = throw.count(i)
                if selected == 0:
                    continue
                score: int = 5 if i == 6 else i
                new_target: int = target - selected * score
                pc: float
                _, pc = CPU.p(new_target, frozenset(
                    {*used, i}), dices - selected)
                # print(i, selected, pc, new_target, throw)
                m = max(m, pc)
            s += m
        return (target, s / c)


if __name__ == "__main__":

    def probability_args_generator() -> Iterator[Tuple[int, frozenset, int]]:
        for i in range(1, 41):
            yield (i, frozenset(), 8)

    time_start: float = perf_counter()

    with Pool() as pool:
        results: list[Tuple[int, float]] = pool.starmap(
            CPU.p, probability_args_generator())

    time_end: float = perf_counter()
    # calculate the duration
    time_duration: float = time_end - time_start
    # report the duration
    print(f'Took {time_duration:.3f} seconds')
    total_prop: float = 0
    for target, probability in results:
        total_prop += probability
        print(f"{target}   {probability}")

    print(f"{total_prop=}")
