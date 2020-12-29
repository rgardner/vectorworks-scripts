#!/usr/bin/env python

"""Assigns all elements of a class to a given class."""

import vs  # pylint: disable=syntax-error

CLASS = "ANNO-NOTES"
IGNORE_CLASS = "ANNO-GRAPHIC TAGS"


def main() -> None:
    updated = 0
    total = 0

    def set_class(obj) -> None:
        nonlocal updated
        nonlocal total
        curr_class = vs.GetClass(obj)
        if curr_class == IGNORE_CLASS:
            return
        if curr_class != CLASS:
            vs.SetClass(obj, CLASS)
            updated += 1
        total += 1

    vs.ForEachObject(set_class, "T=CALLOUT")
    vs.AlrtDialog("Updated {} of {} callouts".format(updated, total))


if __name__ == "__main__":
    main()
