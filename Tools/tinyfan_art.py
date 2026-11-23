"""Flat, outlined illustration toolkit for the TinyFan2350 documentation.

The style follows the pictures of the original TinyFan repository: white sheet, flat colours, black
outlines, ISO technical lettering (osifont) and thin leader lines.

Sheet coordinates are pixels with the origin in the top-left corner (Y down). Board parts are drawn
from layout.json (written by dump_layout.py from the KiCad board), in millimetres from the board's
top-left corner, and placed on a sheet with a Frame.
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, FancyBboxPatch, PathPatch, Polygon, Rectangle
from matplotlib.path import Path as MplPath

HERE = Path(__file__).resolve().parent
LETTERING = FontProperties(fname=str(HERE / "osifont-lgpl3fe.ttf"))
LAYOUT = json.loads((HERE / "layout.json").read_text(encoding="utf-8"))
FOOTPRINTS = {footprint["ref"]: footprint for footprint in LAYOUT["footprints"]}

DPI = 100
INK = "#141414"
BOARD = "#3b3b3d"
BOARD_PRINT = "#f4f4f4"
CREAM = "#f3f0e2"
CREAM_SHADE = "#d9d5c3"
HEADER = "#2a2a2c"
GOLD = "#e3b84f"
TERMINAL = "#7fd39b"
TERMINAL_SHADE = "#3c8f5c"
MODULE = "#234f96"
SILVER = "#d5d7da"
FUSE = "#e2a55c"
RED = "#e02b20"
BLUE = "#1d5fd6"
GREEN = "#2fa33a"
YELLOW = "#f2c318"
WIRE_BLACK = "#2b2b2b"
NOTE = "#555555"

BOARD_LENGTH = 100.0
BOARD_WIDTH = 65.0


# ---------------------------------------------------------------------------------------------
# Sheet and primitives
# ---------------------------------------------------------------------------------------------
def new_sheet(width, height):
    figure = plt.figure(figsize=(width / DPI, height / DPI), dpi=DPI)
    axes = figure.add_axes([0, 0, 1, 1])
    axes.set_xlim(0, width)
    axes.set_ylim(height, 0)
    axes.axis("off")
    figure.patch.set_facecolor("white")
    return figure, axes


def save_sheet(figure, path):
    figure.savefig(str(path), dpi=DPI, facecolor="white")
    plt.close(figure)
    print("wrote", path)


def px_to_pt(pixels):
    return pixels * 72.0 / DPI


def rect(axes, x, y, width, height, fill, radius=0.0, line=1.6, edge=INK, z=3):
    if radius > 0:
        patch = FancyBboxPatch(
            (x + radius, y + radius), width - 2 * radius, height - 2 * radius,
            boxstyle="round,pad=%f,rounding_size=%f" % (radius, radius),
            facecolor=fill, edgecolor=edge, linewidth=line, zorder=z,
        )
    else:
        patch = Rectangle((x, y), width, height, facecolor=fill, edgecolor=edge, linewidth=line, zorder=z)
    axes.add_patch(patch)
    return patch


def circle(axes, x, y, radius, fill, line=1.6, edge=INK, z=3):
    patch = Circle((x, y), radius, facecolor=fill, edgecolor=edge, linewidth=line, zorder=z)
    axes.add_patch(patch)
    return patch


def polygon(axes, points, fill, line=1.6, edge=INK, z=3):
    patch = Polygon(points, closed=True, facecolor=fill, edgecolor=edge, linewidth=line, zorder=z)
    axes.add_patch(patch)
    return patch


def line(axes, points, width=1.3, colour=INK, z=6, style="-"):
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    axes.plot(xs, ys, color=colour, linewidth=width, zorder=z, linestyle=style, solid_capstyle="round")


def label(axes, x, y, content, size=22, ha="left", va="center", colour=INK, z=8, rotation=0):
    """Lettering; size is the approximate capital height in pixels."""
    return axes.text(
        x, y, content, fontproperties=LETTERING, fontsize=px_to_pt(size * 1.45),
        ha=ha, va=va, color=colour, zorder=z, rotation=rotation,
    )


def leader(axes, points, dot=True, z=7):
    """Thin leader line; the first point is on the part and gets a small dot."""
    line(axes, points, width=1.2, z=z)
    if dot:
        circle(axes, points[0][0], points[0][1], 3.2, INK, line=0, z=z)


def curve(axes, points, colour, width=7.0, z=9, outline=True):
    """Smooth wire through the given points (cubic Bezier segments: p0, c1, c2, p1, c1, c2, p1 ...)."""
    codes = [MplPath.MOVETO] + [MplPath.CURVE4] * (len(points) - 1)
    path = MplPath(points, codes)
    if outline:
        axes.add_patch(PathPatch(path, facecolor="none", edgecolor=INK, linewidth=width + 3.0, zorder=z, capstyle="round"))
    axes.add_patch(PathPatch(path, facecolor="none", edgecolor=colour, linewidth=width, zorder=z + 0.1, capstyle="round"))


def arrow(axes, start, end, width=3.0, colour=INK, z=7, head=16):
    axes.annotate(
        "", xy=end, xytext=start, zorder=z,
        arrowprops=dict(arrowstyle="-|>,head_length=%.2f,head_width=%.2f" % (head / 20.0, head / 40.0),
                        color=colour, linewidth=width, shrinkA=0, shrinkB=0, mutation_scale=20),
    )


class Frame:
    """Places board millimetres on the sheet."""

    def __init__(self, x0, y0, scale):
        self.x0 = x0
        self.y0 = y0
        self.scale = scale

    def p(self, x, y):
        return (self.x0 + self.scale * x, self.y0 + self.scale * y)

    def s(self, distance):
        return self.scale * distance


# ---------------------------------------------------------------------------------------------
# Parts (top view)
# ---------------------------------------------------------------------------------------------
def draw_jst(axes, frame, footprint, z=4):
    left, top, right, bottom = footprint["fab"]
    x, y = frame.p(left, top)
    width, height = frame.s(right - left), frame.s(bottom - top)
    rect(axes, x, y, width, height, CREAM, radius=frame.s(0.35), z=z)
    inset = frame.s(0.95)
    rect(axes, x + inset, y + inset, width - 2 * inset, height - 2 * inset, CREAM_SHADE, line=1.1, z=z + 0.1)
    pin = frame.s(0.95)
    for pad in footprint["pads"]:
        pad_x, pad_y = frame.p(*pad["at"])
        rect(axes, pad_x - pin / 2, pad_y - pin / 2, pin, pin, INK, line=0, z=z + 0.2)


def draw_header_cell(axes, frame, at, z=4):
    x, y = frame.p(*at)
    cell = frame.s(2.54)
    rect(axes, x - cell / 2, y - cell / 2, cell, cell, HEADER, radius=frame.s(0.3), line=1.3, z=z)
    pin = frame.s(0.9)
    rect(axes, x - pin / 2, y - pin / 2, pin, pin, GOLD, line=0.9, z=z + 0.1)


def draw_header(axes, frame, footprint, z=4):
    for pad in footprint["pads"]:
        draw_header_cell(axes, frame, pad["at"], z=z)


def draw_jumper_cap(axes, frame, first, second, colour, z=5):
    """Jumper cap bridging two neighbouring header pins (board mm)."""
    x1, y1 = frame.p(*first)
    x2, y2 = frame.p(*second)
    half = frame.s(1.22)
    left, right = min(x1, x2) - half, max(x1, x2) + half
    top, bottom = min(y1, y2) - half, max(y1, y2) + half
    rect(axes, left, top, right - left, bottom - top, colour, radius=frame.s(0.35), line=1.5, z=z)
    inset = frame.s(0.5)
    rect(
        axes, left + inset, top + inset, right - left - 2 * inset, bottom - top - 2 * inset,
        "none", radius=frame.s(0.25), line=1.2, edge="#ffffff", z=z + 0.1,
    )
    grip = frame.s(0.8)
    rect(axes, (x1 + x2) / 2 - grip / 2, (y1 + y2) / 2 - grip / 2, grip, grip, HEADER, line=0.8, z=z + 0.2)


def draw_terminal(axes, frame, footprint, z=4):
    """Screw terminal; the wire entry is on the side nearest the board edge (left)."""
    left, top, right, bottom = footprint["fab"]
    x, y = frame.p(left, top)
    width, height = frame.s(right - left), frame.s(bottom - top)
    rect(axes, x, y, width, height, TERMINAL, z=z)
    shade = frame.s(3.1)
    rect(axes, x + width - shade, y, shade, height, TERMINAL_SHADE, line=1.3, z=z + 0.1)
    line(axes, [(x, y + height / 2), (x + width - shade, y + height / 2)], width=1.1, z=z + 0.2)
    for pad in footprint["pads"]:
        pad_x, pad_y = frame.p(*pad["at"])
        radius = frame.s(1.85)
        circle(axes, pad_x, pad_y, radius, "#ffffff", line=1.4, z=z + 0.3)
        line(axes, [(pad_x - radius * 0.72, pad_y), (pad_x + radius * 0.72, pad_y)], width=1.6, z=z + 0.4)


def draw_fuse_holder(axes, frame, footprint, text_on_fuse="5A", z=4):
    left, top, right, bottom = footprint["fab"]
    x, y = frame.p(left, top)
    width, height = frame.s(right - left), frame.s(bottom - top)
    rect(axes, x, y, width, height, HEADER, radius=frame.s(0.4), z=z)
    fuse_width, fuse_height = frame.s(3.9), frame.s(10.9)
    fuse_x, fuse_y = x + (width - fuse_width) / 2, y + (height - fuse_height) / 2
    rect(axes, fuse_x, fuse_y, fuse_width, fuse_height, FUSE, radius=frame.s(0.5), line=1.3, z=z + 0.1)
    if text_on_fuse and frame.scale >= 9:
        label(
            axes, fuse_x + fuse_width / 2, fuse_y + fuse_height / 2, text_on_fuse,
            size=frame.s(1.9), ha="center", rotation=90, z=z + 0.2,
        )


def draw_capacitor(axes, frame, footprint, z=4):
    left, top, right, bottom = footprint["fab"]
    centre_x, centre_y = frame.p((left + right) / 2, (top + bottom) / 2)
    radius = frame.s((right - left) / 2)
    circle(axes, centre_x, centre_y, radius, "#3d63c4", z=z)
    circle(axes, centre_x, centre_y, radius * 0.7, SILVER, line=1.1, z=z + 0.1)
    line(axes, [(centre_x - radius * 0.45, centre_y), (centre_x + radius * 0.45, centre_y)], width=1.1, z=z + 0.2)


def draw_module(axes, frame, footprint, highlight=None, z=4):
    """Waveshare RP2350-Zero as it sits on the TinyFan2350: USB-C to the left, GP0-GP8 along the top."""
    left, top, right, bottom = footprint["fab"]
    body_left = right - 23.5
    x, y = frame.p(body_left, top)
    width, height = frame.s(23.5), frame.s(bottom - top)
    rect(axes, x, y, width, height, MODULE, radius=frame.s(0.5), z=z)
    for pad in footprint["pads"]:
        pad_x, pad_y = frame.p(*pad["at"])
        circle(axes, pad_x, pad_y, frame.s(0.85), GOLD, line=1.0, z=z + 0.1)
        circle(axes, pad_x, pad_y, frame.s(0.4), "#0f2a55", line=0, z=z + 0.2)
    middle = (top + bottom) / 2
    usb_x, usb_y = frame.p(left, middle - 4.47)
    rect(axes, usb_x, usb_y, frame.s(7.4), frame.s(8.94), SILVER, radius=frame.s(0.9), z=z + 0.3)
    line(axes, [frame.p(left + 2.0, middle - 1.5), frame.p(left + 2.0, middle + 1.5)], width=1.6, z=z + 0.4)
    line(axes, [frame.p(left + 3.4, middle - 1.5), frame.p(left + 3.4, middle + 1.5)], width=1.6, z=z + 0.4)
    regulator_x, regulator_y = frame.p(body_left + 9.3, middle - 0.8)
    rect(axes, regulator_x, regulator_y, frame.s(3.0), frame.s(1.6), INK, line=0, z=z + 0.3)
    buttons = module_buttons(footprint)
    for name, (button_x, button_y) in buttons.items():
        centre_x, centre_y = frame.p(button_x, button_y)
        long_side, short_side = frame.s(4.65), frame.s(3.0)
        fill = "#ffe04a" if highlight == name else "#eeeeee"
        rect(
            axes, centre_x - long_side / 2, centre_y - short_side / 2, long_side, short_side, fill,
            radius=frame.s(0.3), line=1.3, z=z + 0.3,
        )
        circle(axes, centre_x, centre_y, frame.s(0.95), "#ffffff", line=1.2, z=z + 0.4)
    led_x, led_y = frame.p(body_left + 15.46, middle)
    rect(axes, led_x - frame.s(0.9), led_y - frame.s(0.75), frame.s(1.8), frame.s(1.5), "#ffffff", line=1.0, z=z + 0.3)


def module_buttons(footprint):
    """Board-mm centres of the two buttons: RUN (reset) on the GP0-GP8 side, BOOT on the 5V side."""
    left, top, right, bottom = footprint["fab"]
    body_left = right - 23.5
    return {
        "RUN": (body_left + 15.95, top + 4.5),
        "BOOT": (body_left + 15.95, bottom - 4.5),
    }


def draw_hole(axes, frame, footprint, z=4):
    x, y = frame.p(*footprint["at"])
    circle(axes, x, y, frame.s(1.6), "#ffffff", line=1.6, z=z)


def draw_part(axes, frame, footprint, z=4):
    package = footprint["package"]
    if package.startswith("JST_XH"):
        draw_jst(axes, frame, footprint, z=z)
    elif package.startswith("PinHeader"):
        draw_header(axes, frame, footprint, z=z)
    elif package.startswith("TerminalBlock"):
        draw_terminal(axes, frame, footprint, z=z)
    elif package.startswith("Fuseholder"):
        draw_fuse_holder(axes, frame, footprint, z=z)
    elif package.startswith("CP_Radial"):
        draw_capacitor(axes, frame, footprint, z=z)
    elif package.startswith("Waveshare"):
        draw_module(axes, frame, footprint, z=z)
    elif package.startswith("MountingHole"):
        draw_hole(axes, frame, footprint, z=z)


# Jumper positions used in the pictures: fans in 4-pin mode on VIN, LED ports on 5V
FAN_MODE_JUMPERS = ["JP6", "JP7", "JP8", "JP9", "JP10"]
FAN_VOLT_JUMPERS = ["JP1", "JP2", "JP3", "JP4", "JP5"]
LED_VOLT_JUMPERS = ["JP11", "JP12"]


def jumper_pads(reference, upper=True):
    pads = sorted(FOOTPRINTS[reference]["pads"], key=lambda pad: pad["at"][1])
    pair = pads[:2] if upper else pads[1:]
    return pair[0]["at"], pair[1]["at"]


def draw_default_jumpers(axes, frame, z=5):
    for reference in FAN_MODE_JUMPERS:
        draw_jumper_cap(axes, frame, *jumper_pads(reference, upper=True), colour=BLUE, z=z)
    for reference in FAN_VOLT_JUMPERS:
        draw_jumper_cap(axes, frame, *jumper_pads(reference, upper=True), colour=RED, z=z)
    for reference in LED_VOLT_JUMPERS:
        draw_jumper_cap(axes, frame, *jumper_pads(reference, upper=False), colour=RED, z=z)


def draw_board(axes, frame, jumpers=True, silk=True, only=None, z=2):
    """Whole board, top view. `only` limits the parts to the given references."""
    x, y = frame.p(0, 0)
    rect(axes, x, y, frame.s(BOARD_LENGTH), frame.s(BOARD_WIDTH), BOARD, radius=frame.s(2.0), line=2.2, z=z)
    for footprint in LAYOUT["footprints"]:
        if not footprint["top"]:
            continue
        if only is not None and footprint["ref"] not in only:
            continue
        draw_part(axes, frame, footprint, z=z + 2)
    if jumpers:
        draw_default_jumpers(axes, frame, z=z + 3)
    if silk:
        draw_silk(axes, frame, z=z + 1)


def draw_silk(axes, frame, z=3, longest=14, minimum_px=9.0, region=None):
    """The board's own white print, where it is large enough to read.

    region = (left, top, right, bottom) in board mm keeps only the print inside that window.
    """
    for item in LAYOUT["silk"]:
        content = item["text"]
        size = frame.s(item["size"]) * 0.95
        if len(content) > longest or size < minimum_px or content in ("+", "-"):
            continue
        if region is not None:
            inside_x = region[0] + 1.0 <= item["at"][0] <= region[2] - 1.0
            inside_y = region[1] + 0.6 <= item["at"][1] <= region[3] - 0.6
            if not (inside_x and inside_y):
                continue
        x, y = frame.p(*item["at"])
        label(axes, x, y, content, size=size, ha="center", colour=BOARD_PRINT, z=z, rotation=item["angle"])


def draw_board_piece(axes, frame, region, references, silk=True, z=2):
    """A rectangular cut-out of the board (board mm window) with the listed parts on it."""
    left, top, right, bottom = region
    x, y = frame.p(left, top)
    rect(axes, x, y, frame.s(right - left), frame.s(bottom - top), BOARD, radius=frame.s(0.8), line=2.0, z=z)
    for reference in references:
        draw_part(axes, frame, FOOTPRINTS[reference], z=z + 2)
    if silk:
        draw_silk(axes, frame, z=z + 1, region=region)


def frame_for(reference, x, y, scale):
    """Frame that puts the top-left corner of a part's outline at sheet position (x, y)."""
    left, top, _, _ = FOOTPRINTS[reference]["fab"]
    return Frame(x - scale * left, y - scale * top, scale)


def pad_position(reference, number):
    for pad in FOOTPRINTS[reference]["pads"]:
        if pad["number"] == str(number):
            return pad["at"]
    raise KeyError((reference, number))


def code_text(axes, x, y, content, size=17, colour="#ffffff", ha="left", z=9):
    """Monospaced text for commands."""
    return axes.text(
        x, y, content, family="DejaVu Sans Mono", fontsize=px_to_pt(size),
        ha=ha, va="center", color=colour, zorder=z,
    )


def terminal_strip(axes, x, y, width, lines, size=17, z=8):
    """Dark rounded box with shell commands; returns the box height."""
    height = 22 + len(lines) * (size + 12)
    rect(axes, x, y, width, height, "#22262b", radius=9, line=1.6, z=z)
    for index, content in enumerate(lines):
        code_text(axes, x + 18, y + 11 + (size + 12) * (index + 0.5), content, size=size, z=z + 1)
    return height
