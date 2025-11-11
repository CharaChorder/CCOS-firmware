from runner import run_tests
import os
import urllib.request
import json

DEFAULT_VERSION = "2.2.0-beta.19"

builds_dir = os.path.join(os.path.dirname(__file__), "builds")

if __name__ == "__main__":
    version = os.getenv("CCOS_VERSION", DEFAULT_VERSION)

    build_dir = os.path.join(builds_dir, version)
    if not os.path.exists(build_dir):
        print(f"Downloading build {version}...")
        with urllib.request.urlopen(
            f"https://charachorder.io/firmware/zero_linux/{version}/meta.json"
        ) as response:
            os.makedirs(build_dir, exist_ok=True)
            meta = json.load(response)
            with open(os.path.join(build_dir, "meta.json"), "wb") as f:
                f.write(json.dumps(meta).encode("utf-8"))
        for file in meta["files"]:
            print(f"Downloading {file}...")
            with urllib.request.urlopen(
                f"https://charachorder.io/firmware/zero_linux/{version}/{file}"
            ) as response:
                with open(os.path.join(build_dir, file), "wb") as f:
                    f.write(response.read())
        pass

    run_tests(build_dir)
