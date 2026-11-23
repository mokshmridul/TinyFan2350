# Klipper TinyFan2350


### Navigation:
|[• Installation & Klipper](./Klipper)|[• Get a PCB](./PCB)|[• DIN rail mount](./CAD)|[• Pictures](./Images)|
|---|---|---|---|

|[• Klipper Config](./Klipper/TinyFan2350.cfg)|[• Schematic](./PCB/TinyFan2350_Schematic.pdf)|[• Pinout](./Images/TinyFan2350_Pinout.png)|
|---|---|---|
<br>

A small Klipper fan / LED / thermistor controller based on the **Waveshare RP2350-Zero**, derived from [Gi7mo/TinyFan](https://github.com/Gi7mo/TinyFan).

![PCB](./Images/TinyFan2350_top.png)
<br>

## Features
- **5 fan ports** (JST-XH 4-pin) for 2-, 3- and 4-pin fans, 0.6A each
  - every fan has its own PWM output and tacho input -> independent speeds
  - per fan: mode jumper (**4P** = 4-pin PWM, **2/3** = switched GND) and voltage jumper (**VIN** or **5V**)
- **2 addressable LED ports** (JST-XH 3-pin), data level-shifted to 5V, VIN or 5V per port
- **4 thermistor ports** (JST-XH 2-pin) on the RP2350 ADC
- **EXP header** with 4 free GPIOs (GP12-GP15)
- Inputs: **12/24V (VIN)** and **5V**, each with a mini blade fuse and reverse-polarity protection, no converters on board
- All bottom-side SMD parts are **JLCPCB Basic** parts (cheap Economic assembly)
- 2 layers, 1 oz copper, black solder mask; SMD parts only on the bottom, THT only on the top; socketed MCU
- 4x M3 mounting holes (93 x 58 mm) and a printable **DIN rail mount** ([CAD](./CAD))

![Pinout](./Images/TinyFan2350_Pinout.png)

## Quick start
1. Build the board ([PCB](./PCB)), plug the RP2350-Zero into its socket.
2. Set every fan **mode** and **voltage** jumper and both LED voltage jumpers.
3. Flash Klipper for the RP2350 and add [TinyFan2350.cfg](./Klipper/TinyFan2350.cfg) ([Klipper](./Klipper)).
4. Connect power: VIN 12-24V and 5V (+ is the lower pin of each terminal).

## DIN rail mount
A printed tray carries the board on a 35 mm DIN rail with one
[DIN Rail Clip (Heat Insert Version)](https://www.printables.com/model/537942-din-rail-clip-heat-insert-version).
Files and instructions: [CAD](./CAD), [STL](./STL).

![DIN rail mount](./Images/TinyFan2350_DIN_Mount_Assembly.png)

## Notes
- Original TinyFan by [Gi7mo](https://github.com/Gi7mo/TinyFan), idea by [Rama](https://github.com/Ramalama2).
- This is a first revision: it passes KiCad ERC/DRC, but has not been built or tested yet.

## License
GPL-3.0, the same as the original TinyFan. See [LICENSE](./LICENSE).

## Disclaimer
This project is provided on an "as-is" basis, without any warranty of any kind. I am not responsible for any damage, injury, loss or other issues caused by building or using it. If you choose to build or use this board, you do so entirely at your own risk.
