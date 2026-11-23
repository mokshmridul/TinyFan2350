"""Draw the documentation pictures of the TinyFan2350 (pinout, jumpers, wiring, flashing).

Run after a board change:
    1. <KiCad python>  dump_layout.py          (reads ../../TinyFan2350.kicad_pcb, writes layout.json)
    2. python          make_illustrations.py   (needs matplotlib; writes the PNG files into ../)
"""
from pathlib import Path

import tinyfan_art as art
from tinyfan_art import BLUE, GREEN, INK, NOTE, RED, YELLOW, WIRE_BLACK

IMAGES = Path(__file__).resolve().parent.parent

FAN_PORTS = ["J3", "J4", "J5", "J6", "J7"]
LED_PORTS = ["J8", "J9"]
THERMISTOR_PORTS = ["J10", "J11", "J12", "J13"]


def title(axes, width, content):
    art.label(axes, width / 2, 62, content, size=46, ha="center")


# ---------------------------------------------------------------------------------------------
# Pinout
# ---------------------------------------------------------------------------------------------
def make_pinout():
    width, height = 2000, 1400
    figure, axes = art.new_sheet(width, height)
    title(axes, width, "TinyFan2350 Pinout")

    frame = art.Frame(450, 330, 11)
    art.draw_board(axes, frame)

    # Fan ports along the top edge
    for index, reference in enumerate(FAN_PORTS):
        left, top, right, _ = art.FOOTPRINTS[reference]["fab"]
        centre_x, top_y = frame.p((left + right) / 2, top)
        art.label(axes, centre_x, 222, "FAN%d" % (index + 1), size=27, ha="center")
        art.label(axes, centre_x, 257, "PWM  GP%d" % (2 * index), size=15, ha="center")
        art.label(axes, centre_x, 281, "TACH  GP%d" % (2 * index + 1), size=15, ha="center")
        art.leader(axes, [(centre_x, top_y + 14), (centre_x, 297)])

    # Fan port detail, top right
    detail = art.frame_for("J7", 1670, 128, 15)
    art.draw_jst(axes, detail, art.FOOTPRINTS["J7"])
    art.label(axes, 1714, 100, "Fan port", size=22, ha="center")
    for number, name in [(1, "GND"), (2, "V+"), (3, "TACH"), (4, "PWM")]:
        pad_x, pad_y = detail.p(*art.pad_position("J7", number))
        art.leader(axes, [(pad_x, pad_y), (1780, pad_y)], dot=False)
        art.label(axes, 1788, pad_y, "%d  %s" % (number, name), size=17)
    fan5_left, fan5_top, fan5_right, fan5_bottom = art.FOOTPRINTS["J7"]["fab"]
    art.leader(axes, [frame.p(fan5_right, fan5_top + 3.0), (1670, 200)])
    art.label(axes, 1670, 345, "V+ = VIN or 5V (VOLT jumper)", size=14, colour=NOTE)

    # LED ports on the right edge
    for index, reference in enumerate(LED_PORTS):
        left, top, right, bottom = art.FOOTPRINTS[reference]["fab"]
        edge_x, centre_y = frame.p(right, (top + bottom) / 2)
        art.leader(axes, [(edge_x - 10, centre_y), (1585, centre_y)])
        art.label(axes, 1595, centre_y - 17, "LED%d" % (index + 1), size=27)
        art.label(axes, 1595, centre_y + 17, "1 GND   2 V+   3 DATA  GP%d" % (10 + index), size=15)

    # Thermistor ports along the bottom edge
    for index, reference in enumerate(THERMISTOR_PORTS):
        left, _, right, bottom = art.FOOTPRINTS[reference]["fab"]
        centre_x, bottom_y = frame.p((left + right) / 2, bottom)
        art.leader(axes, [(centre_x, bottom_y - 12), (centre_x, 1068)])
        art.label(axes, centre_x, 1090, "TH%d" % (index + 1), size=27, ha="center")
        art.label(axes, centre_x, 1123, "GP%d" % (26 + index), size=15, ha="center")
    art.label(
        axes, frame.p(55.75, 0)[0], 1162, "TH pins:  1 = signal,  2 = GND   (4.7k pull-up to 3.3V on the board)",
        size=15, ha="center", colour=NOTE,
    )

    # EXP header detail, top left
    cell = 2.54
    exp = art.Frame(86, 218, 20)
    exp_names = ["GND", "3V3", "GP12", "GP13", "GP14", "GP15"]
    for index, name in enumerate(exp_names):
        art.draw_header_cell(axes, exp, (index * cell, 0))
        art.label(axes, exp.p(index * cell, 0)[0], 262, name, size=15, ha="center")
    art.label(axes, 61, 172, "EXP header", size=22)
    art.label(axes, 61, 262, "1", size=13, ha="right", colour=NOTE)
    exp_left, exp_top, exp_right, _ = art.FOOTPRINTS["J14"]["fab"]
    exp_x, exp_y = frame.p((exp_left + exp_right) / 2, exp_top + 0.6)
    art.leader(axes, [(exp_x, exp_y), (exp_x, 296), (372, 232)])

    # MCU module and USB
    module_left, module_top, _, module_bottom = art.FOOTPRINTS["U1"]["fab"]
    art.label(axes, 40, 432, "Waveshare RP2350-Zero", size=20)
    art.label(axes, 40, 460, "(plugged into a socket)", size=15, colour=NOTE)
    art.leader(axes, [frame.p(module_left + 3.4, module_top + 1.6), (330, 446)])
    art.label(axes, 330, 520, "USB-C", size=20, ha="right")
    art.leader(axes, [frame.p(module_left + 0.9, (module_top + module_bottom) / 2 + 2.2), (340, 520)])

    # Power input detail, left
    power = art.frame_for("J1", 232, 650, 21)
    for reference in ("J1", "J2"):
        art.draw_terminal(axes, power, art.FOOTPRINTS[reference])
    art.label(axes, 336, 622, "Power in", size=22, ha="center")
    power_names = [("J1", 1, "GND (-)"), ("J1", 2, "VIN 12-24V (+)"), ("J2", 1, "GND (-)"), ("J2", 2, "5V (+)")]
    for reference, number, name in power_names:
        _, pad_y = power.p(*art.pad_position(reference, number))
        art.leader(axes, [(232, pad_y), (215, pad_y)], dot=False)
        art.label(axes, 207, pad_y, name, size=18, ha="right")
    j1 = art.FOOTPRINTS["J1"]["fab"]
    j2 = art.FOOTPRINTS["J2"]["fab"]
    art.leader(axes, [power.p(j1[2], j1[1]), frame.p(j1[0], j1[1])], dot=False)
    art.leader(axes, [power.p(j2[2], j2[3]), frame.p(j2[0], j2[3])], dot=False)
    art.label(axes, 40, 1215, "+ is the lower screw of each terminal", size=16, colour=NOTE)
    art.label(axes, 40, 1245, "F1 / F2: mini blade fuses, 5A max", size=16, colour=NOTE)

    # Jumper legend, bottom right
    art.label(axes, 1500, 1090, "Jumpers", size=24)
    art.label(axes, 1500, 1372, "per fan: MODE + VOLT      per LED port: VOLT", size=14, colour=NOTE)
    legend = [
        (1135, BLUE, "MODE", "upper = 4P :  4-pin PWM fan", "lower = 2/3 :  2-pin or 3-pin fan"),
        (1262, RED, "VOLT", "upper = VIN :  12V / 24V input", "lower = 5V :  5V input"),
    ]
    for top_y, colour, name, upper_text, lower_text in legend:
        jumper = art.Frame(1528, top_y, 15)
        for row in range(3):
            art.draw_header_cell(axes, jumper, (0, row * cell))
        art.draw_jumper_cap(axes, jumper, (0, 0), (0, cell), colour)
        art.label(axes, 1570, top_y - 2, name, size=19)
        art.label(axes, 1570, top_y + 34, upper_text, size=15)
        art.label(axes, 1570, top_y + 64, lower_text, size=15)

    art.save_sheet(figure, IMAGES / "TinyFan2350_Pinout.png")


