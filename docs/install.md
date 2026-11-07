# Installing Italian Dvorak

[Italiano](install.it.md)

> v2 is a candidate. Try it, and open an issue with anything that feels wrong.

## The full keymap

```
 \ 1 2 3 4 5 6 7 8 9 0 ' ì
    K F ' Q È B D S M J X +
     U E I A O C T L N R ◌ ù
  < W Z Y . , P G V H -
```

| Key | Shift | AltGr | Shift+AltGr |
|---|---|---|---|
| `'` (third key, top row) | `?` | `€` | |
| `è` | `é` | | |
| `x` | `X` | `[` | `{` |
| `+` | `*` | `]` | `}` |
| `r` | `R` | `@` | |
| `◌` dead key | acute dead key | `#` | |
| `.` | `:` | | |
| `,` | `;` | | |
| `-` | `_` | | |

- **Accents:** è has its own key, and Shift + è gives é. à ì ò ù use the dead key ◌: press ◌, then the
  vowel. For an acute accent, press Shift + ◌, then the vowel. For a capital, press ◌, then Shift + the
  vowel (È, À, …). ì and ù also keep their own keys from the Italian layout.
- **Digits and symbols** stay where they are on the Italian keyboard, including AltGr + ò position = @
  and AltGr + à position = #.
- The source of truth is [`keymaps/italian-dvorak-v2.json`](../keymaps/italian-dvorak-v2.json); the
  files in [`dist/`](../dist/) are generated from it with `python -m kbeval.export`.

## Linux (Wayland and X11)

The XKB file is [`dist/xkb/itdvorak`](../dist/xkb/itdvorak). Install it for your user:

```sh
mkdir -p ~/.config/xkb/symbols
cp dist/xkb/itdvorak ~/.config/xkb/symbols/
```

Then select it:

- **Hyprland** (`~/.config/hypr/hyprland.conf`):
  ```
  input {
      kb_layout = itdvorak
  }
  ```
- **Sway** (`~/.config/sway/config`): `input type:keyboard xkb_layout itdvorak`
- **X11** (current session only):
  ```sh
  setxkbmap -I ~/.config/xkb itdvorak -print | xkbcomp -I"$HOME/.config/xkb" - "$DISPLAY"
  ```

Compositors built on libxkbcommon 1.0 or later read `~/.config/xkb` by themselves. GNOME and KDE
show only the layouts registered in the system XKB rules (`evdev.xml`), so the layout does not appear
in their settings yet; instructions for registering it there are still to be written.

To go back, switch the layout to `it`.

**Tested:** the file compiles with `xkbcomp` and libxkbcommon, and a test reads back all 103
characters and dead keys from the compiled keymap. **Not yet tested** on a real desktop session.

## keybr (typing practice)

[`dist/keybr/it_dvorak_v2.json`](../dist/keybr/it_dvorak_v2.json) (with the dead key) and
[`it_dvorak_v2_simple.json`](../dist/keybr/it_dvorak_v2_simple.json) (without) are in keybr's
`importKeymap` format. The public keybr.com cannot import custom layouts, so a self-hosted keybr is
needed:

1. Copy the file to `packages/keybr-generators/layouts/`.
2. In `packages/keybr-generators/lib/generate-layouts.ts`, add
   `["it_dvorak", importKeymap("layouts/it_dvorak_v2.json")],` after the `it_it` line, then run
   `npm run generate-layouts` in `packages/keybr-generators`.
3. In `packages/keybr-keyboard/lib/layout.ts`, add an `IT_DVORAK` layout (family `dvorak`,
   `Language.IT`, with the ISO and ANSI geometries) and list it in `Layout.ALL`. Use `emulate: true`
   only with the simple file.

The v1 files passed keybr's layout generator; the v2 files use the same format but have not been run
through it yet.

## Windows and macOS

Not available yet. The keymap file has everything needed to generate a Windows `.klc` (Microsoft
Keyboard Layout Creator) or a macOS `.keylayout`.
