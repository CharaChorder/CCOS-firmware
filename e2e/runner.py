import os
import json
import yaml
from unittest import TestSuite, TestCase, main
import io
from xmlrunner import XMLTestRunner
from xmlrunner.extra.xunit_plugin import transform

from ccos_wrapper import CCOSWrapper


e2e_dir = os.path.dirname(os.path.abspath(__file__))
tests_dir = os.path.join(e2e_dir, "tests")

BOLD = "\033[1m"
RESET = "\033[0m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"


class CCOSTest(TestCase):
    wrapper: CCOSWrapper

    def __init__(self, build_dir: str, id: str, test_case: dict):
        super().__init__()
        self.build_dir = build_dir
        self.id = lambda: id
        self.shortDescription = lambda: test_case.get("description", "")
        self.test_case = test_case

    def setUp(self):
        self.wrapper = CCOSWrapper(self.build_dir, True)

    def tearDown(self):
        self.wrapper.ccos.unload()

    def runTest(self):
        assert isinstance(self.test_case["test"], list)
        for command in self.test_case["test"]:
            print(f"{BOLD}============={RESET}")
            if "clearChords" in command:
                print(f"{BOLD}Clearing chords{RESET}")
                self.wrapper.serial_verify("RST CLEARCML", f"RST CLEARCML{'.' * 100} 0")
                print(f"{BLUE}...1ms{RESET}")
            if "removeChords" in command:
                print(json.dumps(command))
                for chord in command["removeChords"]:
                    self.wrapper.remove_chord(chord["input"])
                    print(f"{BLUE}...1ms{RESET}")
            if "addChords" in command:
                for chord in command["addChords"]:
                    self.wrapper.add_chord(chord["input"], chord["output"])
                    print(f"{BLUE}...1ms{RESET}")
            if "verifyChords" in command:
                print(json.dumps(command))
                for chord in command["verifyChords"]:
                    self.wrapper.check_chord(chord["input"], chord["output"])
                    print(f"{BLUE}...1ms{RESET}")
            if "remap" in command:
                print(json.dumps(command))
                for layer, remaps in command["remap"].items():
                    for remap in remaps:
                        self.wrapper.remap(
                            layer, self.wrapper.ccos.toKeycode(remap[0]), remap[1]
                        )
                        print(f"{BLUE}...1ms{RESET}")
            if "serial" in command:
                print(f"?<< {command['expect']}")
                self.wrapper.serial_verify(command["serial"], command["expect"])
                print(f"{BLUE}...1ms{RESET}")
            if "press" in command:
                keys = command["press"]
                if isinstance(keys, str):
                    keys = [keys]
                print(f"{GREEN}+{' '.join(keys)}{RESET}")
                for key in keys:
                    self.wrapper.ccos.addPressedKey(self.wrapper.ccos.toKeycode(key))
            if "release" in command:
                keys = command["release"]
                if isinstance(keys, str):
                    keys = [keys]
                print(f"{RED}-{' '.join(keys)}{RESET}")
                for key in keys:
                    self.wrapper.ccos.removePressedKey(self.wrapper.ccos.toKeycode(key))

            if "step" not in command:
                command["step"] = 1
            self.wrapper.millis += command["step"]
            self.wrapper.ccos.update(self.wrapper.millis)
            print(f"{BLUE}...{command['step']}ms{RESET}")
            if "keys" in command:
                print(
                    f"{YELLOW}? modifiers=[{', '.join(command.get('modifiers', []))}] keys=[{', '.join(command['keys'])}]{RESET}"
                )
                self.assertGreater(len(self.wrapper.reports), 0)
                report = self.wrapper.reports.pop(0)
                keys = [self.wrapper.ccos.toKeycode(key) for key in command["keys"]]
                report.keys = [key for key in report.keys if key != 0]
                self.assertEqual(report.keys, keys)

            self.assertEqual(
                0,
                len(self.wrapper.reports),
                f"Expected no remaining reports, but got: {self.wrapper.reports}",
            )
            assert len(self.wrapper.ccos.serial_out) == 0
            if command.get("idle", False):
                assert self.wrapper.ccos.idle, "CCOS did not become idle"
            else:
                assert not self.wrapper.ccos.idle, "CCOS became idle unexpectedly"

        assert self.wrapper.ccos.idle, "CCOS is not idle after test completion"


class FactoryTest(TestCase):
    wrapper: CCOSWrapper
    build_dir: str

    def __init__(self, build_dir: str):
        super().__init__()
        self.build_dir = build_dir
        self.id = lambda: "Factory defaults"

    def setUp(self):
        self.wrapper = CCOSWrapper(self.build_dir, True)

    def tearDown(self):
        self.wrapper.ccos.unload()

    def runTest(self):
        print(self.wrapper.do_serial("ID"))
        print(self.wrapper.do_serial("VERSION"))

        self.wrapper.verify_layout(
            "A", self.wrapper.ccos.meta["factory_defaults"]["layout"]["layout"]
        )
        self.wrapper.serial_verify("CML CF", f"CML CF 976 0")
        corrupt_chord = "CML C3 FFFFFF3194000FF0000000000000FF00 " + "FF" * 32
        self.wrapper.serial_verify(corrupt_chord, corrupt_chord + " 0")
        self.wrapper.serial_verify("CML CE", f"CML CE. 0")

        self.wrapper.check_chord_backup(
            self.wrapper.ccos.meta["factory_defaults"]["chords"]["starter"]["chords"]
        )
        self.wrapper.serial_verify("RST CLEARCML", f"RST CLEARCML{'.' * 100} 0")
        self.wrapper.check_chord_backup([])

        self.wrapper.restart()

        self.wrapper.check_chord_backup([])


def collect_tests(build_dir: str) -> TestSuite:
    tests: list[TestCase] = [FactoryTest(build_dir)]
    for root, _, files in os.walk(tests_dir):
        for file in files:
            if not file.endswith(".yml"):
                continue
            with open(os.path.join(root, file), "r") as f:
                test = CCOSTest(build_dir, file.removesuffix(".yml"), yaml.safe_load(f))
                tests.append(test)
    return TestSuite(tests)


def run_tests(build_dir: str):
    report_file = os.path.join(e2e_dir, "report.xml")
    if os.path.exists(report_file):
        os.remove(report_file)
    suite = collect_tests(build_dir)
    out = io.BytesIO()
    runner = XMLTestRunner(output=out)
    runner.run(suite)
    with open(report_file, "wb") as report:
        report.write(transform(out.getvalue()))