# ---------------------------------------------------------------------------------------------
# Jumpers
# ---------------------------------------------------------------------------------------------
def option_card(axes, x, y, colour, upper, print_upper, print_lower, heading, lines):
    """One jumper position: a 3-pin header on a piece of board, plus its meaning."""
    card_width, card_height = 690, 372
    art.rect(axes, x, y, card_width, card_height, "#fafafa", radius=14, line=1.4, edge="#9a9a9a", z=1)
    art.rect(axes, x + 28, y + 22, 190, 328, art.BOARD, radius=10, line=1.8, z=2)
    header = art.Frame(x + 123, y + 110, 30)
    cell = 2.54
    for row in range(3):
        art.draw_header_cell(axes, header, (0, row * cell))
    first, second = ((0, 0), (0, cell)) if upper else ((0, cell), (0, 2 * cell))
    art.draw_jumper_cap(axes, header, first, second, colour)
    art.label(axes, x + 123, y + 47, print_upper, size=20, ha="center", colour=art.BOARD_PRINT)
    art.label(axes, x + 123, y + 326, print_lower, size=20, ha="center", colour=art.BOARD_PRINT)
    art.label(axes, x + 250, y + 66, heading, size=25)
    for index, content in enumerate(lines):
        is_code = content.startswith("  ")
        if is_code:
            art.code_text(axes, x + 262, y + 126 + index * 38, content.strip(), size=18, colour=INK)
        else:
            art.label(axes, x + 250, y + 126 + index * 38, content, size=17)


