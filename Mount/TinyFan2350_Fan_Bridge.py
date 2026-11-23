"""TinyFan2350 fan bridge (3D printed).

Holds one 40 x 40 x 10 mm fan (4010) above the power terminals, the capacitors and the fuses, blowing down onto
the board. The fan sits in the corner of the board, flush with two of its edges: nothing reaches past the PCB
outline. Like the fan mounts people print for larger printer boards, the bridge stands on the PCB's own mounting
holes: two legs on the two holes at the USB-C end, held by the screws that also hold the board there. It fits
on the DIN mount and on any other M3 standoffs.

The deck wraps the fan on two sides and takes two of its screws. A third, long screw goes through the fan's
corner, through the leg below it and through the PCB into the standoff. The fourth corner of the fan hangs free
above the TH1 connector, so that its plug still fits.

Run with CadQuery 2.x:
    python TinyFan2350_Fan_Bridge.py
It writes TinyFan2350_Fan_Bridge.step (as mounted) and TinyFan2350_Fan_Bridge.stl (turned over for printing,
fan seat on the bed) next to this script.

Coordinates (mm): X/Y as in TinyFan2350_DIN_Mount.py - the PCB outline seen from the top, origin at the PCB's
lower-left corner, X = 0 is the USB-C / power-input edge, Y = 0 is the thermistor-connector edge.
Z = 0 is the top face of the PCB.

GPL-3.0, part of TinyFan2350.
"""
from pathlib import Path

import cadquery as cq

from TinyFan2350_DIN_Mount import (
    BOARD_CORNER_RADIUS,
    BOARD_HOLE_INSET,
    BOARD_LENGTH,
    BOARD_WIDTH,
    INSERT_HOLE_DIAMETER,
    INSERT_LEAD_IN,
    cone,
    cylinder,
    rounded_box,
)

# ----------------------------------------------------------------------------
# Parameters (mm)
# ----------------------------------------------------------------------------
PCB_THICKNESS = 1.6

# Fan (40 x 40 x 10 mm)
FAN_SIZE = 40.0
FAN_THICKNESS = 10.0
FAN_HOLE_SPACING = 32.0
FAN_CORNER_RADIUS = 4.0
FAN_OPENING_DIAMETER = 37.4

# Screws that hold the bridge: one through each leg and the PCB into the standoff below
LEG_SCREW_LENGTH = 30.0         # M3x30 on the upper hole, its head on the arm. The lower hole is under the fan's
#                                 corner: there the screw also goes through the fan and is longer by the fan's thickness (M3x40)
LEG_SCREW_ENGAGEMENT = 4.5      # thread left below the PCB (the DIN mount's inserts are 4.0 long, their holes 6.0 deep)
LEG_SCREW_CLEARANCE_DIAMETER = 3.4
FAN_LEG_SCREW_CLEARANCE_DIAMETER = 3.6     # the hole under the fan's corner; it leans a little, see fan_leg_screw_hole()
LEG_FOOT_DIAMETER = 7.0         # on the PCB; this is as wide as the hole's distance to the board edges allows
LEG_TOP_DIAMETER = 8.0          # where the leg meets the deck, and the pad around the upper screw

# Deck: the part the fan sits on
DECK_THICKNESS = 6.0            # fan screws: M3x16 (10 mm fan + 6 mm deck)
RIM_WIDTH = 2.5                 # narrowest part of the deck along the top of the fan
BEAM_WIDTH = 3.8                # ... and along the USB-C edge, where the deck is the beam between the two legs
CORNER_BLOCK = 8.0              # the deck keeps a strip this wide along the USB-C edge and along the top of the fan
ARM_WIDTH = 5.0                 # arm from the deck to the leg on the upper hole
INSIDE_CORNER_RADIUS = 2.0      # every inside corner of the outline
END_CORNER_RADIUS = 2.0         # the two free ends of the deck
FAN_INSERT_DEPTH = 4.6          # M3 x D4.6 x L4.0 inserts, pressed in from the underside of the deck
FAN_SCREW_CLEARANCE_DIAMETER = 3.4

# Screws of the two power terminals (VIN: GND, +; 5V: GND, +). With the fan taken off, a screwdriver reaches
# all four through the deck; the deck is relieved where it would be in the way.
TERMINAL_SCREWS = [(6.0, 31.08), (6.0, 26.0), (6.0, 17.58), (6.0, 12.5)]
SCREWDRIVER_CLEARANCE_DIAMETER = 4.2

