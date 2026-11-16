# Changelog

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
