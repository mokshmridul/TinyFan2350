# Wiring guide

![Pinout](images/pinout.png)

## Power

| Terminal | Feed | Fuse | Supplies |
|---|---|---|---|
| **J1: VIN 12-24V** | 12V or 24V from your PSU | F1, 5A mini blade | Fans whose jumper is on **VIN** |
| **J2: 5V** | 5V from a buck converter or 5V PSU | F2, 4A mini blade | 5V fans, LED ports, level shifters |
| USB-C on the RP2350-Zero | Klipper host (Pi etc.) | - | The RP2350-Zero itself (MCU + 3.3V) |

On **both** terminals the **top screw is GND** and the bottom screw is +.

- There is no voltage conversion on the board. J1 is passed straight to the fan jumpers.
- J1 and J2 share GND with each other and with the USB ground. Tie the supply grounds together at one point (your PSU's V-) and don't run separate ground returns.
- Use at least 0.5 mm² (20 AWG) wire for both inputs.
- There is no reverse-polarity protection. A reversed input will most likely kill the MOSFETs and buffers before the fuse blows.

### Current budget

| Rail | Fuse | Comfortable continuous load |
|---|---|---|
| VIN | 5A | ~3.5A total, e.g. 3 fans at 0.6A + 3 fans at 0.3A = 2.7A |
| 5V | 4A | ~3A total for 5V fans + LEDs (a 60-LED WS2812 strip at full white is ~3.6A, so cap brightness in software) |

## Fans (FAN1-FAN6)

JST-XH 4-pin, 2.5 mm pitch. Standard PC fan plugs (2.54 mm KK-style) **do not fit**. Re-terminate the fans with XHP-4 housings.

| XH pin | Signal | Typical PC fan wire |
|---|---|---|
| 1 | GND | black |
| 2 | +V (VIN or 5V, from the jumper) | yellow (12V fans) / red |
| 3 | TACH | green |
| 4 | PWM | blue |

Wire colours vary by maker, so always check the fan's datasheet.

### Voltage jumpers (JP1-JP6)

Each fan port has a 3-pin header to its right, labelled **VIN** (top) and **5V** (bottom).

- Jumper on the **top two pins**: the fan gets **VIN** (12V or 24V, whatever J1 is fed).
- Jumper on the **bottom two pins**: the fan gets **5V**.
- No jumper: the fan gets no power.

> **Match the jumper to the fan's rated voltage.** A 12V fan on a 24V VIN will overheat and fail. A 5V fan on VIN will be destroyed immediately.

### 2-pin and 3-pin fans

- **3-pin fans** (GND, +V, TACH): they run at full speed whenever the port is powered and still report tach. PWM has no effect, because the board drives the PWM wire, not the fan's power.
- **2-pin fans**: connect to XH pins 1 and 2. They always run at full speed.

## LED ports (J3 = LED1, J4 = LED2)

JST-XH 3-pin: **1 GND, 2 +5V, 3 DATA**. For 5V WS2812B / SK6812 strips only (not 12V WS2811 strips). The data line is buffered to 5V with a 330R series resistor, so a long run to the first LED is fine.

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

4 x M3 holes on a **75 x 67 mm** rectangle, 4.5 mm in from each corner. The holes are connected to GND. Allow about 20 mm of height above the board for the fuse holders with fuses fitted.
