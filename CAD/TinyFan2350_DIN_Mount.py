"""TinyFan2350 DIN rail mount (3D printed tray).

Holds the TinyFan2350 PCB on a 35 mm DIN rail with ONE "DIN Rail Clip (Heat Insert Version)" by Maxstupo:
https://www.printables.com/model/537942-din-rail-clip-heat-insert-version
(the clip itself is CC BY-NC-SA and is not part of this repository - print it from Printables).

The board's long side (100 mm) sits across the rail, so the board uses 65 mm of rail length.

Run with CadQuery 2.x:
    python TinyFan2350_DIN_Mount.py
It writes CAD/TinyFan2350_DIN_Mount.step and STL/TinyFan2350_DIN_Mount.stl.

Coordinates (mm): X/Y = PCB outline seen from the top, origin at the PCB's lower-left corner
(X = 0 is the USB-C / power-input edge, Y = 65 is the fan-connector edge). Z = 0 is the underside
of the mount, the face the DIN clip is screwed to. The rail runs along Y.

GPL-3.0, part of TinyFan2350.
"""
from pathlib import Path

import cadquery as cq

# ----------------------------------------------------------------------------
# Parameters (mm)
# ----------------------------------------------------------------------------
# PCB
BOARD_LENGTH = 100.0            # X
BOARD_WIDTH = 65.0              # Y
BOARD_CORNER_RADIUS = 2.0
BOARD_HOLE_INSET = 3.5          # M3 mounting holes, from each board edge (93 x 58 mm pattern)

# Tray
PLATE_THICKNESS = 3.0
RIM_WIDTH = 5.0                 # solid frame left around the vent windows
WINDOW_END_MARGIN = 12.0        # windows start this far in from the short edges (room for the standoffs)
CENTRE_RIB_WIDTH = 6.0          # rib across the tray at mid length
WINDOW_CORNER_RADIUS = 2.0

# Standoffs for the PCB (M3 heat-set inserts, the same M3 x D4.6 x L4.0 type the DIN clip uses)
STANDOFF_HEIGHT = 7.0           # PCB underside above the plate; bottom parts are <= 2.4 mm, THT leads <= ~3.5 mm
STANDOFF_DIAMETER = 8.5
STANDOFF_BASE_FLARE = 1.5       # 45 degree cone at the foot of each standoff
INSERT_HOLE_DIAMETER = 4.2      # for M3 x D4.6 x L4.0 inserts; use 4.3 for 4.8 mm OD inserts
INSERT_HOLE_DEPTH = 6.0
INSERT_LEAD_IN = 0.4            # chamfer at the hole mouth

# DIN clip (measured from din_clip_heat_insert.step)
CLIP_LENGTH = 60.0              # across the rail (X)
CLIP_WIDTH = 18.0               # along the rail (Y)
CLIP_HOLE_FROM_HOOK_END = 5.0   # first M3 insert, measured from the fixed-hook end of the clip
CLIP_HOLE_SPACING = 51.0        # between the two M3 inserts
CLIP_RAIL_CENTRE_FROM_HOOK_END = 27.3   # middle of the 35 mm rail seat (fixed hook face at 9.8 mm)
CLIP_SLIDER_START = 9.3         # print-in-place latch + spring zone on the clip's flat face ...
CLIP_SLIDER_END = 52.0          # ... measured from the hook end
CLIP_SLIDER_WIDTH = 12.0
SLIDER_RELIEF_DEPTH = 0.4       # shallow pocket so the latch slides freely (0 = flat underside)

# Clip position: the rail centre line sits under the middle of the board, hook end towards X = 0 (USB-C edge)
CLIP_HOOK_END_X = BOARD_LENGTH / 2 - CLIP_RAIL_CENTRE_FROM_HOOK_END
CLIP_CENTRE_Y = BOARD_WIDTH / 2

# Raised spine over the clip, with the two clip screws (M3 x 6 or M3 x 8, socket or button head)
SPINE_HEIGHT = 2.0              # above the plate
SPINE_WIDTH = CLIP_WIDTH
SPINE_END_MARGIN = 2.0          # spine extends this far past each end of the clip
SPINE_GAP_TO_WINDOW = 2.0
CLIP_SCREW_CLEARANCE_DIAMETER = 3.4
CLIP_SCREW_HEAD_DIAMETER = 6.5  # counterbore
CLIP_SCREW_HEAD_DEPTH = 2.0     # leaves PLATE_THICKNESS + SPINE_HEIGHT - this = 3.0 mm under the head

