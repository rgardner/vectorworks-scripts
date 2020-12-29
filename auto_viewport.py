#!/usr/bin/env python

"""Create viewports from each selected rectangle."""

import enum

import vs  # pylint: disable=syntax-error


@enum.unique
class ObjectIndex(enum.IntEnum):
    VP_RENDER_TYPE = 1001
    VP_SCALE = 1003


@enum.unique
class RenderStyle(enum.IntEnum):
    WIREFRAME = 0
    OPENGL = 11


def scale(numerator: float, denominator: float) -> float:
    """Convert vp.Scale parameter from architectural scale."""
    return (denominator / numerator) * 12  # 12"


def main() -> None:
    def create_viewport(obj) -> None:
        if obj.selected:
            layer = vs.GetLayer(obj)
            # Separate viewports for better group/move UX
            vs.Move(10, 0)  # right, up
            vp = vs.CreateVP(layer)
            vs.SetObjectVariableInt(
                vp, ObjectIndex.VP_RENDER_TYPE, RenderStyle.WIREFRAME
            )
            vs.SetObjectVariableReal(vp, ObjectIndex.VP_SCALE, scale(1, 2))
            vs.UpdateVP(vp)
            vs.SetObjectVariableInt(vp, ObjectIndex.VP_RENDER_TYPE, RenderStyle.OPENGL)
            vs.UpdateVP(vp)

    vs.ForEachObject(create_viewport, "T=RECT")


if __name__ == "__main__":
    main()
