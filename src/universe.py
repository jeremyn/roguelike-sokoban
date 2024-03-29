"""
Copyright Jeremy Nation <jeremy@jeremynation.me>.
Licensed under the GNU General Public License (GPL) v3.

"""
from enum import Enum
from typing import Literal, Optional, Sequence, TypedDict, Union

from src.levelloader import Symbols
from src.util import Action, RoguelikeSokobanError


class _MoveTestItem(TypedDict):
    axis: Literal["y", "x"]
    change: Literal[-1, 1]


_MOVE_TEST: dict[Action, _MoveTestItem] = {
    Action.UP: {"axis": "y", "change": -1},
    Action.DOWN: {"axis": "y", "change": 1},
    Action.LEFT: {"axis": "x", "change": -1},
    Action.RIGHT: {"axis": "x", "change": 1},
}


class _MoveMode(Enum):
    DO_MOVE = "do move"
    DRY_RUN = "dry run"


class _Movable:
    """Represents items that can move."""

    _SYMBOL_LOOKUP: str

    def __init__(self, start_y: int, start_x: int, level_sym: Symbols):
        self.curr_y = start_y
        self.curr_x = start_x
        self.level_sym = level_sym
        # things that the player can walk over
        self.walkable = [self.level_sym["floor"]]
        # things that a boulder can be pushed over or into
        self.pushable = self.walkable[:]
        self.pushable.append(self.level_sym["pit"])
        try:
            self.symbol = self.level_sym[self._SYMBOL_LOOKUP]
        except KeyError as exc:
            raise RoguelikeSokobanError(
                f"Unexpected _SYMBOL_LOOKUP: '{self._SYMBOL_LOOKUP}'"
            ) from exc

    def _move(
        self, move_dir: Action, univ: "Universe", mode: Optional[_MoveMode] = None
    ) -> Union[str, "_Boulder"]:
        """Handle movement math for subclasses.

        Return new grid coords for movement target (destination), or if DRY_RUN and the
        target is a boulder, return the boulder object.

        """
        axis = _MOVE_TEST[move_dir]["axis"]
        change = _MOVE_TEST[move_dir]["change"]
        if axis == "y":
            target_y = self.curr_y + change
            target_x = self.curr_x
        elif axis == "x":
            target_y = self.curr_y
            target_x = self.curr_x + change
        else:
            raise RoguelikeSokobanError(f"Unexpected direction: {axis}")

        if mode == _MoveMode.DO_MOVE:
            self.curr_y = target_y
            self.curr_x = target_x
            return univ.level_map[self.curr_y][self.curr_x]

        if mode == _MoveMode.DRY_RUN:
            for boulder in univ.boulders:
                if boulder.curr_y == target_y and boulder.curr_x == target_x:
                    return boulder
            return univ.level_map[target_y][target_x]

        raise RoguelikeSokobanError(f"Unexpected move mode: {mode}")


class _Boulder(_Movable):
    """Represents boulders."""

    _SYMBOL_LOOKUP = "boulder"

    def move(self, move_dir: Action, univ: "Universe") -> Union[str, "_Boulder"]:
        """Check if boulder can move, and if so, move it and update universe."""
        mov = super()._move(move_dir, univ, _MoveMode.DRY_RUN)
        if mov in self.pushable:
            super()._move(move_dir, univ, _MoveMode.DO_MOVE)
            if mov == self.level_sym["pit"]:
                univ.level_map[self.curr_y][self.curr_x] = self.level_sym["floor"]
                univ.pits_remaining -= 1
        return mov


class _Player(_Movable):
    """Represents the player."""

    _SYMBOL_LOOKUP = "player"

    def move(self, move_dir: Action, univ: "Universe") -> None:
        """Check if player can move, and if so, move them and update universe."""
        player_move_result = super()._move(move_dir, univ, _MoveMode.DRY_RUN)
        if player_move_result in self.walkable:
            super()._move(move_dir, univ, _MoveMode.DO_MOVE)
            univ.moves_taken += 1
        if isinstance(player_move_result, _Boulder):
            boulder_move_sq = player_move_result.move(move_dir, univ)
            if boulder_move_sq in self.pushable:
                super()._move(move_dir, univ, _MoveMode.DO_MOVE)
                univ.moves_taken += 1
                if boulder_move_sq == self.level_sym["pit"]:
                    univ.boulders.remove(player_move_result)


class Universe:
    """Represents the game universe."""

    def __init__(
        self, level_name: str, level_map: Sequence[str], level_sym: Symbols
    ) -> None:
        self.level_map = [list(line) for line in level_map]
        self.level_name = level_name
        self.level_sym = level_sym
        self.boulders: list[_Boulder] = []
        self.pits_remaining = 0
        self.moves_taken = 0
        for row_index, row in enumerate(self.level_map):
            for col_index, square in enumerate(row):
                if square == self.level_sym["player"]:
                    self.player = _Player(
                        row_index,
                        col_index,
                        self.level_sym,
                    )
                    self.level_map[row_index][col_index] = self.level_sym["floor"]
                if square == self.level_sym["boulder"]:
                    self.boulders.append(
                        _Boulder(row_index, col_index, self.level_sym),
                    )
                    self.level_map[row_index][col_index] = self.level_sym["floor"]
                if square == self.level_sym["pit"]:
                    self.pits_remaining += 1
        self.game_won = False

    def eval_action(self, act: Action) -> None:
        """Move the player and see if they win."""
        move_dir = act
        self.player.move(move_dir, self)
        self.game_won = self.pits_remaining == 0
