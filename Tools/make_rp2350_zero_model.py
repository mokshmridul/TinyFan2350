"""Simplified 3D model of the Waveshare RP2350-Zero for the KiCad 3D view and STEP export.

It replaces the manufacturer's 20 MB STEP with a light one (outline, pads, USB-C, buttons, LED and the
larger chips only). Same origin as before, so the footprint's model offset does not change:
X across the module (0..18 mm, 5V/BOOT side at X = 0), Y along it (0..23.5 mm, USB-C at the +Y end),
Z = 0 is the top face of the module's PCB.

Run with CadQuery 2.x:  python make_rp2350_zero_model.py   ->  ../KiCad/3d/RP2350-Zero.step
"""
from pathlib import Path

import cadquery as cq

WIDTH = 18.0
LENGTH = 23.5
PCB_THICKNESS = 0.8
PAD_INSET = 1.389           # pad row to the long edges
FIRST_PAD_Y = 21.91         # pad 1 (5V), next to the USB-C connector
PAD_PITCH = 2.54

BLUE = cq.Color(0.09, 0.25, 0.55)
GOLD = cq.Color(0.86, 0.69, 0.25)
METAL = cq.Color(0.80, 0.81, 0.83)
BUTTON = cq.Color(0.90, 0.90, 0.88)
DARK = cq.Color(0.08, 0.08, 0.09)
WHITE = cq.Color(0.96, 0.96, 0.94)


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def pad_positions():
    positions = []
    for index in range(9):                                  # 5V, GND, 3V3, GP29 ... GP14
        positions.append((PAD_INSET, FIRST_PAD_Y - PAD_PITCH * index))
    last_row_y = FIRST_PAD_Y - PAD_PITCH * 8
    for index in range(1, 6):                               # GP13 ... GP9
        positions.append((PAD_INSET + PAD_PITCH * index, last_row_y))
    for index in range(9):                                  # GP8 ... GP0
        positions.append((WIDTH - PAD_INSET, last_row_y + PAD_PITCH * index))
    return positions


def build():
    pads = pad_positions()

    board = box(0, WIDTH, 0, LENGTH, -PCB_THICKNESS, 0).edges("|Z").fillet(0.5)
    board = board.faces(">Z").workplane(origin=(0, 0, 0)).pushPoints(pads).hole(1.0)

    rings = cq.Workplane("XY")
    for x, y in pads:
        ring = cq.Workplane("XY").circle(0.85).circle(0.5).extrude(PCB_THICKNESS + 0.04).translate((x, y, -PCB_THICKNESS - 0.02))
        rings = rings.union(ring)

    # USB-C receptacle: shell with the opening at the +Y end
    shell = box(4.51, 13.45, 16.61, 24.57, 0.0, 2.86).edges("|Y").fillet(1.1)
    cavity = box(5.0, 12.96, 18.6, 24.6, 0.45, 2.41).edges("|Y").fillet(0.75)
    tongue = box(5.63, 12.33, 18.6, 23.9, 1.08, 1.78)
    usb = shell.cut(cavity)

    button_bodies = box(3.0, 6.0, 5.22, 9.87, 0.0, 1.6).union(box(12.0, 15.0, 5.22, 9.87, 0.0, 1.6))
    button_caps = (
        cq.Workplane("XY").pushPoints([(4.5, 7.545), (13.5, 7.545)]).circle(0.95).extrude(2.5)
    )

    led = box(8.25, 9.75, 7.14, 8.94, 0.0, 1.0)
    chips = (
        box(8.2, 9.8, 11.2, 14.2, 0.0, 1.15)                                   # regulator
        .union(box(5.53, 12.58, 7.02, 14.07, -PCB_THICKNESS - 0.85, -PCB_THICKNESS))   # RP2350A (underside)
        .union(box(8.54, 11.04, 3.51, 5.51, -PCB_THICKNESS - 0.8, -PCB_THICKNESS))     # flash (underside)
        .union(box(6.15, 8.25, 15.22, 16.83, -PCB_THICKNESS - 1.0, -PCB_THICKNESS))    # crystal (underside)
    )

    assembly = cq.Assembly(name="RP2350-Zero")
    assembly.add(board, name="pcb", color=BLUE)
    assembly.add(rings, name="pads", color=GOLD)
    assembly.add(usb, name="usb_c_shell", color=METAL)
    assembly.add(tongue, name="usb_c_tongue", color=DARK)
    assembly.add(button_bodies, name="button_bodies", color=METAL)
    assembly.add(button_caps, name="button_caps", color=BUTTON)
    assembly.add(led, name="rgb_led", color=WHITE)
    assembly.add(chips, name="chips", color=DARK)
    return assembly


if __name__ == "__main__":
    output = Path(__file__).resolve().parent.parent / "KiCad" / "3d" / "RP2350-Zero.step"
    output.parent.mkdir(parents=True, exist_ok=True)
    build().save(str(output))
    print("wrote", output, "(%d kB)" % (output.stat().st_size // 1024))