def make_jumpers():
    width, height = 2000, 1200
    figure, axes = art.new_sheet(width, height)
    title(axes, width, "TinyFan2350 Jumpers")

    # One fan channel, enlarged
    region = (29.6, 0.6, 42.4, 29.0)
    channel = art.Frame(110 - 26 * region[0], 150 - 26 * region[1], 26)
    art.draw_board_piece(axes, channel, region, ["J3", "JP6", "JP1"])
    art.draw_jumper_cap(axes, channel, *art.jumper_pads("JP6", upper=True), colour=BLUE)
    art.draw_jumper_cap(axes, channel, *art.jumper_pads("JP1", upper=True), colour=RED)
    art.label(axes, 276, 122, "One fan channel (FAN1)", size=20, ha="center")
    mode_x, mode_y = channel.p(*art.pad_position("JP6", 3))
    volt_x, volt_y = channel.p(*art.pad_position("JP1", 3))
    art.leader(axes, [(mode_x, mode_y + 62), (170, 962)], dot=False)
    art.leader(axes, [(volt_x, volt_y + 62), (385, 962)], dot=False)
    art.label(axes, 170, 988, "MODE jumper", size=21, ha="center")
    art.label(axes, 170, 1018, "(left, blue)", size=15, ha="center", colour=NOTE)
    art.label(axes, 385, 988, "VOLT jumper", size=21, ha="center")
    art.label(axes, 385, 1018, "(right, red)", size=15, ha="center", colour=NOTE)

    # The four positions
    art.label(axes, 570, 124, "MODE jumper  -  what kind of fan", size=22)
    art.label(axes, 1280, 124, "VOLT jumper  -  which supply", size=22)
    option_card(
        axes, 560, 150, BLUE, True, "4P", "2/3", "4P  =  4-pin PWM fan",
        ["Fan GND is always connected,", "the MOSFET pulls the PWM wire.", "In Klipper:",
         "  pin: !tinyfan:FAN1_PWM", "  cycle_time: 0.00004"],
    )
    option_card(
        axes, 560, 545, BLUE, False, "4P", "2/3", "2/3  =  2- or 3-pin fan",
        ["The MOSFET switches the fan GND.", "", "In Klipper:",
         "  pin: tinyfan:FAN1_PWM", "  cycle_time: 0.01"],
    )
    option_card(
        axes, 1270, 150, RED, True, "VIN", "5V", "VIN  =  12V or 24V",
        ["The port is fed from the VIN input,", "so it gets whatever you connect", "there: 12V or 24V.", "",
         "12V / 24V fans, 12V LED strips"],
    )
    option_card(
        axes, 1270, 545, RED, False, "VIN", "5V", "5V  =  5V input",
        ["The port is fed from the 5V input.", "", "", "",
         "5V fans, WS2812B / SK6812 strips"],
    )

    # Warnings
    art.rect(axes, 560, 945, 1400, 215, "#fff4f2", radius=14, line=1.8, edge=RED, z=1)
    art.label(axes, 590, 987, "Set every jumper BEFORE power-on!", size=27, colour=RED)
    art.label(axes, 590, 1034, "A 5V fan or a 5V LED strip on VIN (12V / 24V) will be destroyed  -  check twice.", size=18)
    art.label(axes, 590, 1074, "No MODE jumper = the fan never runs.     No VOLT jumper = the port has no power.", size=18)
    art.label(axes, 590, 1114, "LED1 and LED2 only have a VOLT jumper.", size=18)

    art.save_sheet(figure, IMAGES / "TinyFan2350_Jumpers.png")


