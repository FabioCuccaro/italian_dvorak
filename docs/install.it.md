# Installare Italian Dvorak

[English](install.md)

> v2 è un candidato. Provala e apri una issue per tutto quello che non ti convince.

## La mappa completa

```
 \ 1 2 3 4 5 6 7 8 9 0 ' ì
    K F ' Q È B D S M J X +
     U E I A O C T L N R ◌ ù
  < W Z Y . , P G V H -
```

| Tasto | Shift | AltGr | Shift+AltGr |
|---|---|---|---|
| `'` (terzo tasto, riga alta) | `?` | `€` | |
| `è` | `é` | | |
| `x` | `X` | `[` | `{` |
| `+` | `*` | `]` | `}` |
| `r` | `R` | `@` | |
| `◌` tasto morto | tasto morto acuto | `#` | |
| `.` | `:` | | |
| `,` | `;` | | |
| `-` | `_` | | |

- **Accenti:** la è ha un tasto suo e Shift + è dà é. à ì ò ù usano il tasto morto ◌: premi ◌ e poi la
  vocale. Per l'accento acuto premi Shift + ◌ e poi la vocale. Per la maiuscola premi ◌ e poi
  Shift + la vocale (È, À, …). ì e ù mantengono anche i loro tasti della tastiera italiana.
- **Cifre e simboli** restano dove sono sulla tastiera italiana, compresi AltGr sul tasto della ò = @
  e AltGr sul tasto della à = #.
- Il riferimento è [`keymaps/italian-dvorak-v2.json`](../keymaps/italian-dvorak-v2.json); i file in
  [`dist/`](../dist/) si generano da lì con `python -m kbeval.export`.

## Linux (Wayland e X11)

Il file XKB è [`dist/xkb/itdvorak`](../dist/xkb/itdvorak). Installalo per il tuo utente:

```sh
mkdir -p ~/.config/xkb/symbols
cp dist/xkb/itdvorak ~/.config/xkb/symbols/
```

Poi selezionalo:

- **Hyprland** (`~/.config/hypr/hyprland.conf`):
  ```
  input {
      kb_layout = itdvorak
  }
  ```
- **Sway** (`~/.config/sway/config`): `input type:keyboard xkb_layout itdvorak`
- **X11** (solo per la sessione corrente):
  ```sh
  setxkbmap -I ~/.config/xkb itdvorak -print | xkbcomp -I"$HOME/.config/xkb" - "$DISPLAY"
  ```

I compositor basati su libxkbcommon 1.0 o successiva leggono `~/.config/xkb` da soli. GNOME e KDE
mostrano solo i layout registrati nelle regole XKB di sistema (`evdev.xml`), quindi per ora il layout
non compare nelle loro impostazioni; le istruzioni per registrarlo sono ancora da scrivere.

Per tornare indietro, riporta il layout a `it`.

**Verificato:** il file compila con `xkbcomp` e con libxkbcommon, e un test rilegge dalla mappa
compilata tutti i 103 caratteri e tasti morti. **Non ancora provato** in una vera sessione desktop.

## keybr (esercizi di digitazione)

[`dist/keybr/it_dvorak_v2.json`](../dist/keybr/it_dvorak_v2.json) (con tasto morto) e
[`it_dvorak_v2_simple.json`](../dist/keybr/it_dvorak_v2_simple.json) (senza) sono nel formato
`importKeymap` di keybr. Il sito pubblico keybr.com non permette di importare layout personalizzati,
quindi serve una copia self-hosted di keybr:

1. Copia il file in `packages/keybr-generators/layouts/`.
2. In `packages/keybr-generators/lib/generate-layouts.ts` aggiungi
   `["it_dvorak", importKeymap("layouts/it_dvorak_v2.json")],` dopo la riga `it_it`, poi esegui
   `npm run generate-layouts` in `packages/keybr-generators`.
3. In `packages/keybr-keyboard/lib/layout.ts` aggiungi un layout `IT_DVORAK` (family `dvorak`,
   `Language.IT`, con le geometrie ISO e ANSI) e inseriscilo in `Layout.ALL`. Usa `emulate: true` solo
   con il file semplice.

I file di v1 passavano il generatore di keybr; quelli di v2 usano lo stesso formato ma non sono ancora
stati provati.

## Windows e macOS

Non ancora disponibili. Il file della mappa contiene tutto il necessario per generare un `.klc`
per Windows (Microsoft Keyboard Layout Creator) o un `.keylayout` per macOS.
