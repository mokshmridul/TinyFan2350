"""Dump the TinyFan2350 top-side layout (mm, origin at the board's top-left corner, Y down) for the illustrations."""
import json

import pcbnew

from pathlib import Path

HERE = Path(__file__).resolve().parent
BOARD_PATH = str(HERE.parent / "KiCad" / "TinyFan2350.kicad_pcb")
OUTPUT_PATH = str(HERE / "layout.json")
ORIGIN_X = 50.0
ORIGIN_Y = 50.0

board = pcbnew.LoadBoard(BOARD_PATH)


def xy(point):
    return [round(pcbnew.ToMM(point.x) - ORIGIN_X, 3), round(pcbnew.ToMM(point.y) - ORIGIN_Y, 3)]


def box(bounding_box):
    return [
        round(pcbnew.ToMM(bounding_box.GetLeft()) - ORIGIN_X, 3),
        round(pcbnew.ToMM(bounding_box.GetTop()) - ORIGIN_Y, 3),
        round(pcbnew.ToMM(bounding_box.GetRight()) - ORIGIN_X, 3),
        round(pcbnew.ToMM(bounding_box.GetBottom()) - ORIGIN_Y, 3),
    ]


footprints = []
for footprint in board.GetFootprints():
    on_top = footprint.GetLayer() == pcbnew.F_Cu
    fab_layer = pcbnew.F_Fab if on_top else pcbnew.B_Fab
    fab_box = None
    for item in footprint.GraphicalItems():
        if item.GetLayer() == fab_layer and item.GetClass() == "PCB_SHAPE":
            item_box = item.GetBoundingBox()
            if fab_box is None:
                fab_box = item_box
            else:
                fab_box.Merge(item_box)
    courtyard = footprint.GetCourtyard(pcbnew.F_CrtYd if on_top else pcbnew.B_CrtYd).BBox()
    footprints.append(
        {
            "ref": footprint.GetReference(),
            "value": footprint.GetValue(),
            "package": str(footprint.GetFPID().GetLibItemName()),
            "top": on_top,
            "at": xy(footprint.GetPosition()),
            "rotation": footprint.GetOrientationDegrees(),
            "fab": box(fab_box) if fab_box is not None else None,
            "courtyard": box(courtyard),
            "pads": [
                {
                    "number": pad.GetNumber(),
                    "at": xy(pad.GetPosition()),
                    "net": pad.GetNetname(),
                    "size": [round(pcbnew.ToMM(pad.GetSize(pcbnew.F_Cu).x), 2), round(pcbnew.ToMM(pad.GetSize(pcbnew.F_Cu).y), 2)],
                    "drill": round(pcbnew.ToMM(pad.GetDrillSize().x), 2),
                    "through": pad.GetAttribute() == pcbnew.PAD_ATTRIB_PTH,
                }
                for pad in footprint.Pads()
            ],
        }
    )

silk = []
for drawing in board.GetDrawings():
    if drawing.GetClass() == "PCB_TEXT" and drawing.GetLayer() == pcbnew.F_SilkS:
        silk.append(
            {
                "text": drawing.GetText(),
                "at": xy(drawing.GetPosition()),
                "size": round(pcbnew.ToMM(drawing.GetTextSize().y), 2),
                "angle": drawing.GetTextAngleDegrees(),
            }
        )

with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
    json.dump({"footprints": footprints, "silk": silk}, handle, indent=1)

print("footprints:", len(footprints), "silk texts:", len(silk))
for footprint in sorted(footprints, key=lambda item: item["ref"]):
    if not footprint["top"]:
        continue
    pads = " ".join("%s=%s" % (pad["number"], pad["net"].lstrip("/")) for pad in footprint["pads"][:6])
    print(
        "%-5s %-44s rot %6.1f fab %s pads %d: %s"
        % (
            footprint["ref"], footprint["package"][:44], footprint["rotation"], footprint["fab"],
            len(footprint["pads"]), pads,
        )
    )
u1 = next(item for item in footprints if item["ref"] == "U1")
print("U1 pads:")
for pad in u1["pads"]:
    print("   %-3s %-10s at %s" % (pad["number"], pad["net"], pad["at"]))
