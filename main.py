from Cpu import CPU
from Game import Game
from Player import Player
from HumanPlayer import HumanPlayer
from typing import Union



def startup() -> Game:
    """ Starts the game and adds the players.

    Returns:
        Game: the game that is started

    Author:
        Magnus Rein
    """
    number_of_players = 0
    game: Game = Game()
    answer: str = input("add players? (y/n)")
    while answer != "n":
        game.add_player(HumanPlayer(input("Next player ")))
        number_of_players += 1
        answer = input("add more players? (y/n)")
    # answer = input("add CPU? (y/n)")
    # while answer != "n":
    #     game.add_player(CPU(input("Next CPU ")))
    #     number_of_players += 1
    #     answer = input("add more CPUs? (y/n)")
    if number_of_players < 2:
        print("Need at least 2 player")
        exit()
    game.setup()
    return game


def main() -> None:
    """ Main loop of the game.

    Author:
        Magnus Rein
    """
    game: Game = startup()

    while game.is_active():
        current_player: Player = game.next_player()
        current_player.player_turn(game)

    game.print_scoreboard()

if __name__ == "__main__":
    main()
