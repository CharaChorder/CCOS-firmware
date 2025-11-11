from ctypes import (
    c_bool,
    cdll,
    CDLL,
    c_char_p,
    c_char,
    c_uint8,
    c_uint16,
    c_uint32,
    CFUNCTYPE,
    POINTER,
    Structure,
    c_void_p,
    create_string_buffer,
)
from collections.abc import Callable
import os
import json


REPORT_CALLBACK = CFUNCTYPE(
    None,
    c_uint8,
    c_uint8,
    c_uint8,
    c_uint8,
    c_uint8,
    c_uint8,
    c_uint8,
    c_uint8,
    c_uint8,
    c_uint8,
    c_uint8,
    c_uint8,
    c_uint8,
)
SERIAL_CALLBACK = CFUNCTYPE(None, c_char)


class KeyReport:
    def __init__(self, modifiers: int, keys: list[int]):
        self.modifiers = modifiers
        self.keys = keys

    def __repr__(self) -> str:
        return f"KeyReport(modifiers={self.modifiers}, keys={self.keys})"


class ChordPhrase(Structure):
    _fields_ = [("length", c_uint16), ("bytes", c_uint8 * 228)]


class ChordInput(Structure):
    _fields_ = [("bytes", c_uint8 * 16)]


class CCOS:
    lib: CDLL

    on_report: Callable[[KeyReport], None] | None
    serial_out: bytearray

    action_to_id: dict[int, str]
    id_to_action: dict[str, int]
    id_to_keycode: dict[str, int]
    settings: dict[str, dict[str, dict]]

    meta: dict
    actions: dict

    idle: bool

    def __init__(self, lib_path: str, data_path: str):
        self.serial_out = bytearray()
        self.on_report = None
        self.action_to_id = {}
        self.id_to_action = {}
        self.id_to_keycode = {}
        self.settings = {}
        self.lib = cdll.LoadLibrary(lib_path)
        self.idle = False

        def report_callback(modifiers: int, *keys: int):
            if self.on_report:
                self.on_report(KeyReport(modifiers, list(keys)))

        def serial_callback(data: bytes):
            print(data.decode("ascii"), end="")
            self.serial_out.append(*data)

        self.c_on_report = REPORT_CALLBACK(report_callback)
        self.c_on_serial = SERIAL_CALLBACK(serial_callback)

        self.lib.init.argtypes = [c_char_p, c_void_p, c_void_p]
        self.lib.init.restype = None
        self.lib.update.argtypes = [c_uint32]
        self.lib.update.restype = c_bool
        self.lib.addPressedKey.argtypes = [c_uint8]
        self.lib.addPressedKey.restype = None
        self.lib.removePressedKey.argtypes = [c_uint8]
        self.lib.removePressedKey.restype = None
        self.lib.serialWrite.argtypes = [c_char]
        self.lib.serialWrite.restype = None
        self.lib.encodeChordInput.argtypes = [POINTER(c_uint16), c_uint8]
        self.lib.encodeChordInput.restype = ChordInput
        self.lib.encodeChordPhrase.argtypes = [POINTER(c_uint16), c_uint8]
        self.lib.encodeChordPhrase.restype = ChordPhrase
        self.lib.setCompoundChord.argtypes = [ChordInput, ChordInput]
        self.lib.setCompoundChord.restype = ChordInput

        with open(os.path.join(os.path.dirname(lib_path), "meta.json"), "r") as f:
            self.meta = json.load(f)

        def load_factory_defaults(items: dict):
            for key in items:
                if isinstance(items[key], str):
                    with open(
                        os.path.join(os.path.dirname(lib_path), items[key]), "r"
                    ) as f:
                        items[key] = json.load(f)
                else:
                    load_factory_defaults(items[key])

        load_factory_defaults(self.meta["factory_defaults"])

        with open(
            os.path.join(os.path.dirname(lib_path), self.meta["settings"]), "r"
        ) as f:
            settings = json.load(f)
            for category in settings:
                category_name = category["name"]
                self.settings[category_name] = {}
                for item in category["items"]:
                    item_name = item["name"]
                    self.settings[category_name][item_name] = item

        with open(
            os.path.join(os.path.dirname(lib_path), self.meta["actions"]), "r"
        ) as f:
            self.actions = json.load(f)
        for group in self.actions:
            group_actions = group["actions"]
            for action_str in group_actions:
                id = group["actions"][action_str].get("id", None)
                if id is None:
                    continue
                action = int(action_str)
                self.action_to_id[action] = id
                self.id_to_action[id] = action

        for i, action in enumerate(
            self.meta["factory_defaults"]["layout"]["layout"][0]
        ):
            name = self.action_to_id.get(action, None)
            if name is not None:
                assert name not in self.id_to_keycode
                self.id_to_keycode[name] = i

        self.lib.init(
            create_string_buffer(data_path.encode("utf-8")),
            self.c_on_report,
            self.c_on_serial,
        )

    def unload(self):
        stdlib = cdll.LoadLibrary("")
        stdlib.dlclose
        stdlib.dlclose.argtypes = [c_void_p]
        handle = self.lib._handle
        del self.lib
        stdlib.dlclose(handle)

    def update(self, millis: int) -> bool:
        self.idle = not self.lib.update(millis)
        return self.idle

    def addPressedKey(self, key: int):
        self.lib.addPressedKey(key)

    def removePressedKey(self, key: int):
        self.lib.removePressedKey(key)

    def serialWrite(self, data: int):
        self.lib.serialWrite(data)

    def serialSend(self, data: str):
        print(f">>> {data}")
        for char in data.encode("ascii") + b"\r\n":
            self.lib.serialWrite(char)

    def serialReceive(self) -> str:
        index = self.serial_out.find(b"\r\n")
        if index == -1:
            return ""
        result = self.serial_out[:index].decode("ascii")
        self.serial_out = self.serial_out[index + 2 :]
        return result

    def fromId(self, id: str | int) -> int:
        if isinstance(id, str):
            return self.id_to_action[id]
        return id

    def toId(self, action: int) -> str | int:
        return self.action_to_id.get(action, action)

    def toKeycode(self, id: str | int) -> int:
        if isinstance(id, str):
            return self.id_to_keycode[id]
        return id

    def encodeChordInput(
        self,
        input: list[list[str | int]] | list[list[int]],
    ) -> str:
        result: ChordInput | None = None
        for part in reversed(input):
            arr_type = c_uint16 * len(part)
            arr = arr_type(*map(lambda id: self.fromId(id), part))
            next = self.lib.encodeChordInput(arr, len(part))
            result = next if result is None else self.lib.setCompoundChord(next, result)
        assert result is not None
        return "".join(f"{byte:02X}" for byte in reversed(result.bytes))

    def encodeChordPhrase(self, actions: list[str | int] | list[int]) -> str:
        arr_type = c_uint16 * len(actions)
        arr = arr_type(*map(lambda id: self.fromId(id), actions))
        result = self.lib.encodeChordPhrase(arr, len(actions))
        return "".join(f"{self.fromId(id):02X}" for id in result.bytes[: result.length])

    def humanReadableActions(self, actions: list[str | int] | list[int]) -> str:
        return " ".join(f"{self.toId(self.fromId(id))}" for id in actions)