# ----------------------------------------------------------------------------
# Derived values
# ----------------------------------------------------------------------------
# The fan sits in the corner of the board, flush with the USB-C edge and the thermistor edge. That centres it
# over the fuses and capacitors (their middle is at Y 19.5). The layout depends on this position: the lower leg
# stands under the fan's corner.
FAN_CENTRE_X = FAN_SIZE / 2
FAN_CENTRE_Y = FAN_SIZE / 2

UPPER_HOLE = (BOARD_HOLE_INSET, BOARD_WIDTH - BOARD_HOLE_INSET)    # next to the RP2350-Zero
LOWER_HOLE = (BOARD_HOLE_INSET, BOARD_HOLE_INSET)                  # under the fan's corner
LEG_HOLES = [UPPER_HOLE, LOWER_HOLE]

DECK_TOP_Z = LEG_SCREW_LENGTH - PCB_THICKNESS - LEG_SCREW_ENGAGEMENT   # the fan sits on this face
DECK_UNDERSIDE_Z = DECK_TOP_Z - DECK_THICKNESS                         # = height of the legs
FAN_LEG_SCREW_LENGTH = LEG_SCREW_LENGTH + FAN_THICKNESS

SEAT_LEFT = FAN_CENTRE_X - FAN_SIZE / 2
SEAT_RIGHT = FAN_CENTRE_X + FAN_SIZE / 2
SEAT_BOTTOM = FAN_CENTRE_Y - FAN_SIZE / 2
SEAT_TOP = FAN_CENTRE_Y + FAN_SIZE / 2

HALF_HOLE_SPACING = FAN_HOLE_SPACING / 2
FAN_SCREWS = [                  # into heat-set inserts in the deck
    (FAN_CENTRE_X - HALF_HOLE_SPACING, FAN_CENTRE_Y + HALF_HOLE_SPACING),
    (FAN_CENTRE_X + HALF_HOLE_SPACING, FAN_CENTRE_Y + HALF_HOLE_SPACING),
]
FAN_LEG_SCREW = (FAN_CENTRE_X - HALF_HOLE_SPACING, FAN_CENTRE_Y - HALF_HOLE_SPACING)   # through the lower leg
# The fan's fourth corner, above the TH1 connector, gets no support.


def box(x_start, y_start, x_end, y_end, z_start, height):
    return (
        cq.Workplane("XY")
        .box(x_end - x_start, y_end - y_start, height, centered=False)
        .translate((x_start, y_start, z_start))
    )


def within_board_outline(shape, z_start, height):
    """Trim a shape to the PCB outline, so that nothing reaches past the board."""
    return shape.intersect(rounded_box(0, 0, BOARD_LENGTH, BOARD_WIDTH, z_start, height, BOARD_CORNER_RADIUS))


def deck_outline():
    """Top view of the deck, the arm and the pad of the upper leg as one closed outline."""
    slab = 1.0      # the outline is put together from thin slabs, then read back as a wire

    seat = box(SEAT_LEFT, SEAT_BOTTOM, SEAT_RIGHT, SEAT_TOP, 0, slab).edges("|Z").fillet(FAN_CORNER_RADIUS)
    left_strip = (
        box(SEAT_LEFT, SEAT_BOTTOM, SEAT_LEFT + CORNER_BLOCK, SEAT_TOP, 0, slab)
        .edges("|Z").edges(">X").edges("<Y").fillet(END_CORNER_RADIUS)
    )
    top_strip = (
        box(SEAT_LEFT, SEAT_TOP - CORNER_BLOCK, SEAT_RIGHT, SEAT_TOP, 0, slab)
        .edges("|Z").edges(">X").edges("<Y").fillet(END_CORNER_RADIUS)
    )
    opening = cylinder(FAN_CENTRE_X, FAN_CENTRE_Y, 0, FAN_OPENING_DIAMETER, slab).intersect(
        box(
            SEAT_LEFT + BEAM_WIDTH, SEAT_BOTTOM + RIM_WIDTH,
            SEAT_RIGHT - RIM_WIDTH, SEAT_TOP - RIM_WIDTH,
            0, slab,
        )
    )
    arm = box(SEAT_LEFT, SEAT_TOP - CORNER_BLOCK / 2, SEAT_LEFT + ARM_WIDTH, BOARD_WIDTH, 0, slab)
    upper_pad = cylinder(UPPER_HOLE[0], UPPER_HOLE[1], 0, LEG_TOP_DIAMETER, slab)

    outline = seat.intersect(left_strip.union(top_strip)).cut(opening).union(arm).union(upper_pad)
    outline = within_board_outline(outline, 0, slab)

    wire = outline.faces(">Z").val().outerWire()
    # Round every inside corner: grow the outline, then shrink it back by the same amount
    wire = wire.offset2D(INSIDE_CORNER_RADIUS)[0].offset2D(-INSIDE_CORNER_RADIUS)[0]
    return wire.translate((0, 0, -slab))        # back down to Z = 0


