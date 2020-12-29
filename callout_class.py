#!/usr/bin/env python

"""Assigns all elements of a class to a given class."""

import logging
import pathlib

import vs  # pylint: disable=syntax-error

CLASS = "ANNO-NOTES"
IGNORE_CLASS = "ANNO-GRAPHIC TAGS"
LOG_LEVEL = logging.DEBUG

# https://developer.vectorworks.net/index.php/VS:GetFolderPath
USER_PLUGINS_DIR = -2


def main() -> None:
    log_filename = pathlib.Path(vs.GetFolderPath(USER_PLUGINS_DIR)) / "adi_script.log"
    logging.basicConfig(filename=log_filename, level=LOG_LEVEL)

    updated = 0
    total = 0

    def set_class(obj) -> None:
        nonlocal updated
        nonlocal total
        klass = vs.GetClass(obj)
        logging.debug("%s class: %s", vs.GetName(obj), klass)
        if klass != CLASS:
            vs.SetClass(obj, CLASS)
            updated += 1
        total += 1

    vs.ForEachObject(set_class, "(R IN ['Callout']) & C<>'{}'".format(IGNORE_CLASS))
    vs.AlrtDialog("Updated {} of {} callouts\n{}".format(updated, total, log_filename))


if __name__ == "__main__":
    main()