# ---------------------------------------------------------------------------------------------
# Wiring
# ---------------------------------------------------------------------------------------------
def fan_icon(axes, x, y, radius):
    art.rect(axes, x - radius, y - radius, 2 * radius, 2 * radius, "#4a4a4c", radius=radius * 0.22, line=1.6, z=4)
    art.circle(axes, x, y, radius * 0.86, "#e9e9e9", line=1.4, z=4.1)
    import math

    for blade in range(5):
        angle = 2 * math.pi * blade / 5
        tip = (x + radius * 0.78 * math.cos(angle), y + radius * 0.78 * math.sin(angle))
        side = (x + radius * 0.6 * math.cos(angle + 0.75), y + radius * 0.6 * math.sin(angle + 0.75))
        art.polygon(axes, [(x, y), tip, side], "#9a9a9a", line=1.1, z=4.2)
    art.circle(axes, x, y, radius * 0.3, "#4a4a4c", line=1.3, z=4.3)


def fan_case(axes, x, y, wires, heading, lines):
    """A fan port with the plugged wires; wires = list of (pin number, colour)."""
    port = art.frame_for("J3", x + 92, y, 16)
    art.draw_jst(axes, port, art.FOOTPRINTS["J3"])
    names = {1: "1  GND", 2: "2  V+", 3: "3  TACH", 4: "4  PWM"}
    used = {number for number, _ in wires}
    fan_x, fan_y = x + 284, y + 100
    for number in (1, 2, 3, 4):
        pad_x, pad_y = port.p(*art.pad_position("J3", number))
        art.label(axes, x + 82, pad_y, names[number], size=15, ha="right", colour=INK if number in used else "#b0b0b0")
    for number, colour in wires:
        pad_x, pad_y = port.p(*art.pad_position("J3", number))
        end_y = fan_y - 24 + 16 * (number - 1)
        art.curve(
            axes, [(pad_x, pad_y), (pad_x + 60, pad_y), (fan_x - 110, end_y), (fan_x - 40, end_y)],
            colour, width=5.5, z=5,
        )
    fan_icon(axes, fan_x, fan_y, 48)
    art.label(axes, x + 10, y + 250, heading, size=23)
    for index, content in enumerate(lines):
        art.label(axes, x + 10, y + 290 + index * 30, content, size=16)


