#!/usr/bin/env python

import vs


def main():
    num = 0
    def count(_obj):
        nonlocal num
        num += 1
    vs.ForEachObject(count, "T=LINE")
    vs.AlrtDialog(f"num lines: {num}")


if __name__ == "__main__":
    main()
