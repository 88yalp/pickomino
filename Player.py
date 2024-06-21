from __future__ import annotations
from typing import TYPE_CHECKING
from Tile import Tile

if TYPE_CHECKING:
    from Game import Game
    


class Player:

    def __init__(self, name: str ) -> None:
        """ Makes a new player with a name.
        
        Args:
            name (str): The name of the new player.
        """
        # Tested: False
        self.name: str = name
        self.tiles: list[Tile] = []

    
    def calculate_score(self) -> int:
        """Calculates the score for the player.

        Returns:
            int: the score of the player.

        Author:
            Magnus Rein
        """
        # Tested: False
        score: int = 0
        for tile in self.tiles:
            score += tile.worms
        return score

    def acquire_tile(self, tile:Tile) -> None:
        """acquires the given tile.

        Args:
            tile (Tile): The tile that is acquired.
        
        Author:
            Magnus Rein
        """
        # Tested: False
        self.tiles.append(tile)
    
    def get_top_tile(self) -> Tile | None:
        """ Gets the top tile 

        Returns:
            Tile: the tile on top of the pile. 
        
        Author:
            Magnus Rein
        """
        if len(self.tiles) == 0:
            return None
        return self.tiles[-1]
    
    def remove_top_tile(self) -> Tile:
        """removes the top tile, and then returns it.

        Returns:
            Tile: The tile that is retuned.
        
        Author:
            Magnus Rein
        """
        # Tested: False
        return self.tiles.pop()

    def __str__(self) -> str:
        """ Makes a string representation of a player

        Returns:
            str: The string representation of the tile

        Author:
            Magnus Rein
        """
        if len(self.tiles) == 0:
            return f"{' '*4}Name: {self.name} \n{' '*8}Number of tiles: 0 \n"
        return f"{' '*4}Name: {self.name} \n{' '*8}Number of tiles: {len(self.tiles)} \n{' '*8}Top tile: {self.tiles[-1]} \n"
    
    def player_turn(self, game: Game) -> None:
        print("feil")