# Klipper setup

TinyFan2350 runs as a secondary Klipper MCU on USB. These steps assume Klipper is already installed on the host (Pi, CB1, etc.).

## 1. Build the firmware

```bash
cd ~/klipper
make menuconfig
```

| Option | Value |
|---|---|
| Micro-controller Architecture | Raspberry Pi RP2040/RP235x |
| Processor model | **rp2350** |
| Bootloader offset | No bootloader |
| Communication interface | USBSERIAL |

```bash
make clean
make
```

## 2. Flash

1. Unplug the RP2350-Zero. Hold its **BOOT** button, plug the USB cable into the host, then release BOOT.
2. Check that it shows up: `lsusb` should list `2e8a:000f`.
3. Flash:

```bash
sudo service klipper stop
make flash FLASH_DEVICE=2e8a:000f
sudo service klipper start
```

> Dragging `klipper.uf2` onto the boot drive does **not** work for the RP2350 build. Use `make flash` or `picotool load -x out/klipper.uf2`.

4. Find the serial id:

```bash
ls /dev/serial/by-id/
# usb-Klipper_rp2350_XXXXXXXXXXXXXXXX-if00
```

Later updates can be flashed without pressing BOOT:
`make flash FLASH_DEVICE=/dev/serial/by-id/usb-Klipper_rp2350_...-if00`

## 3. Add the config

1. Copy [`klipper/tinyfan.cfg`](../klipper/tinyfan.cfg) next to your `printer.cfg`.
2. Paste in your serial id under `[mcu tinyfan]`.
3. Add `[include tinyfan.cfg]` to `printer.cfg`.
4. Delete or comment out the sections for anything you don't have connected. **An enabled thermistor with nothing plugged in shuts Klipper down** ("ADC out of range").
5. `FIRMWARE_RESTART`.

## 4. Test

```
SET_FAN_SPEED FAN=fan1 SPEED=0.5
QUERY_ADC                                 ; optional
SET_LED LED=led1 RED=0.2 GREEN=0 BLUE=0
```

Fan RPM appears in Mainsail/Fluidd next to each fan. If the RPM reads 0 while the fan is spinning, the fan's tach wire is not on XH pin 3, or the fan has no tach.

## Pin map

| Function | Pin alias | GPIO |
|---|---|---|
| FAN1 PWM / TACH | `tinyfan:FAN1_PWM` / `FAN1_TACH` | gpio0 / gpio1 |
| FAN2 PWM / TACH | `FAN2_PWM` / `FAN2_TACH` | gpio2 / gpio3 |
| FAN3 PWM / TACH | `FAN3_PWM` / `FAN3_TACH` | gpio4 / gpio5 |
| FAN4 PWM / TACH | `FAN4_PWM` / `FAN4_TACH` | gpio6 / gpio7 |
| FAN5 PWM / TACH | `FAN5_PWM` / `FAN5_TACH` | gpio8 / gpio9 |
| FAN6 PWM / TACH | `FAN6_PWM` / `FAN6_TACH` | gpio10 / gpio11 |
| LED1 / LED2 data | `LED1` / `LED2` | gpio12 / gpio13 |
| TH1-TH4 | `TH1`...`TH4` | gpio26-gpio29 |
| EXP | `EXP_GP15` / `EXP_GP14` | gpio15 / gpio14 |
| On-module RGB LED | `STATUS_LED` | gpio16 |

## Notes

- **PWM** runs at 25 kHz (`cycle_time: 0.00004`) on hardware PWM. Each fan uses its own PWM slice, so the ports don't interfere with each other.
- The tach inputs have **external** 10k pull-ups, so don't add `^` to `tachometer_pin`.
- The thermistor pull-up is 4.7k, so keep `pullup_resistor: 4700`.
- Sensor types: `Generic 3950` covers most 100k chamber thermistors. Use `ATC Semitec 104GT-2` for 104GT probes, and so on.
- To give a port a role (controller fan, temperature fan, Nevermore), see the commented examples at the bottom of `tinyfan.cfg`. Remove the matching `fan_generic` block first, because a pin can only be used once.
