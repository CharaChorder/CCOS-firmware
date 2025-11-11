from ccos import CCOS, KeyReport
import os

flash_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "flash",
)


class CCOSWrapper:
    reports: list[KeyReport]

    def __init__(self, build_dir: str, clear_flash: bool):
        self.build_dir = build_dir
        if clear_flash and os.path.exists(flash_dir):
            os.system(f"rm -rf {flash_dir}")
        os.makedirs(flash_dir, exist_ok=True)
        self.reports = []
        self.ccos = CCOS(os.path.join(build_dir, "libccos.so"), flash_dir)

        def report_callback(report: KeyReport):
            self.reports.append(report)
            print(f"{report}")

        self.ccos.on_report = report_callback
        self.millis = 0

    def restart(self):
        self.ccos.unload()
        self.ccos = CCOS(os.path.join(self.build_dir, "libccos.so"), flash_dir)

    def do_serial(self, data: str) -> str:
        self.ccos.serialSend(data)
        self.millis += 1
        self.ccos.update(self.millis)
        return self.ccos.serialReceive()

    def serial_verify(self, command: str, expected: str, message: str | None = None):
        response = self.do_serial(command)
        assert response == expected, (
            f"Expected '{expected}', got '{response}'" if message is None else message
        )

    def remap(self, layer: str, key: int, action: str | int):
        action_id = (
            action if isinstance(action, int) else self.ccos.id_to_action[action]
        )
        command = f"VAR B4 {layer} {key} {action_id}"
        self.serial_verify(
            command,
            f"{command} 0",
        )

    def add_chord(
        self,
        input: list[list[str | int]] | list[list[int]],
        output: list[str | int] | list[int],
    ):
        input_encoded = self.ccos.encodeChordInput(input)
        output_encoded = self.ccos.encodeChordPhrase(output)
        command = f"CML C3 {input_encoded} {output_encoded}"
        self.serial_verify(
            command,
            f"{command} 0",
        )

    def remove_chord(self, input: list[list[str | int]] | list[list[int]]):
        input_encoded = self.ccos.encodeChordInput(input)
        command = f"CML C4 {input_encoded}"
        self.serial_verify(
            command,
            f"{command} 0",
        )

    def check_chord(
        self,
        input: list[list[str | int]] | list[list[int]],
        output: list[str | int] | list[int],
    ):
        input_encoded = self.ccos.encodeChordInput(input)
        output_encoded = self.ccos.encodeChordPhrase(output)
        command = f"CML C2 {input_encoded} {output_encoded}"
        self.serial_verify(
            command,
            f"{command} 0",
        )

    def check_chord_backup(self, chords: list[list[list[int]]]):
        self.serial_verify("CML C0", f"CML C0 {len(chords)}")
        chords_map = {}
        for chord in chords:
            input = self.ccos.encodeChordInput([chord[0]])
            output = self.ccos.encodeChordPhrase(chord[1])
            chords_map[input] = output
            command = f"CML C2 {input}"
            self.serial_verify(
                command,
                f"{command} {output} 0",
            )
        for i in range(len(chords)):
            command = f"CML C1 {i}"
            self.ccos.serialSend(command)
            self.millis += 1
            self.ccos.update(self.millis)
            response = self.ccos.serialReceive()
            [input, output] = (
                response.removeprefix(f"{command} ").removesuffix(" 0").split(" ")
            )
            assert chords_map[input] == output

    def verify_layout(self, profile: str, layout: list[list[int]]):
        for layer, row in enumerate(layout):
            for key, action in enumerate(row):
                command = f"VAR B3 {profile}{layer + 1} {key}"
                self.serial_verify(command, f"{command} {action} 0")

    def set_setting(self, category: str, item: str, value: str | int):
        setting_info: dict = self.ccos.settings[category][item]
        value_id: int = (
            setting_info["enum"].index(value) if isinstance(value, str) else value
        )
        assert value_id >= 0, f"Invalid setting value: {value}"
        command_str = f"VAR B2 0x{setting_info['id']:02X} {value_id}"
        self.serial_verify(
            command_str,
            f"{command_str} 0",
        )
