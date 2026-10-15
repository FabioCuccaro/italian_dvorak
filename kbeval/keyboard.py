"""Physical keyboard model: key positions, fingers, hands and travel distance.

Keys are addressed as (row, col):

    row -1  number row   (col 0 = the "1" key, col 10 = Minus, col 11 = Equal)
    row  0  top row      (col 0 = Q on QWERTY, col 10/11 = the two bracket keys)
    row  1  home row     (col 0 = A on QWERTY, col 9 = Semicolon, col 10 = Quote,
                          col 11 = the ISO key left of Enter)
    row  2  bottom row   (col 0 = Z on QWERTY, col 9 = Slash)

Columns 0-9 follow standard touch typing. Columns 10 and 11 are extra keys
reached by the right pinky. Horizontal positions use the usual row stagger of a
row-staggered (ANSI/ISO) board, measured in key widths ("u") relative to the
home row: number -0.75, top -0.25, home 0, bottom +0.5.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

ROWS = {"number": -1, "top": 0, "home": 1, "bottom": 2}
ROW_NAMES = {v: k for k, v in ROWS.items()}
ROW_STAGGER = {-1: -0.75, 0: -0.25, 1: 0.0, 2: 0.5}
MAX_COL = {-1: 11, 0: 11, 1: 11, 2: 9}

FINGERS = ["LP", "LR", "LM", "LI", "RI", "RM", "RR", "RP"]
FINGER_NAMES = {
    "LP": "left pinky", "LR": "left ring", "LM": "left middle", "LI": "left index",
    "RI": "right index", "RM": "right middle", "RR": "right ring", "RP": "right pinky",
}
COL_FINGER = ["LP", "LR", "LM", "LI", "LI", "RI", "RI", "RM", "RR", "RP", "RP", "RP"]
HOME_COL = {"LP": 0, "LR": 1, "LM": 2, "LI": 3, "RI": 6, "RM": 7, "RR": 8, "RP": 9}

# Position of each finger along its hand, from the outside in. A same-hand
# bigram is an *inward* roll when this rank increases (towards the index
# finger) and an *outward* roll when it decreases. This is the usual
# definition: on QWERTY, "as" and "lk" are inward, "sa" and "kl" are outward.
FINGER_RANK = {"LP": 0, "LR": 1, "LM": 2, "LI": 3, "RP": 0, "RR": 1, "RM": 2, "RI": 3}


@dataclass(frozen=True)
class Key:
    row: int
    col: int

    def __post_init__(self):
        if self.row not in ROW_STAGGER:
            raise ValueError(f"unknown row {self.row}")
        if not 0 <= self.col <= MAX_COL[self.row]:
            raise ValueError(f"column {self.col} out of range for row {self.row}")

    @property
    def finger(self) -> str:
        return COL_FINGER[self.col]

    @property
    def hand(self) -> str:
        return self.finger[0]

    @property
    def row_name(self) -> str:
        return ROW_NAMES[self.row]

    @property
    def x(self) -> float:
        return self.col + ROW_STAGGER[self.row]

    @property
    def distance(self) -> float:
        """Travel from the finger's home key, in key widths."""
        home_x = HOME_COL[self.finger]
        return math.hypot(self.x - home_x, self.row - 1)

    def __str__(self) -> str:
        return f"{self.row_name}:{self.col}"


def parse_key(spec: str) -> Key:
    """Parse "home:10" style key addresses."""
    row, col = spec.split(":")
    return Key(ROWS[row], int(col))


def roll_direction(a: Key, b: Key) -> str | None:
    """'inward' or 'outward' for a same-hand, different-finger bigram, else None."""
    if a.hand != b.hand or a.finger == b.finger:
        return None
    return "inward" if FINGER_RANK[b.finger] > FINGER_RANK[a.finger] else "outward"