def make_wiring():
    width, height = 2000, 1330
    figure, axes = art.new_sheet(width, height)
    title(axes, width, "TinyFan2350 Wiring")

    # --- power ---------------------------------------------------------------------------
    art.label(axes, 40, 150, "Power inputs", size=28)
    region = (0.0, 27.2, 31.0, 65.0)
    power = art.Frame(330, 195 - 17 * region[1], 17)
    art.draw_board_piece(axes, power, region, ["J1", "J2", "C1", "C2", "F1", "F2", "H3"])
    supply = [
        ("J1", 1, BLUE, "GND"),
        ("J1", 2, RED, "+12V  or  +24V"),
        ("J2", 1, BLUE, "GND"),
        ("J2", 2, RED, "+5V"),
    ]
    for reference, number, colour, name in supply:
        pad_x, pad_y = power.p(*art.pad_position(reference, number))
        entry_x = power.p(art.FOOTPRINTS[reference]["fab"][0], 0)[0]
        art.curve(
            axes, [(40, pad_y + 26), (150, pad_y + 26), (170, pad_y), (entry_x - 62, pad_y)],
            colour, width=8.0, z=5,
        )
        art.rect(axes, entry_x - 66, pad_y - 10, 42, 20, colour, radius=4, line=1.5, z=6)
        art.rect(axes, entry_x - 24, pad_y - 5, 26, 10, art.SILVER, line=1.3, z=6)
        art.label(axes, 46, pad_y - 6, name, size=19)
    notes = [
        "VIN takes 12V or 24V. The board does not convert voltages:",
        "VIN ports get what you feed into VIN, 5V ports need the 5V input.",
        "+ is the lower screw of each terminal, GND the upper one.",
        "F1 / F2 are mini blade fuses, 5A max. Wrong polarity blows the fuse.",
    ]
    for index, content in enumerate(notes):
        art.label(axes, 40, 900 + index * 34, content, size=17)

    art.rect(axes, 40, 1060, 830, 228, "#fff9e6", radius=14, line=1.6, edge="#c9a227", z=1)
    art.label(axes, 66, 1100, "Before the first power-up", size=24)
    checklist = [
        "1.  Every used port has its jumpers set (see the jumper picture).",
        "2.  Polarity checked on both terminals with a multimeter.",
        "3.  Fuses fitted - the smallest that covers your load (5 fans x 0.6A = 3A).",
        "4.  RP2350-Zero in its socket, USB-C pointing off the board edge.",
    ]
    for index, content in enumerate(checklist):
        art.label(axes, 66, 1146 + index * 34, content, size=16)

    # --- fans -----------------------------------------------------------------------------
    art.label(axes, 950, 150, "Fan ports  (FAN1 - FAN5)", size=28)
    fan_case(
        axes, 940, 205, [(1, WIRE_BLACK), (2, RED), (3, YELLOW), (4, BLUE)],
        "4-pin PWM fan", ["MODE jumper: 4P", "speed control and RPM", "at every speed"],
    )
    fan_case(
        axes, 1280, 205, [(1, WIRE_BLACK), (2, RED), (3, YELLOW)],
        "3-pin fan", ["MODE jumper: 2/3", "RPM reading is only", "valid at 100%"],
    )
    fan_case(
        axes, 1620, 205, [(1, WIRE_BLACK), (2, RED)],
        "2-pin fan", ["MODE jumper: 2/3", "plug sits on pins 1-2"],
    )
    art.label(axes, 950, 620, "max 0.6A per fan.  VOLT jumper: VIN for 12V / 24V fans, 5V for 5V fans.", size=17, colour=NOTE)

    # --- LED strip ------------------------------------------------------------------------
    art.label(axes, 950, 720, "LED ports  (LED1, LED2)", size=28)
    led = art.frame_for("J8", 1042, 770, 16)
    art.draw_jst(axes, led, art.FOOTPRINTS["J8"])
    strip_x, strip_y = 1300, 800
    art.rect(axes, strip_x, strip_y, 330, 60, "#f1f1f1", radius=6, line=1.6, z=4)
    for pixel in range(5):
        art.rect(axes, strip_x + 28 + pixel * 62, strip_y + 14, 32, 32, "#ffffff", radius=4, line=1.3, z=4.1)
        art.circle(axes, strip_x + 44 + pixel * 62, strip_y + 30, 9, [RED, GREEN, BLUE, YELLOW, RED][pixel], line=1.0, z=4.2)
    led_wires = [(1, WIRE_BLACK, "1  GND"), (2, RED, "2  V+"), (3, GREEN, "3  DATA")]
    for number, colour, name in led_wires:
        pad_x, pad_y = led.p(*art.pad_position("J8", number))
        end_y = strip_y + 12 + 18 * (number - 1)
        art.curve(axes, [(pad_x, pad_y), (pad_x + 70, pad_y), (strip_x - 90, end_y), (strip_x, end_y)], colour, width=5.5, z=5)
        art.label(axes, 1032, pad_y, name, size=15, ha="right")
    led_notes = [
        "Addressable strips: WS2812B, SK6812 (5V), WS2811 (12V).",
        "VOLT jumper: 5V for 5V strips, VIN for 12V strips.",
        "Data is level-shifted to 5V.  max 3A per port.",
    ]
    for index, content in enumerate(led_notes):
        art.label(axes, 950, 975 + index * 30, content, size=16)

    # --- thermistor -----------------------------------------------------------------------
    art.label(axes, 950, 1100, "Thermistor ports  (TH1 - TH4)", size=28)
    thermistor = art.frame_for("J10", 1010, 1150, 16)
    art.draw_jst(axes, thermistor, art.FOOTPRINTS["J10"])
    bead_x, bead_y = 1420, 1197
    for number, offset in [(1, -9), (2, 9)]:
        pad_x, pad_y = thermistor.p(*art.pad_position("J10", number))
        art.curve(
            axes, [(pad_x, pad_y), (pad_x, pad_y - 70 - 25 * number), (bead_x - 190, bead_y + offset), (bead_x - 8, bead_y + offset)],
            "#f1f1f1", width=4.5, z=5,
        )
    art.circle(axes, bead_x + 6, bead_y, 17, "#3a3a3c", line=1.6, z=6)
    art.label(axes, 1470, 1180, "NTC 100k thermistor", size=17)
    art.label(axes, 1470, 1212, "(polarity does not matter)", size=15, colour=NOTE)
    art.label(axes, 950, 1275, "pin 1 = signal, pin 2 = GND.  Keep the wires away from 12V / 24V wiring.", size=16)

    art.save_sheet(figure, IMAGES / "TinyFan2350_Wiring.png")