# Orientation label, debossed into the spine ("" = no label)
LABEL_TEXT = "< USB     LATCH >"
LABEL_HEIGHT = 4.0
LABEL_DEPTH = 0.4

# ----------------------------------------------------------------------------
# Derived values
# ----------------------------------------------------------------------------
BOARD_HOLES = [
    (BOARD_HOLE_INSET, BOARD_HOLE_INSET),
    (BOARD_LENGTH - BOARD_HOLE_INSET, BOARD_HOLE_INSET),
    (BOARD_HOLE_INSET, BOARD_WIDTH - BOARD_HOLE_INSET),
    (BOARD_LENGTH - BOARD_HOLE_INSET, BOARD_WIDTH - BOARD_HOLE_INSET),
]
CLIP_SCREWS = [
    (CLIP_HOOK_END_X + CLIP_HOLE_FROM_HOOK_END, CLIP_CENTRE_Y),
    (CLIP_HOOK_END_X + CLIP_HOLE_FROM_HOOK_END + CLIP_HOLE_SPACING, CLIP_CENTRE_Y),
]
SPINE_TOP_Z = PLATE_THICKNESS + SPINE_HEIGHT
STANDOFF_TOP_Z = PLATE_THICKNESS + STANDOFF_HEIGHT
SPINE_X_START = CLIP_HOOK_END_X - SPINE_END_MARGIN
SPINE_X_END = CLIP_HOOK_END_X + CLIP_LENGTH + SPINE_END_MARGIN
SPINE_Y_START = CLIP_CENTRE_Y - SPINE_WIDTH / 2
SPINE_Y_END = CLIP_CENTRE_Y + SPINE_WIDTH / 2


def rounded_box(x_start, y_start, x_end, y_end, z_start, height, corner_radius):
    """Axis-aligned box with its vertical edges rounded."""
    box = (
        cq.Workplane("XY")
        .box(x_end - x_start, y_end - y_start, height, centered=False)
        .translate((x_start, y_start, z_start))
    )
    if corner_radius > 0:
        box = box.edges("|Z").fillet(corner_radius)
    return box


def cylinder(x, y, z_start, diameter, height):
    return cq.Workplane("XY").circle(diameter / 2).extrude(height).translate((x, y, z_start))


def cone(x, y, z_start, bottom_diameter, top_diameter, height):
    solid = cq.Solid.makeCone(bottom_diameter / 2, top_diameter / 2, height)
    return cq.Workplane("XY").add(solid).translate((x, y, z_start))


