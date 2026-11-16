# Changelog

## v2.4 (2026-11)
- **Easier to build and cheaper at JLCPCB.** The six 10k resistor arrays (EXB-38V) are now 18 ordinary 0805 resistors (R47-R64), and the three BSS138DW duals are now six **2N7002** SOT-23 MOSFETs (Q10-Q15). Both are JLC basic parts, so the only extended part JLC still places is U2.
- The LED resistors R33-R40 moved to the bottom. The top side now has only the 8 status LEDs, so a JLC order can be **bottom-side assembly only** (hand-solder the 8 LEDs).
- **1 oz copper is fine again, with F1 = 5A.** Sized for up to 5A on VIN, e.g. 3 x 0.8A + 3 x 0.2A fans (3A) at 12V or 24V. Above 5A on VIN, use 2 oz copper and a 7.5A fuse.
- Through-hole GND pins now connect to the ground pours with thermal spokes (0.8 mm), so they are easy to hand-solder. SMD pads stay solidly connected.
- U2 is the 74HCT2G17GW-Q100H (C547569), same chip as the ,125 part which is often short at JLC.
- JLC CPL: J1-J4 rotated 180° to match JLC's 3D models.
- R41-R46 (MOSFET gate resistors) 4.7k -> **22k** (C17560, basic): the AO3400A's gate capacitance no longer slows the 25 kHz PWM edge in 4-pin mode.
- Independent review: ERC/DRC 0, all 355 pads match the design, pinouts checked against datasheets.

## v2.3 (2026-11)
- **Port protection against bad crimps.** Each fan port's return goes through a 1.6A resettable fuse (PTC, F3-F8, holds 0.8-1A fans) and each LED port's return through a 2A PTC (F9/F10): a short in a cable switches off only that port and it recovers once fixed.
- LED data: 330R -> 1k 1206 plus a BAT54S clamp (D19/D20), so +V touching the data pin no longer kills the 74HCT2G17.
- Fan MOSFETs: 4.7k gate resistor + BZT52C5V6 zener (R41-R46, D13-D18), so a miswired fan can't push its gate past its rating. The resistor also keeps the gate's capacitance off the 4-pin PWM line.
- TVS crowbars behind the main fuses: SMCJ28A on VIN (D21), SMBJ5.0A on 5V (D22). Reverse polarity, or 12/24V into the 5V terminal, now blows the main fuse instead of the board.
- **F1 (VIN) is now 7.5A and the board is 2 oz copper**, for six 0.8A fans on VIN plus LEDs (~6.8A worst case).
- **MODE jumper flipped:** bottom two pins = 4-pin fan, top two pins = 2/3-pin fan (it was the other way round in v2.2).
- Board 100 x 63 mm (+7 mm for the protection column), holes 86 x 54 mm, black solder mask. DIN tray updated (clips 50 mm apart, centred).

## v2.2 (2026-11)
- Inspired by the Voron Klipper Expander: **every fan port can now drive a 2-pin or 3-pin fan**. A MODE jumper (JM1-JM6) picks 4-pin PWM (fan ground solid) or 2/3-pin (an AO3400A MOSFET switches the fan ground, B5819W flyback diode). The MOSFET is driven from the 5V PWM line, so fans still run at full speed if the RP2350 is unplugged.
- Status LED on every fan port, plus VIN ON and 5V ON LEDs.
- LED ports: jumpers JL1/JL2 pick 5V or VIN for each strip, so 12/24V addressable strips (WS2815) work. Data stays 5V.
- Board 93 x 63 mm (+6 mm wide for the new jumpers). DIN tray updated.
- LEDs and their resistors are on the top side, so the JLCPCB order is now two-sided SMT.

## v2.1 (2026-11)
- **Smaller board: 87 x 63 mm** (was 89 x 76), M3 holes on a 73 x 54 mm pattern. The DIN tray in `mechanical/` is updated to match.
- Fan PWM level shifters: 6 x BSS138 -> **3 x BSS138DW** (dual MOSFET, SOT-363). Same circuit, half the parts.
- LED data buffers: 2 x 74AHCT1G125 -> **1 x 74HCT2G17** (dual Schottky-input buffer, SOT-363/TSSOP-6), with a 10k pull-down on each input so the strips stay dark while the RP2350 boots.
- 18 discrete 10k pull-ups -> **6 x EXB-38V103JV** 4-resistor arrays.
- **5A fuses on both rails** (F2 was 4A). Keystone 3568 mini-blade holders kept.
- Tach protection (4.7k + BAT54S) moved under the RP2350-Zero, next to the pins it protects.
- RP2350-Zero stays socketed in female headers.
- Assembly files for JLCPCB (BOM + CPL with LCSC part numbers) and PCBWay (BOM with maker part numbers). All SMD parts are on the bottom side, so it is a single-side SMT order.
- Narrower signal rules (0.2 mm / 0.18 mm) so the smaller board routes completely. Power trunks are still 2-3 mm.

## v2.0 (2026-11)
- Board enlarged to 89 x 76 mm with new M3 mounting holes (75 x 67 mm pattern). **Old TinyFan mounts no longer fit.**
- Fan supply input relabelled **VIN 12-24V**. No on-board conversion: fans on the VIN jumper position get whatever J1 is fed with.
- VIN-side capacitors uprated for 24V: C1 10uF **50V**, C5 100uF **50V**.
- New: 4 thermistor ports TH1-TH4 (JST-XH 2-pin) on GP26-GP29, each with a 4.7k 1% pull-up and 100nF filter.
- New: tach input protection on every fan (4.7k series resistor + BAT54S clamp to GND/3V3).
- EXP header reduced to 1x4 (GND, 3V3, GP15, GP14); GP26-29 moved to the thermistor ports.
- Power trunks widened to 2-3 mm, GND pour on both layers, wider clearances.
- Klipper config refactored (thermistors, flashing notes, examples).
- Left edge extended 5 mm so every input screw has its own GND / VIN+ / 5V+ label right in front of it.
- New printable DIN rail tray for two Voron Trident PCB DIN clips (`mechanical/`).

## v1.2
- Mini-blade fuses on both inputs (F1 5A, F2 4A), bulk capacitors, wider power traces.

## v1.1
- JST-XH fan and LED connectors, socketed RP2350-Zero, autorouted.

## v1.0
- First RP2350-Zero version: separate 12V and 5V inputs, 6 jumper-selectable 4-pin fans, 2 WS2812 ports.