# ---------------------------------------------------------------------------------------------
# Flashing
# ---------------------------------------------------------------------------------------------
def step_card(axes, x, y, width, number, heading, lines, commands, result):
    art.rect(axes, x, y, width, 292, "#fafafa", radius=14, line=1.4, edge="#9a9a9a", z=1)
    art.circle(axes, x + 46, y + 48, 27, INK, line=0, z=3)
    art.label(axes, x + 46, y + 47, str(number), size=27, ha="center", colour="#ffffff")
    art.label(axes, x + 92, y + 48, heading, size=27)
    for index, content in enumerate(lines):
        art.label(axes, x + 30, y + 102 + index * 30, content, size=17)
    strip_y = y + 92 + len(lines) * 30
    strip_height = art.terminal_strip(axes, x + 26, strip_y, width - 52, commands, size=16)
    art.label(axes, x + 30, strip_y + strip_height + 30, result, size=17, colour=GREEN)


def make_flashing():
    width, height = 2000, 1240
    figure, axes = art.new_sheet(width, height)
    title(axes, width, "Flashing: Katapult + Klipper")

    # The module with its two buttons
    module = art.frame_for("U1", 150, 250, 20)
    footprint = art.FOOTPRINTS["U1"]
    art.draw_module(axes, module, footprint, highlight="BOOT")
    buttons = art.module_buttons(footprint)
    art.label(axes, 395, 196, "Waveshare RP2350-Zero", size=22, ha="center")
    boot_x, boot_y = module.p(*buttons["BOOT"])
    run_x, run_y = module.p(*buttons["RUN"])
    art.leader(axes, [(boot_x, boot_y + 36), (boot_x, 700)], dot=False)
    art.label(axes, boot_x, 728, "BOOT", size=27, ha="center")
    art.label(axes, boot_x, 762, "hold it while plugging in", size=15, ha="center", colour=NOTE)
    art.leader(axes, [(run_x + 36, run_y), (600, run_y), (650, 700)], dot=False)
    art.label(axes, 650, 728, "RUN", size=27, ha="center")
    art.label(axes, 650, 762, "= reset", size=15, ha="center", colour=NOTE)
    usb_y = module.p(0, (footprint["fab"][1] + footprint["fab"][3]) / 2)[1]
    art.curve(axes, [(20, usb_y + 40), (70, usb_y + 40), (80, usb_y), (148, usb_y)], "#4a4a4c", width=16, z=3)
    art.label(axes, 20, usb_y + 82, "USB to the Pi", size=16)

    art.rect(axes, 40, 860, 650, 300, "#fff9e6", radius=14, line=1.6, edge="#c9a227", z=1)
    art.label(axes, 66, 902, "Good to know", size=24)
    hints = [
        "Double-click RUN (twice within half a second):",
        "the board waits in Katapult for a firmware.",
        "It then shows up as  usb-katapult_rp2350_...",
        "",
        "The RGB LED on the module cannot be used",
        "as Katapult status LED - leave that option off.",
    ]
    for index, content in enumerate(hints):
        art.label(axes, 66, 948 + index * 32, content, size=16)

    # The three steps
    card_x, card_width = 760, 1200
    step_card(
        axes, card_x, 150, card_width, 1, "Flash Katapult  (once)",
        ["Hold BOOT and plug the board into the Pi.  lsusb shows  2e8a:000f RP2350 Boot."],
        ["cd ~/katapult && make menuconfig && make", "make flash"],
        "->  /dev/serial/by-id/usb-katapult_rp2350_XXXX-if00",
    )
    step_card(
        axes, card_x, 482, card_width, 2, "Flash Klipper through Katapult",
        ["Build Klipper with  Bootloader offset = 16KiB bootloader."],
        ["cd ~/klipper && make menuconfig && make",
         "python3 ~/katapult/scripts/flashtool.py -d /dev/serial/by-id/usb-katapult_rp2350_XXXX-if00"],
        "->  /dev/serial/by-id/usb-Klipper_rp2350_XXXX-if00      (goes into TinyFan2350.cfg)",
    )
    step_card(
        axes, card_x, 814, card_width, 3, "Later updates  -  no buttons",
        ["The flash tool restarts Klipper into Katapult, uploads and starts it again."],
        ["cd ~/klipper && git pull && make clean && make",
         "python3 ~/katapult/scripts/flashtool.py -d /dev/serial/by-id/usb-Klipper_rp2350_XXXX-if00"],
        "->  /dev/serial/by-id/usb-Klipper_rp2350_XXXX-if00      (unchanged)",
    )
    for arrow_y in (442, 774):
        art.arrow(axes, (card_x + card_width / 2, arrow_y + 2), (card_x + card_width / 2, arrow_y + 38), width=4.0, head=22)
    art.label(axes, card_x + 26, 1150, "Stop Klipper first:  sudo systemctl stop klipper      and start it afterwards:  sudo systemctl start klipper", size=16, colour=NOTE)

    art.save_sheet(figure, IMAGES / "TinyFan2350_Flashing.png")


