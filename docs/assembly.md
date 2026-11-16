# Assembly guide

**Easiest: have JLCPCB or PCBWay build it** ([ordering.md](ordering.md)). Then the only soldering left is the RP2350-Zero socket strips (step 2.2 below), plus the fuse holders if you left them off the order.

**Cheaper middle route:** order JLCPCB assembly for the **bottom side only**, with only the basic parts plus U2, and hand-solder the rest: the 8 top LEDs, the TVS diodes, PTC fuses, zeners, BAT54S clamps and all the through-hole parts. All of those are 0805 or bigger, SOT-23 or SOD-123.

If you build it all by hand: SMD parts are 0805, 1206, 1812, SOT-23, SOD-123, SMB/SMC and one **SOT-363 (0.65 mm pitch)**, U2, which needs a fine tip, flux and a magnifier. Everything except the 8 status/power LEDs (LD1-LD8, top side so you can see them) is on the bottom. Connectors and through-hole parts go on the top side; their GND pins have thermal spokes so a normal iron heats them fine.

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
| Q10-Q15 | 2N7002 (SOT-23) | PWM level shifters, between the fan connector pin rows |
| D1-D6 | BAT54S (SOT-23) | Under the RP2350-Zero. Not interchangeable with BAT54/BAT54C/BAT54A |
| R47-R64 | 10k 0805 | Pull-ups for the PWM shifters and tach lines, next to Q10-Q15 |
| R33-R39 | 10k 0805 | Fan / VIN LED resistors (bottom, under the LEDs' area) |
| R40 | 1k 0805 | 5V ON LED resistor |
| R19, R20 | 1k 1206 | LED data series resistors |
| R21-R26 | 4.7k | Tach series resistors, under the RP2350-Zero |
| R27-R30 | 4.7k 1% | Thermistor pull-ups (bottom edge, under TH1-TH4) |
| R31, R32 | 10k | LED input pull-downs |
| C1, C2 | 10uF 50V 1206 | C1 next to F1, C2 next to F2 |
| C3, C7-C10 | 100nF 0805 | |
| Q4-Q9 | AO3400A (SOT-23) | Fan-mode MOSFETs, right of each fan connector |
| D7-D12 | B5819W (SOD-123) | Flyback diodes. **Band (cathode) towards the jumpers** as on the silk |
| R41-R46 | 4.7k 0805 | MOSFET gate resistors (protection column, left of the MODE jumpers) |
| D13-D18 | BZT52C5V6 (SOD-123) | Gate zeners. Band (cathode) to pad 1, as on the silk |
| F3-F8 | PTC 1.6A 30V 1812 | Per-fan resettable fuses. Not polarised |
| F9, F10 | PTC 2A 30V 1812 | Per-LED-port resettable fuses, above the LED connectors. Not polarised |
| D19, D20 | BAT54S (SOT-23) | LED data clamps, below U2 |
| D21 | SMCJ28A (SMC) | VIN TVS next to F1. **Band (cathode) towards F1** |
| D22 | SMBJ5.0A (SMB) | 5V TVS next to F2. **Band (cathode) towards F2** |

Top side SMD:

| Refs | Part | Notes |
|---|---|---|
| LD1-LD8 | Green LED 0805 | Cathode mark to pad 1 (square/marked pad) |

The reference designators are hidden on the bottom silk to save space. Use the interactive BOM or the `hardware/fab/TinyFan2350-pos.csv` coordinates, or open the PCB in KiCad and hover over a footprint.

Check after this step: no solder bridges on U2 (SOT-363). Check with the meter that +5V, +3V3 and VIN are not shorted to GND. Measure at the fuse holders and the EXP header.

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
