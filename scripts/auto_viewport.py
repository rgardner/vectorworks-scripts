#!/usr/bin/env python

"""Create viewports from each selected rectangle."""

import enum

import vs


@enum.unique
class ObjectIndex(enum.IntEnum):
    VP_RENDER_TYPE = 1001  # int
    VP_SCALE = 1003  # real
    VP_USE_DOCUMENT_CLASS_VISIBILITY = 1031  # bool


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
            # Quickly update viewport properties without "red cross" issue by
            # setting render type to wireframe to avoid rendering
            # https://forum.vectorworks.net/index.php?/topic/74320-exporting-rendersimages-to-folder/&tab=comments#comment-360809
            vs.SetObjectVariableInt(
                vp, ObjectIndex.VP_RENDER_TYPE, RenderStyle.WIREFRAME
            )
            vs.SetObjectVariableReal(vp, ObjectIndex.VP_SCALE, scale(1, 2))
            vs.SetObjectVariableBoolean(
                vp, ObjectIndex.VP_USE_DOCUMENT_CLASS_VISIBILITY, True
            )
            vs.SetVPCropObject(vp, obj)
            vs.UpdateVP(vp)

            # Separate viewports for better group/move UX
            vs.HMove(obj, 10, 0)

            # Restore OpenGL render type to force re-render
            vs.SetObjectVariableInt(vp, ObjectIndex.VP_RENDER_TYPE, RenderStyle.OPENGL)
            vs.UpdateVP(vp)

    vs.ForEachObject(create_viewport, "T=RECT")


if __name__ == "__main__":
    main()
