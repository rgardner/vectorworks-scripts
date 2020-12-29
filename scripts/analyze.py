#!/usr/bin/env python

"""Analyze VectorWorks file for notable signatures."""

import datetime
import logging
import pathlib
from typing import Any, Iterator

import vs

LOG_LEVEL = logging.DEBUG

# https://developer.vectorworks.net/index.php/VS:GetFolderPath
USER_PLUGINS_DIR = -2

Handle = Any


def vs_ts_to_str(ts: int) -> str:
    """Converts Vectorworks time in seconds since January 1, 1904 to a human friendly string."""
    d = datetime.datetime(year=1904, month=1, day=1) + datetime.timedelta(seconds=ts)
    return d.isoformat()


def layers() -> Iterator[Handle]:
    """Yields each layer in the document."""
    layer = vs.FLayer()
    while layer is not None:
        yield layer
        layer = vs.NextLayer(layer)


def main() -> None:
    log_filename = pathlib.Path(vs.GetFolderPath(USER_PLUGINS_DIR)) / "nla_analyze.log"
    logging.basicConfig(filename=log_filename, level=LOG_LEVEL)

    output = []
    output.append("lines: {}".format(vs.Count("T=LINE")))
    output.append("rects: {}".format(vs.Count("T=RECT")))
    output.append("verts: {}".format(vs.Count("T=VERT")))
    output.append("all: {}".format(vs.Count("ALL")))
    if vs.IsAWorkingFile():
        for i, layer in enumerate(layers()):
            if i == 0:
                output.append("Working file info:")
            project_info = vs.GetLayerProjectInfo(layer)
            layer_name = vs.GetLName(layer)
            mod_time = vs_ts_to_str(project_info[2])
            checkout_time = vs_ts_to_str(project_info[3])
            out_of_date = "yes" if project_info[7] else "no"
            output.append(
                "\tlayer: {}\tmodification: {}\tcheckout: {}\tout of date: {}".format(
                    layer_name, mod_time, checkout_time, out_of_date
                )
            )

    vs.AlrtDialog("\n".join(output))


if __name__ == "__main__":
    main()