# ---------------------------------------------------------------------------------------------
# menuconfig screens
# ---------------------------------------------------------------------------------------------
def make_menuconfig(file_name, window_title, rows, marked_row, note):
    """Drawing of a `make menuconfig` screen; marked_row gets a red frame and the note."""
    width, row_height, top = 1500, 36, 84
    height = top + row_height * len(rows) + 150
    figure, axes = art.new_sheet(width, height)
    grey, yellow = "#c4c4c4", "#c9c530"
    art.rect(axes, 0, 0, width, height, grey, line=0, z=1)
    art.code_text(axes, 8, 17, "(Top)", size=22, colour=INK)
    art.rect(axes, 0, 34, width, 36, yellow, line=0, z=2)
    art.code_text(axes, width / 2, 52, window_title, size=22, colour="#555555", ha="center")
    for index, content in enumerate(rows):
        centre_y = top + row_height * (index + 0.5)
        if index == 0:
            art.rect(axes, 4, centre_y - 16, 13.3 * len(content) + 10, 32, "#1433c9", line=0, z=2)
            axes.text(
                10, centre_y, content, family="DejaVu Sans Mono", weight="bold",
                fontsize=art.px_to_pt(22), va="center", color="#ffffff", zorder=9,
            )
        else:
            art.code_text(axes, 10, centre_y, content, size=22, colour=INK)
        if index == marked_row:
            text_width = 13.3 * len(content.rstrip())
            art.rect(axes, 56, centre_y - 17, text_width - 44, 34, "none", radius=7, line=3.0, edge=RED, z=10)
            art.arrow(axes, (text_width + 150, centre_y), (text_width + 26, centre_y), width=3.0, colour=RED, head=20)
            art.label(axes, text_width + 162, centre_y, note, size=19, colour=RED)
    bottom = top + row_height * len(rows) + 30
    art.rect(axes, 0, bottom, width, 34, yellow, line=0, z=2)
    art.code_text(axes, 8, bottom + 58, "[Space/Enter] Toggle/enter      [?] Help            [/] Search", size=22, colour="#555555")
    art.code_text(axes, 8, bottom + 92, "[Q] Quit (prompts for save)     [ESC] Leave menu", size=22, colour="#555555")
    art.save_sheet(figure, IMAGES / file_name)