def fan_leg_screw_hole():
    """Hole for the long screw through the fan's corner, the lower leg and the PCB.

    The fan's hole is 4 mm from the fan's edges, the PCB's hole 3.5 mm from the board's edges. With the fan
    flush with the board, the two are 0.7 mm apart, so this hole leans by about 1 degree from one to the other.
    """
    foot = cq.Vector(LOWER_HOLE[0], LOWER_HOLE[1], -PCB_THICKNESS)
    head = cq.Vector(FAN_LEG_SCREW[0], FAN_LEG_SCREW[1], DECK_TOP_Z + FAN_THICKNESS)
    axis = head - foot
    hole = cq.Solid.makeCylinder(FAN_LEG_SCREW_CLEARANCE_DIAMETER / 2, axis.Length, foot, axis)
    return cq.Workplane("XY").add(hole)


def fan_screw_hole(x, y):
    """Clearance hole from the fan side, insert pocket with a lead-in chamfer from the underside."""
    hole = cylinder(x, y, DECK_UNDERSIDE_Z, FAN_SCREW_CLEARANCE_DIAMETER, DECK_THICKNESS)
    pocket = cylinder(x, y, DECK_UNDERSIDE_Z, INSERT_HOLE_DIAMETER, FAN_INSERT_DEPTH)
    lead_in = cone(
        x, y, DECK_UNDERSIDE_Z,
        INSERT_HOLE_DIAMETER + 2 * INSERT_LEAD_IN, INSERT_HOLE_DIAMETER, INSERT_LEAD_IN,
    )
    return hole.union(pocket).union(lead_in)


def build_bridge():
    # Deck, arm and pad: one outline, one extrusion
    deck_face = cq.Face.makeFromWires(deck_outline())
    bridge = (
        cq.Workplane("XY")
        .add(cq.Solid.extrudeLinear(deck_face, cq.Vector(0, 0, DECK_THICKNESS)))
        .translate((0, 0, DECK_UNDERSIDE_Z))
    )

    # Legs, slightly tapered, flat where they would cross the board edge
    for x, y in LEG_HOLES:
        leg = cone(x, y, 0, LEG_FOOT_DIAMETER, LEG_TOP_DIAMETER, DECK_UNDERSIDE_Z)
        bridge = bridge.union(within_board_outline(leg, 0, DECK_UNDERSIDE_Z))

    bridge = bridge.cut(cylinder(UPPER_HOLE[0], UPPER_HOLE[1], 0, LEG_SCREW_CLEARANCE_DIAMETER, DECK_TOP_Z))
    bridge = bridge.cut(fan_leg_screw_hole())
    for x, y in FAN_SCREWS:
        bridge = bridge.cut(fan_screw_hole(x, y))
    for x, y in TERMINAL_SCREWS:
        bridge = bridge.cut(cylinder(x, y, DECK_UNDERSIDE_Z, SCREWDRIVER_CLEARANCE_DIAMETER, DECK_THICKNESS))
    return bridge


def print_orientation(bridge):
    """Turned over, with the fan seat on the print bed (Z = 0)."""
    return bridge.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, DECK_TOP_Z))


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    name = "TinyFan2350_Fan_Bridge"
    bridge = build_bridge()
    solid = bridge.val()
    size = solid.BoundingBox(tolerance=1e-5)   # measured before meshing, so the size is exact

    cq.exporters.export(bridge, str(folder / (name + ".step")))
    cq.exporters.export(
        print_orientation(bridge), str(folder / (name + ".stl")), tolerance=0.02, angularTolerance=0.1
    )
    print(
        f"wrote {name}: {size.xlen:.2f} x {size.ylen:.2f} x {size.zlen:.2f} mm, "
        f"volume {solid.Volume() / 1000:.1f} cm3, solids {len(bridge.solids().vals())}, valid {solid.isValid()}"
    )
    print(
        f"legs {DECK_UNDERSIDE_Z:.1f} mm, fan seat {DECK_TOP_Z:.1f} mm and fan top "
        f"{DECK_TOP_Z + FAN_THICKNESS:.1f} mm above the PCB; fan centre at X {FAN_CENTRE_X}, Y {FAN_CENTRE_Y}; "
        f"screws M3x{LEG_SCREW_LENGTH:.0f} and M3x{FAN_LEG_SCREW_LENGTH:.0f}"
    )
