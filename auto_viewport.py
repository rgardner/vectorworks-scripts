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
    """Convert architectural scale to vp.Scale parameter."""
    return (denominator / numerator) * 12  # 12"


def main() -> None:
    def create_viewport(obj) -> None:
        if obj.selected:
            layer = vs.GetLayer(obj)
            vp = vs.CreateVP(layer)
            # Render twice (first using WIREFRAME) to avoid "red cross" when
            # changing variables.
            # https://forum.vectorworks.net/index.php?/topic/74320-exporting-rendersimages-to-folder/&tab=comments#comment-360809
            vs.SetObjectVariableInt(
                vp, ObjectIndex.VP_RENDER_TYPE, RenderStyle.WIREFRAME
            )
            vs.SetObjectVariableReal(vp, ObjectIndex.VP_SCALE, scale(1, 2))
            vs.UpdateVP(vp)
            vs.SetObjectVariableInt(vp, ObjectIndex.VP_RENDER_TYPE, RenderStyle.OPENGL)
            vs.UpdateVP(vp)

            # Separate viewports for better group/move UX
            vs.HMove(obj, 10, 0)

    vs.ForEachObject(create_viewport, "T=RECT")


if __name__ == "__main__":
    main()
