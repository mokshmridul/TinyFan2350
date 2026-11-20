# Design notes

This page explains how the board works and why the parts were chosen. You don't need it to build or use the board. Each section starts with a short plain-language summary, and the details follow for anyone who wants them.

Schematic: [TinyFan2350-schematic.pdf](TinyFan2350-schematic.pdf). KiCad project: [`hardware/kicad`](../hardware/kicad) (KiCad 10).

## Safety margins

**In short:** every important part runs well below its maximum rating, even with a 24 V supply turned up to its 28.8 V limit and the board in a warm electronics bay. Datasheet maximums are not targets: real parts get hot, power supplies spike, and cheap parts vary. So the design follows the usual engineering rule of thumb and keeps voltage at or below about 80 % of each part's rating, current at or below about 75 %, and copper heating at or below about 20 °C at the recommended maximum load (the two main rails go slightly over that only right at the fuse limit; see [Copper](#copper-1-oz)).

Voltages are given at **24 V** and at **28.8 V**, which is the highest setting of a typical adjustable 24 V supply such as the Mean Well LRS-350-24. Currents are for the intended load: up to 3 fans at 0.8 A plus 3 fans at 0.2 A.

### Voltage

| Part | What it is | Rating | Load at 24 V | Load at 28.8 V |
|---|---|---|---|---|
| Q4-Q9 **SI2308A** | Switch for 2/3-pin fans | 60 V | 40 % | 48 % |
| D7-D12 B5819W | Flyback diode across each fan | 40 V | 60 % | 72 % |
| F3-F10 PTC fuses | Self-resetting port fuses (they only see full voltage after they trip) | 33 V | 73 % | 87 % |
| D21 **SMCJ30A** | Input protection diode | 30 V stand-off | 80 % | 96 % (still below the point where it starts to conduct) |
| Q1 **AO4485** | VIN reverse-polarity switch | 40 V | 60 % | 72 % |
| Q1 gate | Held at 5.6 V by zener D23 | 20 V | 28 % | 28 % |
| Q2 **AO4407A** | 5 V reverse-polarity switch | 30 V | 17 % | - |
| C1 / C5 | VIN capacitors (ceramic / electrolytic) | 50 V | 48 % | 58 % |
| F1/F2 **Nano2 fuses** (Littelfuse 0452005.MRL) | Main fuses, soldered | 125 V | 19 % | 23 % |
| C6 / C2 | 5 V capacitors | 16 V / 50 V | 31 % / 10 % | - |
| 2N7002, 74HCT2G17, BAT54S | Signal parts on 3.3/5 V | 60 V / 7 V / 30 V | 8 % / 71 % / 17 % | - |

