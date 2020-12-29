#!/usr/bin/env python

"""Project setup, build, and test script."""

import argparse
import io
import pathlib
import sys
import urllib.request
import zipfile
from typing import List

VS_ZIP_FILE_URL = "https://developer.vectorworks.net/images/c/c5/Vs.zip"
SCRIPT_DIR = pathlib.Path(__file__).absolute().parent


def setup() -> None:
    output = SCRIPT_DIR / "build"
    output.mkdir(exist_ok=True)
    if not (output / "vs.py").exists():
        with urllib.request.urlopen(VS_ZIP_FILE_URL) as resp:
            with io.BytesIO(resp.read()) as buf, zipfile.ZipFile(buf) as zipf:
                zipf.extract("vs.py", output)


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    return parser.parse_args(args)


def main(raw_args: List[str]) -> None:
    parse_args(raw_args)
    setup()


if __name__ == "__main__":
    main(sys.argv[1:])