def make_menuconfigs():
    make_menuconfig(
        "Menuconfig_Katapult.png", "Katapult Configuration",
        [
            "    Micro-controller Architecture (Raspberry Pi RP2040/RP235x)  --->",
            "    Processor model (rp2350)  --->",
            "    Build Katapult deployment application (Do not build)  --->",
            "    Communication Interface (USBSERIAL)  --->",
            "    USB ids  --->",
            "    Build Optimization Override (Size (-Os))  --->",
            "()  GPIO pins to set on bootloader entry",
            "[*] Support bootloader entry on rapid double click of reset button",
            "[ ] Enable bootloader entry on button (or gpio) state",
            "[ ] Enable Status LED",
        ],
        1, "rp2350",
    )
    klipper_rows = [
        "[*] Enable extra low-level configuration options",
        "    Micro-controller Architecture (Raspberry Pi RP2040/RP235x)  --->",
        "    Processor model (rp2350)  --->",
        "    Bootloader offset (%s)  --->",
        "    Communication Interface (USBSERIAL)  --->",
        "    USB ids  --->",
        "[*] Optimize stepper code for 'step on both edges'",
        "()  GPIO pins to set at micro-controller startup",
    ]
    make_menuconfig(
        "Menuconfig_Klipper_Katapult.png", "Klipper Firmware Configuration",
        [row % "16KiB bootloader" if "%s" in row else row for row in klipper_rows],
        3, "needed for Katapult",
    )
    make_menuconfig(
        "Menuconfig_Klipper.png", "Klipper Firmware Configuration",
        [row % "No bootloader" if "%s" in row else row for row in klipper_rows],
        3, "without Katapult",
    )


if __name__ == "__main__":
    make_pinout()
    make_jumpers()
    make_wiring()
    make_flashing()
    make_menuconfigs()
