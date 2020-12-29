#!/usr/bin/env python

"""Analyze VectorWorks file for notable signatures."""

import vs


def main():
    output = []
    output.append("lines: {}".format(vs.Count("T=LINE")))
    output.append("rects: {}".format(vs.Count("T=RECT")))
    output.append("verts: {}".format(vs.Count("T=VERT")))
    output.append("all: {}".format(vs.Count("ALL")))
    vs.AlrtDialog("\n".join(output))


if __name__ == "__main__":
    main()