def build_mount():
    # Base plate with the PCB's outline
    mount = rounded_box(0, 0, BOARD_LENGTH, BOARD_WIDTH, 0, PLATE_THICKNESS, BOARD_CORNER_RADIUS)

    # Vent windows: two on each side of the spine, split by the centre rib
    window_x_ranges = [
        (WINDOW_END_MARGIN, BOARD_LENGTH / 2 - CENTRE_RIB_WIDTH / 2),
        (BOARD_LENGTH / 2 + CENTRE_RIB_WIDTH / 2, BOARD_LENGTH - WINDOW_END_MARGIN),
    ]
    window_y_ranges = [
        (RIM_WIDTH, SPINE_Y_START - SPINE_GAP_TO_WINDOW),
        (SPINE_Y_END + SPINE_GAP_TO_WINDOW, BOARD_WIDTH - RIM_WIDTH),
    ]
    for x_start, x_end in window_x_ranges:
        for y_start, y_end in window_y_ranges:
            window = rounded_box(
                x_start, y_start, x_end, y_end, 0, PLATE_THICKNESS, WINDOW_CORNER_RADIUS
            )
            mount = mount.cut(window)

    # Raised spine over the clip
    spine = rounded_box(
        SPINE_X_START, SPINE_Y_START, SPINE_X_END, SPINE_Y_END,
        PLATE_THICKNESS, SPINE_HEIGHT, WINDOW_CORNER_RADIUS,
    )
    mount = mount.union(spine)

    # Standoffs with a flared foot
    for x, y in BOARD_HOLES:
        mount = mount.union(cylinder(x, y, PLATE_THICKNESS, STANDOFF_DIAMETER, STANDOFF_HEIGHT))
        mount = mount.union(
            cone(
                x, y, PLATE_THICKNESS,
                STANDOFF_DIAMETER + 2 * STANDOFF_BASE_FLARE, STANDOFF_DIAMETER, STANDOFF_BASE_FLARE,
            )
        )

    # Trim everything to the PCB outline so nothing sticks out past the board
    envelope = rounded_box(0, 0, BOARD_LENGTH, BOARD_WIDTH, 0, STANDOFF_TOP_Z, BOARD_CORNER_RADIUS)
    mount = mount.intersect(envelope)

    # Heat-set insert holes in the standoffs
    for x, y in BOARD_HOLES:
        mount = mount.cut(
            cylinder(x, y, STANDOFF_TOP_Z - INSERT_HOLE_DEPTH, INSERT_HOLE_DIAMETER, INSERT_HOLE_DEPTH)
        )
        mount = mount.cut(
            cone(
                x, y, STANDOFF_TOP_Z - INSERT_LEAD_IN,
                INSERT_HOLE_DIAMETER, INSERT_HOLE_DIAMETER + 2 * INSERT_LEAD_IN, INSERT_LEAD_IN,
            )
        )

    # Clip screws: clearance hole from the underside, counterbore for the head from the top
    for x, y in CLIP_SCREWS:
        mount = mount.cut(cylinder(x, y, 0, CLIP_SCREW_CLEARANCE_DIAMETER, SPINE_TOP_Z))
        mount = mount.cut(
            cylinder(
                x, y, SPINE_TOP_Z - CLIP_SCREW_HEAD_DEPTH,
                CLIP_SCREW_HEAD_DIAMETER, CLIP_SCREW_HEAD_DEPTH,
            )
        )

    # Relief under the clip's sliding latch and spring
    if SLIDER_RELIEF_DEPTH > 0:
        relief = rounded_box(
            CLIP_HOOK_END_X + CLIP_SLIDER_START,
            CLIP_CENTRE_Y - CLIP_SLIDER_WIDTH / 2,
            CLIP_HOOK_END_X + CLIP_SLIDER_END,
            CLIP_CENTRE_Y + CLIP_SLIDER_WIDTH / 2,
            0, SLIDER_RELIEF_DEPTH, 1.0,
        )
        mount = mount.cut(relief)

    # Orientation label between the two clip screws
    if LABEL_TEXT:
        label_centre_x = (CLIP_SCREWS[0][0] + CLIP_SCREWS[1][0]) / 2
        label = (
            cq.Workplane("XY")
            .workplane(offset=SPINE_TOP_Z)
            .center(label_centre_x, CLIP_CENTRE_Y)
            .text(LABEL_TEXT, LABEL_HEIGHT, -LABEL_DEPTH, kind="bold", halign="center", valign="center")
        )
        mount = mount.cut(label)

    return mount


if __name__ == "__main__":
    cad_folder = Path(__file__).resolve().parent
    stl_folder = cad_folder.parent / "STL"
    stl_folder.mkdir(exist_ok=True)
    step_path = cad_folder / "TinyFan2350_DIN_Mount.step"
    stl_path = stl_folder / "TinyFan2350_DIN_Mount.stl"

    mount = build_mount()
    solid = mount.val()
    box = solid.BoundingBox(tolerance=1e-5)   # measured before meshing, so the size is exact

    cq.exporters.export(mount, str(step_path))
    cq.exporters.export(mount, str(stl_path), tolerance=0.02, angularTolerance=0.1)
    print(f"wrote {step_path}")
    print(f"wrote {stl_path}")
    print(
        f"size {box.xlen:.2f} x {box.ylen:.2f} x {box.zlen:.2f} mm, "
        f"volume {solid.Volume() / 1000:.1f} cm3, solids {len(mount.solids().vals())}, valid {solid.isValid()}"
    )
    print(f"clip screws at {CLIP_SCREWS}, rail centre at X = {BOARD_LENGTH / 2:.1f}")
