from Dice import Dice
from Player import Player
from Tile import Tile


class Game:
    def __init__(self) -> None:
        """Makes a new game

        Author:
            Magnus Rein
        """
        self.players: list[Player] = []
        self.board_tiles: list[Tile] = []
        self.current_player_index: int = 0

    def setup(self) -> None:
        """Does the basic setup

        Generates all the tiles, and adds them to the board tiles.

        Author:
            Magnus Rein
        """
        # Tested: True
        for dice_score in range(21, 37):
            self.board_tiles.append(Tile(dice_score))

    def __str__(self) -> str:
        """ Makes a readable string of the current state of the game

        Returns:
                str: the string representing the current state of the game

        Author:
            Magnus Rein
        """
        # Tested: False
        output: str = f"BordTiles:\n{' '*3}"
        for tile in self.board_tiles:
            output += f"{tile.__str__()}"
        output += "\nPlayers:\n"
        for player in self.players:
            output += f"{player.__str__()}"
        return output

    def add_player(self, new_player: Player) -> None:
        """ Adds a player to the game

        Args:
                new_player (Player): The player that is added to the game

        Author:
            Magnus Rein
        """
        # Tested: True
        self.players.append(new_player)

    def next_player(self) -> Player:
        """The player that is next to play. 

        Returns:
                Player: is the player that is next to play.

        Author:
            Magnus Rein
        """
        # Tested: True
        next_player: Player = self.players[self.current_player_index]
        self.current_player_index = (
            self.current_player_index + 1) % len(self.players)
        return next_player

    def is_active(self) -> bool:
        """Determines if the game is active or not.

        Returns:
                bool: Active game -> True, Not active game -> False

        Author:
            Magnus Rein
        """
        # Tested: True
        for tile in self.board_tiles:
            if not tile.is_turned:
                return True
        return False

    def highest_tile(self) -> Tile:
        """The highest tile on the board

        Raises:
                Exception: raised if there is no tile left on the board, but then the game should be over.

        Returns:
                Tile: the tile on the board that has the highest value.

        Author:
                Magnus Rein
        """
        for tile in reversed(self.board_tiles):
            if not tile.is_turned:
                return tile
        raise Exception("something went wrong")

    def lowest_tile(self) -> Tile:
        return self.board_tiles[0]

    def add_tile(self, tile: Tile) -> None:
        for index in range(len(self.board_tiles)):
            if self.board_tiles[index].dice_score > tile.dice_score:
                self.board_tiles.insert(index, tile)
                return None

    def remove_tile(self, dice_score: int) -> Tile:
        for tile in self.board_tiles:
            if tile.dice_score == dice_score:
                self.board_tiles.remove(tile)
                return tile

        raise Exception("tile with given dice_score is not in board_tiles")

    def print_scoreboard(self) -> None:
        scores: list[tuple[int, Player]] = [
            (player.calculate_score(), player) for player in self.players]

        scores = sorted(scores, key=lambda x: x[0], reverse=True)
        print("The game is over, the scores was:")
        for place, (score, player) in enumerate(scores):
            print(f"{place}.{player.name:20}{score}")

    def valid_choices_from_board(self, dice_sum: int) -> list[int]:
        choices: list[int] = []
        for tile in self.board_tiles:
            if (not tile.is_turned) and tile.dice_score <= dice_sum:
                choices.append(tile.dice_score)
        return choices

    def valid_choices_from_players(self, dice_sum: int, current_player: Player) -> list[int]:
        choices: list[int] = []
        for player in self.players:
            if player != current_player:
                tile: Tile | None = player.get_top_tile()
                if isinstance(tile, Tile):
                    if tile.dice_score == dice_sum:
                        choices.append(dice_sum)
        return choices

    def valid_choices(self, dice_sum: int, current_player: Player) -> list[int]:
        return self.valid_choices_from_board(dice_sum) + self.valid_choices_from_players(dice_sum, current_player)

    def can_take_tile(self, dice_sum: int, current_player: Player) -> bool:
        """ Determines if the given player can take a tile in the given game with the current dice

        Args:
            game (Game): The game that is being played
            dice_sum (int): The sum of the dices the player selected
            current_player (Player): Tests it this player can take the tile

        Returns:
            bool: Returns True if the player can take a tile, else False

        Author:
            Magnus Rein
        """
        if len(self.valid_choices(dice_sum, current_player)) == 0:
            return False
        return True

    def handle_not_able_to_take_tile(self, current_player: Player) -> None:
        """ handles what happens when the player cant take a tile

        returns the top tile of the player to the board if the player has a tile.
        if a tile is returned, turns the highest tile on the board unless this is the tile that got returned.

        Args:
            game (Game): The game that is being played
            current_player (Player): The player who cant take a tile

        Author:
            Magnus Rein
        """
        if len(current_player.tiles) == 0:
            return None
        tile_returned: Tile = current_player.remove_top_tile()
        self.add_tile(tile_returned)
        if not (tile_returned == self.highest_tile()):
            self.highest_tile().turn()
