# Assembly guide

**Easiest: have JLCPCB or PCBWay build it** ([ordering.md](ordering.md)). Then the only soldering left is the RP2350-Zero socket strips (step 2.2 below), plus the fuse holders if you left them off the order.

If you build it by hand: SMD parts are 0805, 1206, SOT-23, SOD-123, 0603x4 resistor arrays and **SOT-363 (0.65 mm pitch)**. Almost all of them are on the bottom side. The 8 status/power LEDs and their resistors (LD1-LD8, R33-R40) are on the **top** so you can see them. The SOT-363 parts need a fine tip, flux and a magnifier. Connectors and through-hole parts go on the top side.

![Bottom side](images/render-bottom.png)

## Tools

- Temperature-controlled iron with a fine chisel tip, flux, 0.5-0.8 mm solder
- Tweezers, desoldering wick
- Multimeter (continuity and voltage)

## Order of work

Solder from the lowest parts to the tallest.

### 1. Bottom side SMD

| Refs | Part | Notes |
|---|---|---|
| U2 | 74HCT2G17GW (SOT-363 / TSSOP-6) | Pin 1 dot on the silk. Must be **HCT**, not HC |
| Q1-Q3 | BSS138DW (SOT-363) | Pin 1 dot on the silk |
| D1-D6 | BAT54S (SOT-23) | Under the RP2350-Zero. Not interchangeable with BAT54/BAT54C/BAT54A |
| RN1-RN6 | 10k x4 array, EXB-38V103JV | Not polarised |
| R19, R20 | 330R | LED data series resistors |
| R21-R26 | 4.7k | Tach series resistors, under the RP2350-Zero |
| R27-R30 | 4.7k 1% | Thermistor pull-ups (bottom edge, under TH1-TH4) |
| R31, R32 | 10k | LED input pull-downs |
| C1, C2 | 10uF 50V 1206 | C1 next to F1, C2 next to F2 |
| C3, C7-C10 | 100nF 0805 | |
| Q4-Q9 | AO3400A (SOT-23) | Fan-mode MOSFETs, right of each fan connector |
| D7-D12 | B5819W (SOD-123) | Flyback diodes. **Band (cathode) towards the jumpers** as on the silk |

Top side SMD:

| Refs | Part | Notes |
|---|---|---|
| LD1-LD8 | Green LED 0805 | Cathode mark to pad 1 (square/marked pad) |
| R33-R39 | 10k 0805 | LED resistors |
| R40 | 1k 0805 | 5V ON LED resistor |

The reference designators are hidden on the bottom silk to save space. Use the interactive BOM or the `hardware/fab/TinyFan2350-pos.csv` coordinates, or open the PCB in KiCad and hover over a footprint.

Check after this step: no solder bridges on the SOT-363 parts. Check with the meter that +5V, +3V3 and VIN are not shorted to GND. Measure at the fuse holders and the EXP header.

### 2. Top side, low parts

1. JP1-JP6, JM1-JM6, JL1-JL2 (1x3 headers) and J5 (1x4 header)
2. RP2350-Zero sockets: 2 x 1x9 + 1 x 1x5 female headers. Put the module into the sockets while you solder them, so they stay straight.
3. JST-XH headers: FAN1-FAN6 (4-pin), J3/J4 (3-pin), J6-J9 / TH1-TH4 (2-pin). The locking ramp faces the same way as the silk outline.

### 3. Top side, tall parts

1. F1, F2 mini-blade fuse holders (Keystone 3568)
2. C5 (100uF 50V) and C6 (470uF 16V). **Polarity**: the long lead (+) goes to the pad next to the `+` on the silk, and the stripe faces away from it.
3. J1, J2 screw terminals. The wire openings face the left board edge.

### 4. RP2350-Zero

Solder male pin headers to the module: both 9-pin sides and the 5-pin row on the end (GP9-GP13). Plug it in with the **USB-C connector facing the top edge** of the board, as the outline on the silk shows.

## Before first power-up

1. Leave the fuses out. Using the meter in continuity mode, check:
   - J1 VIN+ screw to J1 GND screw: not shorted
   - J2 5V+ screw to J2 GND screw: not shorted
2. Fit the fuses: **5A in F1** (VIN) and **5A in F2** (5V).
3. With no fans plugged in, apply 5V to J2 and VIN to J1. You should measure:
   - the JP middle pin with the jumper on top = VIN
   - the JP middle pin with the jumper on the bottom = 5V
   - J3/J4 pin 2 = 5V
4. Plug the RP2350-Zero into the host by USB, then flash Klipper ([klipper.md](klipper.md)).
5. Set every fan jumper ([wiring.md](wiring.md)), then plug the fans in.

![Side view](images/render-front.png)
