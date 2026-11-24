# Klipper TinyFan2350

A small Klipper fan / LED / thermistor controller based on the **Waveshare RP2350-Zero**, derived from [Gi7mo/TinyFan](https://github.com/Gi7mo/TinyFan).

<p align="center">
  <img src="./Images/TinyFan2350_top.png" width="49%" alt="Top side">
  <img src="./Images/TinyFan2350_bottom.png" width="49%" alt="Bottom side">
</p>

|[• Build it](./Production)|[• Set it up](./Klipper)|[• Mount it](./Mount)|
|---|---|---|
|Order the PCB, parts list, soldering|Flashing, jumpers, wiring, Klipper config|Printable DIN rail mount, optional fan bridge|

## Features
- **5 fan ports** (JST-XH 4-pin) for 2-, 3- and 4-pin fans, 0.6A each
  - every fan has its own PWM output and tacho input -> independent speeds
  - per fan: mode jumper (**4P** = 4-pin PWM, **2/3** = switched GND) and voltage jumper (**VIN** or **5V**)
- **2 addressable LED ports** (JST-XH 3-pin), data level-shifted to 5V, VIN or 5V per port, 3A per connector
- **4 thermistor ports** (JST-XH 2-pin) on the RP2350 ADC
- **EXP header** with 4 free GPIOs (GP12-GP15)
- Inputs: **12/24V (VIN)** and **5V** for the fans and LEDs, each with a mini blade fuse (5A max, 3.75A continuous) and a
  reverse-polarity diode; no converters on board
- The RP2350-Zero is powered by its own **USB-C** cable, so the board cannot feed power back into the USB host
- All bottom-side SMD parts are **JLCPCB Basic** parts (cheap Economic assembly)
- 2 layers, 1 oz copper, black solder mask; SMD parts only on the bottom, THT only on the top; socketed MCU
- 100 x 65 mm, 4x M3 mounting holes (93 x 58 mm)
- Printable [DIN rail mount](./Mount) and an optional [fan bridge](./Mount#fan-bridge-optional) for a 40 mm cooling fan, run from one of the fan ports

## Files
|[Pinout](./Images/TinyFan2350_Pinout.png)|[Schematic](./Production/TinyFan2350_Schematic.pdf)|[Klipper config](./Klipper/TinyFan2350.cfg)|[KiCad project](./KiCad)|[Simulation](./Simulation)|[Pictures](./Images)|[Download](https://github.com/mokshmridul/TinyFan2350/releases/latest)|
|---|---|---|---|---|---|---|

## Notes
- Original TinyFan by [Gi7mo](https://github.com/Gi7mo/TinyFan), idea by [Rama](https://github.com/Ramalama2).
- Board revision **v1.3**: new tach inputs (series resistor, pass transistor and a capacitor at the pin instead of a
  diode), so the RP2350 sees a fan's low level properly and stays protected while a fan is switched; the unused D3
  pads are gone. See [Build it](./Production#v13-printed-on-the-board). It passes KiCad ERC/DRC and is
  simulated, but **it has not been built or tested yet**: read [Limits and safety](./Production#limits-and-safety) first.
- Release **v1.31**: the [schematic](./Production/TinyFan2350_Schematic.pdf) is redrawn on one page and is easier to
  read. The circuit and the board did not change, and the board still reads v1.3.

## License
GPL-3.0, the same as the original TinyFan. See [LICENSE](./LICENSE).

## Disclaimer
This project is provided on an "as-is" basis, without any warranty of any kind. I am not responsible for any damage, injury, loss or other issues caused by building or using it. If you choose to build or use this board, you do so entirely at your own risk.