How the protection fits together: D21 starts to conduct between 33.3 V and 36.8 V. That is above any normal 24 V supply, but below the 40 V of the flyback diodes, the 40 V of Q1 and the 60 V of the fan MOSFETs. If something higher arrives (a wrong supply, a big spike), D21 shorts it and F1 blows before any other part reaches its limit. Power wired **backwards** never gets that far: Q1 / Q2 simply stay off (see [Power](#power)).

### Current and heat

| Part | Rating | Normal load | Margin |
|---|---|---|---|
| SI2308A switch, per fan | 3 A, 1.25 W | 0.8 A, about 0.06 W of heat | 27 % of current, 5 % of power |
| Fan port PTC (F3-F8) | 1.5 A hold (about 1.1 A at 60 °C) | 0.8 A | 53 % cold, about 73 % in a 60 °C bay |
| LED port PTC (F9/F10) | 2 A hold (about 1.5 A at 60 °C) | recommended max 1.5 A | 75 % |
| F1 VIN fuse (slow-blow) | 5 A | 3 A | 60 % |
| F2 5 V fuse (slow-blow) | 5 A | recommended max 3.5 A | 70 % |
| Q1 AO4485 (VIN switch) | 10 A | 3 A, about 0.2 W of heat | 30 % |
| Q2 AO4407A (5 V switch) | 12 A | 3.5 A, about 0.2 W of heat | 29 % |
| R65/R66 22k gate resistors | 0.125 W | 0.015 W at 24 V | 12 % (20 % at 28.8 V) |
| JST-XH connectors | 3 A per pin | 0.8 A fan, 1.5 A LED | 27 % / 50 % |
| 0805 resistors on VIN (R33-R39) | 0.125 W | 0.05 W at 24 V | 38 % (66 % at 28.8 V) |

### Copper (1 oz)

A resistive model of the real board layout (every track, pad, via and copper pour, both layers) finds the most crowded spot on each power path and turns it into a temperature rise with the IPC-2221 method:

| Path | Normal load | Rise | At the fuse limit | Rise |
|---|---|---|---|---|
| Fan power and return, per port | 0.8 A | 2-3 °C | 1.5 A | 6.5-9 °C (FAN4 power: 11.5 °C) |
| LED strip power, per port | 1.5 A | 2.5-5.5 °C | 2 A | 4.3 and 9.6 °C |
| J1 → F1 → Q1 (VIN input side) | 3 A | 2-3 °C | 5 A | 5.0-7.4 °C |
| VIN after Q1 (to the jumpers) | 3 A | about 3 °C | 5 A | 7.8 °C |
| J2 → F2 → Q2 (5 V input side) | 3 A | 1.5-2.5 °C | 5 A | 4.5-6.9 °C |
| +5 V after Q2 (to the jumpers) | 3 A | about 3.5 °C | 5 A | 9.2 °C |
| GND return (shared) | 3 A | about 2 °C | 5 A | 6.2 °C |

v2.7 is 3 mm wider and 6 mm taller than v2.6 (89 x 58.1 mm). The power section was rebuilt around that space: the VIN bus and the +5 V rail now run as wide copper areas on the bottom layer, so the top layer is free for an unbroken ground return. Every power path now stays **under 10 °C even at the 5 A fuse limit** (v2.6: about 25 °C). The one exception is a single short neck on the FAN4 power feed, next to its flyback diode, which reaches 11.5 °C at the full 1.5 A. That is still far below what the copper and the black solder mask can take (above 100 °C). The recommended maximums (4 A on VIN, 3.5 A on 5 V) now come only from fuse derating, not from copper heating.

**Need more current, or want extra margin?** Order the board with **2 oz copper** (one option on the order page). It roughly halves every number in the table. With 2 oz copper you may fit a **7 A** Nano2 fuse (Littelfuse 0452007.MRL) in F1 and run up to about 6 A on VIN.

### Known limits

- **+V shorted to a 12/24 V strip's DATA pin**: the 1k protection resistor (R19/R20) takes about 0.36 W at 24 V, more than its 0.25 W rating. It is fine for a moment, but fix the short quickly. With 5 V strips there is no problem.
- **24 V shorted to a fan's tach (RPM) pin**: the 4.7k resistor takes about 0.09 W (71 % of its rating). It survives.
- **+V shorted straight onto a fan's PWM pin** is not protected. Pins 2 and 4 are not next to each other, so a bad crimp can't easily cause it.

## Schematic layout

**In short:** the schematic is split into pages by job. The fan page is drawn once and used six times.

| Sheet | File | What is on it |
|---|---|---|
| Root | `TinyFan2350.kicad_sch` | Overview: which RP2350 pin goes to which port |
| Power | `power.kicad_sch` | J1/J2, F1/F2 fuses, Q1/Q2 reverse-polarity switches, capacitors, protection diodes, power lights, mounting holes |
| MCU | `mcu.kicad_sch` | RP2350-Zero pin map, EXP header J5 |
| FAN1..FAN6 | `fan_channel.kicad_sch` (one file, used 6 times) | Speed-signal booster, RPM input and its protection, fan socket, VIN/5V jumper, flyback diode, status light, 2/3-pin switch, port fuse |
| LEDs | `leds.kicad_sch` | 74HCT2G17 data booster, data protection, two LED ports with their jumpers and fuses |
| Thermistors | `thermistors.kicad_sch` | Four thermistor inputs (4.7k resistor + 100 nF filter each) |

`VIN`, `+5V`, `+3V3` and `GND` are global power symbols. The root sheet only carries signals between the RP2350 and the ports. Inside a fan page the signals are named per port, for example `/FAN3/FAN_GND`. Each part keeps its board reference (R, Q, D, F number); the fan page has a table that maps FAN1..FAN6 to their numbers. Every fitted part carries its maker, maker part number and LCSC number.

## Power

**In short:** two separate inputs. Each has a fuse, a reverse-polarity switch and a protection diode. The RP2350-Zero is powered by its own USB cable.

```mermaid
flowchart LR
  J1["J1 VIN 12-24V"] --> F1["F1 5A"] --> Q1["Q1 AO4485<br/>reverse-polarity switch"] --> VIN(("VIN<br/>C1 10uF 50V<br/>C5 100uF 50V<br/>D21 SMCJ30A"))
  J2["J2 5V"] --> F2["F2 5A"] --> Q2["Q2 AO4407A<br/>reverse-polarity switch"] --> V5(("+5V<br/>C2 10uF<br/>C6 470uF<br/>D22 SMBJ5.0A"))
  VIN --> JP["JP1-JP6 left"]
  V5 --> JPb["JP1-JP6 right"]
  JP --> FANS["FAN1-6 +V"]
  JPb --> FANS
  VIN --> JL["JL1/JL2 VIN side"] --> LED["LED1/LED2 +V"]
  V5 --> JL5["JL1/JL2 5V side"] --> LED
  V5 --> SHIFT["PWM pull-ups, 74HCT2G17 buffer"]
  USB["USB-C (host)"] --> MCU["RP2350-Zero"] --> V33(("+3V3: tach/thermistor pull-ups"))
```

- The RP2350-Zero's 5 V pin is not connected, so the USB 5 V and the J2 5 V can never feed into each other.
- VIN is not regulated on the board. Anything from 12 V to 24 V works (see the voltage table above).
- **Main fuses F1/F2:** Littelfuse Nano2 0452005.MRL, 5 A slow-blow, a small soldered SMD fuse (2410 size, about 6 x 2.7 mm). Slow-blow means the inrush when fans spin up won't blow it. It replaces the blade-fuse holders of v2.5 and saves a lot of board space. The trade-off: if one ever blows you have to solder in a new one. With the reverse-polarity switches below, it should only blow on a real fault (a short or the wrong supply).
- **Power wired backwards:** Q1 (VIN) and Q2 (5 V) are P-channel MOSFETs in the "ideal diode" arrangement. With correct polarity, the MOSFET's gate is pulled to GND by a 22k resistor (R65/R66), so it turns fully on and drops only about 0.05 V at 3 A. Wired backwards, the gate sees the wrong polarity and the MOSFET stays off: nothing flows, nothing blows, the board just does not turn on (the ON light stays dark). Fix the wiring and it works. A 5.6 V zener (D23/D24) keeps Q1's gate inside its 20 V limit on 24 V.
- **Too high a voltage** (for example 12 V or 24 V into the 5 V input): D21 (VIN) and D22 (5 V) sit right after the switches. They break down and short the rail, the fuse blows, and the rest of the board never sees it. They also absorb short spikes from the power supply.
- **Grounds:** J1 GND, J2 GND and the USB ground are joined on this board, as on every earlier version (the fans and LED strips need it). The board does not need any other ground link: in a printer where the Pi, 5 V and 24 V supplies already share a ground elsewhere, that is fine.
- Both copper layers have a solid GND pour, tied together by stitching vias. Small SMD ground pads connect solidly. Through-hole ground pins connect with four spokes, so a normal soldering iron can heat them.

## Fan speed signal (x6)

**In short:** the RP2350 speaks 3.3 V, and 4-pin fans expect 5 V, so a small MOSFET on each port converts it. If the RP2350 is unplugged, the fans run at full speed, which is the safe way to fail.

Each fan has its own 2N7002 (Q10-Q15 = FAN1-FAN6). The gate is tied to 3V3 and the source is on the GPIO, the classic two-way level shifter. The GPIO side is pulled up to 3V3 with 10k and the fan side to 5V with 10k (R47-R64). The logic is non-inverting. Fans have their own pull-up on PWM, so the result is an open-drain 5 V signal, as the Intel 4-wire fan spec expects.

## Fan mode: 4-pin or 2/3-pin (x6)

**In short:** a jumper picks how the fan is controlled. 4-pin fans get steady power and a speed signal. 2/3-pin fans have no speed wire, so the board switches their ground on and off instead.

Pin 1 of the fan socket (GND) goes to the MODE jumper JMx and to the drain of an SI2308A MOSFET (Q4-Q9). The MOSFET's source is on the port's return (FANx_RET), which reaches GND through the port's PTC fuse.

- **JM on the right two pins (`4P`, 4-pin):** the jumper ties pin 1 straight to the return. The MOSFET is bypassed, and the fan is controlled by its PWM wire as above.
- **JM on the left two pins (`2/3`, 2/3-pin):** pin 1 only reaches the return through the MOSFET. Its gate is driven by the same 5 V PWM line, through a 22k resistor and clamped by a 5.6 V zener, so the PWM switches the fan's ground (like the Voron Klipper Expander). A B5819W Schottky across the fan catches the spike when it switches off. If the RP2350 is unplugged, the pull-up holds the gate on, so the fan runs at full speed, the same safe failure as 4-pin mode.
- The 10k pull-up and 22k gate resistor make the switch turn on in tens of microseconds. That is fine at 100 Hz but too slow for 25 kHz, so 2/3-pin ports use `cycle_time: 0.010` (see `klipper/tinyfan.cfg`).
- **Why the SI2308A:** it is rated for 60 V, so on 24 V it runs at 40 % of its voltage rating (the AO3400A used before v2.5 was rated 30 V, which is 80 % at 24 V and 96 % at 28.8 V). It has 95 mΩ at 4.5 V gate drive, so a 0.8 A fan heats it by only about 0.06 W. Same SOT-23 size and pin order (1 G, 2 S, 3 D).
- The status light (10k from the fan's +V to pin 1) is on whenever the port has power. In 2/3-pin mode it follows the fan speed. It is dim on 5 V fans and bright on 24 V fans.

## Port protection

**In short:** a badly crimped cable should kill a fan at worst, never the board.

- **Fan ports:** each port's return goes to GND through a **1.5 A / 33 V** PTC (F3-F8, LUTE 1812L150/33GR). It carries a 0.8 A fan continuously even in a warm bay, and trips a dead short (tens of amps) in well under a second, so only that port switches off. It resets once the short is gone and it cools.
- **Fan MOSFET gates:** R41-R46 (22k) plus BZT52C5V6 zeners (D13-D18). A fan wired with its power reversed can push the PWM line well above 5 V; the zener keeps the gate under its 20 V limit.
- **RPM (tach) lines:** 4.7k in series plus a BAT54S clamp to 3V3, so even 24 V on a tach pin only lets about 4 mA through.
- **LED ports:** a **2 A / 33 V** PTC (F9/F10, LUTE 1812L200/33GR) in each strip's return, plus the data protection below.
- **Inputs:** see [Power](#power).

## LED strip power (x2)

JL1/JL2 connect each LED socket's pin 2 to VIN (left two pins) or 5 V (right two pins). Data is always the 5 V buffer output. 12 V/24 V addressable strips (WS2815, WS2813 12 V) also accept it, because their chips run their logic from an internal ~5 V supply. The strip power tracks are 0.8 mm or wider (see the copper table).

## Fan RPM (tach) input (x6)

```
FAN TACH (XH pin 3) --+-- 10k (R51/R52, R57/R58, R63/R64) --> 3V3
                      |
                      +-- 4.7k --+--> GPIO
                                 |
                          BAT54S clamp to GND and 3V3
```

The fan's tach output is open collector, pulled up to 3V3 on the board. The 4.7k resistor and the clamp diodes limit the current into the RP2350 to a few mA if a miswired fan puts VIN on the tach wire.

The RP2350 has a known chip bug (erratum E9): a GPIO input can latch at about 2 V when the signal is weak. The 10k pull-up drives the line hard enough that this doesn't happen here.

## LED data (x2)

**In short:** the RP2350's 3.3 V data is boosted to 5 V so long strips read it reliably, and the line is protected against mistakes.

One 74HCT2G17 dual buffer, powered from 5 V, drives both ports. HCT inputs switch below 2 V, so they read 3.3 V reliably, and the outputs swing the full 5 V. Each input has a 10k pull-down (R31/R32), so the strips stay dark while the RP2350 is unplugged or starting. A 1k resistor (R19/R20) damps ringing on long cables, and a BAT54S (D19/D20) clamps the buffer side to 0-5 V. If +V touches the data pin, the current is limited to about 19 mA even at 24 V (see [Known limits](#known-limits)).

## Thermistors (x4)

4.7k 1 % pull-up to 3V3 and 100 nF to GND at the ADC pin, with the 100k NTC thermistor to GND through the connector. The ADC pins are GP26-GP29. Klipper sets them as analog inputs with the digital input off, so erratum E9 does not affect them.

## Track corners and EMI

Right-angle track corners are often said to cause interference (EMI). That only matters at multi-GHz signal speeds. The fastest signal here is the 800 kHz LED data (the fan PWM is 25 kHz). What matters on this board is a clean ground return, so it has solid ground pours under the signal tracks and stitching vias between the top and bottom grounds. Right-angle corners were still cut to 45° wherever there was room.

## Changes from the original TinyFan

| | TinyFan (Gi7mo) | TinyFan2350 v2.7 |
|---|---|---|
| MCU | RP2040-Zero | RP2350-Zero (same footprint and pinout), socketed |
| Input | 24 V + on-board converter | Separate 12-24 V and 5 V inputs, each with a fuse, a reverse-polarity switch and a protection diode |
| Fans | 2/3/4-pin, fixed voltage | 6 x JST-XH, VIN/5V jumper per port, 4-pin PWM or switched 2/3-pin, RPM input with protection, self-resetting fuse per port |
| LEDs | - | 2 x addressable LED ports, 5 V data, 5 V or VIN strip power |
| Sensors | - | 4 x thermistor ports |
| Size | ~60 x 62 mm | 89 x 58.1 mm |

## Verification

- ERC (electrical check): 0 errors.
- DRC (layout check, KiCad 10.0.8): 0 violations, 0 unconnected.
- Every pad's net checked against the design table by script.
- A separate script rebuilt the copper from the board file and checked it for shorts between nets and for gaps below 0.15 mm: none found.
- Clearances: 0.18 mm on signals (0.15 mm where tracks enter fine-pitch pads), 0.2 mm on GND and fan power, 0.25-0.3 mm on VIN/5V. Copper stays at least 0.5 mm from the board edge. All of it is well inside JLCPCB's and PCBWay's standard 2-layer limits.
