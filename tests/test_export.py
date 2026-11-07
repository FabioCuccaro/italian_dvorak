import ctypes
import ctypes.util
import json
import tempfile
import unittest
from pathlib import Path

from kbeval.export import XKB_KEYS, check_against_layout, keybr_layout, xkb_symbols

ROOT = Path(__file__).resolve().parent.parent
KEYMAP = ROOT / "keymaps" / "italian-dvorak-v2.json"
SYSTEM_XKB = Path("/usr/share/X11/xkb")


class Keymap(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads(KEYMAP.read_text(encoding="utf-8"))

    def test_matches_scored_layout(self):
        check_against_layout(self.spec, ROOT / self.spec["layout"])

    def test_every_physical_key_is_defined(self):
        self.assertEqual(set(self.spec["keys"]), set(XKB_KEYS))

    def test_keybr_dead_key(self):
        self.assertEqual(keybr_layout(self.spec, dead_keys=True)["Quote"], ["*`", "*´"])
        self.assertEqual(keybr_layout(self.spec, dead_keys=False)["KeyT"], "èé")


@unittest.skipUnless(ctypes.util.find_library("xkbcommon") and SYSTEM_XKB.is_dir(),
                     "libxkbcommon and xkeyboard-config are needed")
class XkbCompile(unittest.TestCase):
    """Compile the generated XKB file with libxkbcommon and read every key back."""

    def test_every_symbol(self):
        spec = json.loads(KEYMAP.read_text(encoding="utf-8"))
        lib = ctypes.CDLL(ctypes.util.find_library("xkbcommon"))

        class Names(ctypes.Structure):
            _fields_ = [(n, ctypes.c_char_p) for n in ("rules", "model", "layout", "variant", "options")]

        lib.xkb_context_new.restype = ctypes.c_void_p
        lib.xkb_context_include_path_append.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lib.xkb_keymap_new_from_names.restype = ctypes.c_void_p
        lib.xkb_keymap_new_from_names.argtypes = [ctypes.c_void_p, ctypes.POINTER(Names), ctypes.c_int]
        lib.xkb_keymap_key_by_name.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lib.xkb_keymap_key_by_name.restype = ctypes.c_uint32
        lib.xkb_keymap_key_get_syms_by_level.argtypes = [
            ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32,
            ctypes.POINTER(ctypes.POINTER(ctypes.c_uint32))]
        lib.xkb_keysym_get_name.argtypes = [ctypes.c_uint32, ctypes.c_char_p, ctypes.c_size_t]
        lib.xkb_keysym_to_utf32.argtypes = [ctypes.c_uint32]
        lib.xkb_keysym_to_utf32.restype = ctypes.c_uint32

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "symbols").mkdir()
            (Path(tmp) / "symbols" / "itdvorak").write_text(xkb_symbols(spec), encoding="utf-8")
            ctx = lib.xkb_context_new(1)  # no default include paths
            lib.xkb_context_include_path_append(ctx, tmp.encode())
            lib.xkb_context_include_path_append(ctx, str(SYSTEM_XKB).encode())
            names = Names(b"evdev", b"pc105", b"itdvorak", b"", b"")
            keymap = lib.xkb_keymap_new_from_names(ctx, ctypes.byref(names), 0)
        self.assertTrue(keymap, "the XKB file does not compile")

        for code, symbols in spec["keys"].items():
            key = lib.xkb_keymap_key_by_name(keymap, XKB_KEYS[code].encode())
            for level, expected in enumerate(symbols):
                syms = ctypes.POINTER(ctypes.c_uint32)()
                n = lib.xkb_keymap_key_get_syms_by_level(keymap, key, 0, level, ctypes.byref(syms))
                self.assertEqual(n, 1, f"{code} level {level + 1}")
                buf = ctypes.create_string_buffer(64)
                lib.xkb_keysym_get_name(syms[0], buf, 64)
                name = buf.value.decode()
                got = name if name.startswith("dead_") else chr(lib.xkb_keysym_to_utf32(syms[0]))
                self.assertEqual(got, expected, f"{code} level {level + 1}")


if __name__ == "__main__":
    unittest.main()
