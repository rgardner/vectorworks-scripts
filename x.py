#!/usr/bin/env python

"""Project setup, build, and test script."""

import argparse
import io
import pathlib
import subprocess
import sys
import urllib.request
import zipfile
from typing import List

VS_ZIP_FILE_URL = "https://developer.vectorworks.net/images/c/c5/Vs.zip"
SCRIPT_DIR = pathlib.Path(__file__).absolute().parent


def run_setup() -> None:
    subprocess.run(
        ["pip", "install", "--requirement", str(SCRIPT_DIR / "requirements.txt")],
        check=True,
    )

    subprocess.run(["pre-commit", "install"], check=True)

    output = SCRIPT_DIR / "build"
    output.mkdir(exist_ok=True)
    if not (output / "vs.py").exists():
        with urllib.request.urlopen(VS_ZIP_FILE_URL) as resp:
            with io.BytesIO(resp.read()) as buf, zipfile.ZipFile(buf) as zipf:
                zipf.extract("vs.py", output)


def run_ci() -> None:
    subprocess.run(["pre-commit", "run", "--all-files"], check=True)


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers()

    setup_parser = subparsers.add_parser("setup")
    setup_parser.set_defaults(func=run_setup)

    ci_parser = subparsers.add_parser("ci")
    ci_parser.set_defaults(func=run_ci)

    return parser.parse_args(args)


def main(raw_args: List[str]) -> None:
    args = parse_args(raw_args)
    if (func := getattr(args, "func", None)) is not None:
        func()  # pylint: disable=not-callable
    else:
        run_setup()


if __name__ == "__main__":
    main(sys.argv[1:])
