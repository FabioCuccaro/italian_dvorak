"""Layout definitions and the mapping from characters to keystrokes.

A layout is a JSON file:

    {
      "id": "v1",
      "name": "Italian-Dvorak v1",
      "description": "...",
      "rows": {"top": "gwqzymlchb", "home": "uaoeisntrd", "bottom": "'.xkjfpv,-"},
      "extra": {"è": "top:10"},
      "accents": {"method": "deadkey", "key": "home:10"}
    }

"rows" lists the characters on columns 0-9 of each row; "_" marks a key with
nothing relevant on it. "extra" places characters on any other key.

"accents" says how accented vowels that are not on a key of their own are typed:

  - "deadkey": a dead key ("key") then the base vowel. Grave accent unshifted,
    acute accent with Shift, as in the it_dvorak.json keybr file.
  - "altgr": AltGr + the base vowel; acute with AltGr + Shift.
  - "direct": no extra mechanism. As on the Italian keyboard, an acute vowel
    is Shift + the key of the grave vowel (é = Shift + è).
"""

from __future__ import annotations

import json
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from .keyboard import ROWS, Key, parse_key

LETTERS = set("abcdefghijklmnopqrstuvwxyz")
GRAVE = "̀"
ACUTE = "́"

# Modifier presses. They are counted as extra keystrokes but are not part of
# the positional key sequence used for row, finger and bigram metrics.
SHIFT = "Shift"
ALTGR = "AltGr"
DEAD = "DK"


@dataclass(frozen=True)
class Press:
    key: Key | None  # None for a modifier
    label: str  # character on the key, "DK" for the dead key, or the modifier name


@dataclass
class Layout:
    id: str
    name: str
    description: str
    keys: dict[str, Key]
    accent_method: str
    dead_key: Key | None = None
    source: str = ""
    _cache: dict[str, list[Press] | None] = field(default_factory=dict, repr=False)

    @property
    def labels(self) -> dict[Key, str]:
        out = {k: ch for ch, k in self.keys.items()}
        if self.dead_key:
            out[self.dead_key] = DEAD
        return out

    def presses(self, ch: str) -> list[Press] | None:
        """Keystrokes needed to type one lowercase character, or None if unmapped."""
        if ch not in self._cache:
            self._cache[ch] = self._resolve(ch)
        return self._cache[ch]

    def _resolve(self, ch: str) -> list[Press] | None:
        if ch in self.keys:
            return [Press(self.keys[ch], ch)]
        decomposed = unicodedata.normalize("NFD", ch)
        if len(decomposed) != 2 or decomposed[1] not in (GRAVE, ACUTE):
            return None
        base, accent = decomposed
        if base not in self.keys:
            return None
        base_press = Press(self.keys[base], base)
        shift = [Press(None, SHIFT)] if accent == ACUTE else []
        if self.accent_method == "deadkey":
            return shift + [Press(self.dead_key, DEAD), base_press]
        if self.accent_method == "altgr":
            return [Press(None, ALTGR)] + shift + [base_press]
        if self.accent_method == "direct" and accent == ACUTE:
            grave = unicodedata.normalize("NFC", base + GRAVE)
            if grave in self.keys:
                return [Press(None, SHIFT), Press(self.keys[grave], grave)]
        return None

    def letter_rows(self) -> list[str]:
        """Three 10-character strings (top, home, bottom) for display."""
        labels = self.labels
        out = []
        for row in (0, 1, 2):
            cells = []
            for col in range(10):
                label = labels.get(Key(row, col), "_")
                cells.append("◌" if label == DEAD else label)
            out.append("".join(cells))
        return out


def load_layout(path: Path) -> Layout:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    keys: dict[str, Key] = {}

    def place(ch: str, key: Key):
        if ch in keys:
            raise ValueError(f"{path}: '{ch}' is on two keys ({keys[ch]} and {key})")
        keys[ch] = key

    for row_name, chars in data["rows"].items():
        if len(chars) != 10:
            raise ValueError(f"{path}: row '{row_name}' must have 10 characters")
        for col, ch in enumerate(chars):
            if ch != "_":
                place(ch, Key(ROWS[row_name], col))
    for ch, spec in data.get("extra", {}).items():
        place(ch, parse_key(spec))

    missing = LETTERS - set(keys)
    if missing:
        raise ValueError(f"{path}: letters not on any key: {''.join(sorted(missing))}")

    accents = data.get("accents", {"method": "direct"})
    method = accents["method"]
    if method not in ("deadkey", "altgr", "direct"):
        raise ValueError(f"{path}: unknown accent method '{method}'")
    dead_key = parse_key(accents["key"]) if method == "deadkey" else None
    if dead_key and dead_key in keys.values():
        raise ValueError(f"{path}: dead key {dead_key} is also used by a character")

    return Layout(
        id=data["id"],
        name=data.get("name", data["id"]),
        description=data.get("description", ""),
        keys=keys,
        accent_method=method,
        dead_key=dead_key,
        source=data.get("source", ""),
    )


def load_layouts(directory: Path) -> list[Layout]:
    """Load every *.json file in a directory, in file name order."""
    layouts = [load_layout(p) for p in sorted(Path(directory).glob("*.json"))]
    ids = [lay.id for lay in layouts]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate layout ids")
    return layouts
