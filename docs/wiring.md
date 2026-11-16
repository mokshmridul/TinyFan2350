# Wiring guide

![Pinout](images/pinout.png)

## Power

| Terminal | Feed | Fuse | Supplies |
|---|---|---|---|
| **J1: VIN 12-24V** | 12V or 24V from your PSU | F1, 5A mini blade | Fans (and LED strips) whose jumper is on **VIN**. Must match your fans: 12V fans need 12V here |
| **J2: 5V** | 5V from a buck converter or 5V PSU | F2, 5A mini blade | 5V fans, LED ports, level shifters |
| USB-C on the RP2350-Zero | Klipper host (Pi etc.) | - | The RP2350-Zero itself (MCU + 3.3V) |

Each screw has its label printed right in front of it: **GND**, **VIN+** (J1) and **5V+** (J2). On both terminals the top screw is GND.

- There is no voltage conversion on the board. J1 is passed straight to the fan jumpers.
- J1 and J2 share GND with each other and with the USB ground. Tie the supply grounds together at one point (your PSU's V-) and don't run separate ground returns.
- Use at least 0.5 mm² (20 AWG) wire for both inputs.
- Reverse polarity (or 12/24V into the 5V terminal) is caught by the TVS diodes D21/D22, which short the input and blow that input's fuse. Replace the fuse after fixing the wiring.

### Current budget

| Rail | Fuse | Comfortable continuous load |
|---|---|---|
| VIN | 5A | up to ~4A continuous, e.g. 3 fans at 0.8A + 3 fans at 0.2A = 3A, at 12V or 24V. More than 5A on VIN needs 2 oz copper and a 7.5A fuse |
| 5V | 5A | ~3.5A total for 5V fans + LEDs (a 60-LED WS2812 strip at full white is ~3.6A, so cap brightness in software) |

Each fan port is good for about **1A**. The board warms by roughly 15 °C if a rail runs at the full 5A for a long time, which is fine. Order 2 oz copper if you want it to run cooler (see [ordering.md](ordering.md)).

## Fans (FAN1-FAN6)

JST-XH 4-pin, 2.5 mm pitch. Standard PC fan plugs (2.54 mm KK-style) **do not fit**. Re-terminate the fans with XHP-4 housings.

| XH pin | Signal | Typical PC fan wire |
|---|---|---|
| 1 | GND | black |
| 2 | +V (VIN or 5V, from the jumper) | yellow (12V fans) / red |
| 3 | TACH | green |
| 4 | PWM | blue |

Wire colours vary by maker, so always check the fan's datasheet.

### Two jumpers per fan port

Each port has two 3-pin jumpers next to it. **Set both before you power up.**

| Jumper | Top two pins | Bottom two pins |
|---|---|---|
| **MODE** (JM, left column) | 2-pin or 3-pin fan | 4-pin PWM fan |
| **FAN V** (JP, right column) | VIN (what J1 is fed, 12V or 24V) | 5V |

- **4-pin fan:** MODE on the bottom. The fan gets steady power and is controlled through its blue PWM wire.
- **2-pin fan** (most Voron 4010/5015/6015 fans): MODE on top. Crimp the fan into an XHP-4 housing using **pin 1 (black, -) and pin 2 (red, +)** only. The board switches the fan's ground. In Klipper set `cycle_time: 0.010` for that fan (see `klipper/tinyfan.cfg`).
- **3-pin fan:** MODE on top, pins 1-3 as in the table. Speed control works, but the tach reading is not reliable in this mode, so leave `tachometer_pin` out.
- If you get MODE wrong nothing is damaged: a 2-pin fan with MODE on the bottom just runs at full speed, and a 4-pin fan with MODE on top runs badly until you move the jumper.
- The small green LED next to each fan lights when that port is powered. With a 2/3-pin fan it gets brighter as the fan speeds up.
- **Shorted cable?** Each fan port has its own resettable fuse (1.6A) and each LED port a 2A one. If a bad crimp shorts +V to GND, only that port switches off (its fan stops). Unplug, fix the cable, wait about a minute and it works again. No fuse to replace. Fans up to about 1A each are fine (your 0.8A fans included). With six big fans on VIN, use a 7.5A fuse in F1.

## LED strips (LED1, LED2)

JST-XH 3-pin: 1 GND, 2 +V, 3 DATA. The **LED V** jumpers (JL1 for LED1, JL2 for LED2, bottom right corner) pick the strip's power:

| JL position | Strip power | For |
|---|---|---|
| Left two pins (VIN) | Whatever J1 is fed (12V or 24V) | WS2815, 12V/24V addressable strips |
| Right two pins (5V) | 5V from J2 | WS2812B, SK6812 and other 5V strips |

**A 5V strip on VIN will be destroyed. Check the jumper first.** The data line is 5V in both cases. Each port is good for about 2A.

### Voltage jumpers (JP1-JP6)

Each fan port has a 3-pin header to its right, labelled **VIN** (top) and **5V** (bottom).

- Jumper on the **top two pins**: the fan gets **VIN** (12V or 24V, whatever J1 is fed).
- Jumper on the **bottom two pins**: the fan gets **5V**.
- No jumper: the fan gets no power.

> **Match the jumper to the fan's rated voltage.** A 12V fan on a 24V VIN will overheat and fail. A 5V fan on VIN will be destroyed immediately.

### 2-pin and 3-pin fans

- **2-pin and 3-pin fans**: set that port's MODE jumper to the top two pins (see above) and Klipper controls their speed.

The LED data line is buffered to 5V with a 1k series resistor and a clamp diode, so a long run to the first LED is fine, and touching +V to the data pin by mistake doesn't kill the buffer.

## Thermistors (TH1-TH4)

JST-XH 2-pin: **pin 1 = signal, pin 2 = GND**. Thermistors have no polarity. Use 100k NTC thermistors (Generic 3950 by default). The 4.7k pull-up is on the board, so you don't need to add anything.

| Port | GPIO |
|---|---|
| TH1 | GP26 |
| TH2 | GP27 |
| TH3 | GP28 |
| TH4 | GP29 |

## EXP header (J5)

1 GND, 2 3V3, 3 GP15, 4 GP14. **3.3V logic only.** You can use it for a door switch, a filament sensor, a single extra neopixel data line (unbuffered), I2C (GP14 = SDA1, GP15 = SCL1), etc. Do not draw more than ~100 mA from 3V3.

## Mounting

4 x M3 holes on a **75 x 67 mm** rectangle (4.5 mm in from the top, bottom and right edges, 9.5 mm from the left edge). The holes are connected to GND. Allow about 20 mm of height above the board for the fuse holders with fuses fitted. For DIN rail mounting, see [mounting.md](mounting.md).
