# Klipper setup

TinyFan2350 works as a **second MCU** in Klipper: your printer's main board stays as it is, and Klipper also talks to the TinyFan over USB. These steps assume Klipper already runs on your host (Raspberry Pi, CB1, etc.) and that you can log in to it over SSH.

You do this once: build Klipper for the RP2350, copy it onto the RP2350-Zero, then tell Klipper where to find it.

## 1. Build the firmware

Log in to your host and run:

```bash
cd ~/klipper
make menuconfig
```

In the menu, set these options (arrow keys to move, Enter to choose), then press **Q** and **Y** to save:

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

1. Unplug the RP2350-Zero. Hold its **BOOT** button (the small button on the module), plug the USB cable into the host, then let go of BOOT. The module is now waiting for new firmware.
2. Check that the host can see it: run `lsusb`. One line should show `2e8a:000f`.
3. Flash:

```bash
sudo service klipper stop
make flash FLASH_DEVICE=2e8a:000f
sudo service klipper start
```

> Dragging `klipper.uf2` onto the boot drive does **not** work for the RP2350 build. Use `make flash` or `picotool load -x out/klipper.uf2`.

4. Find the module's serial id (its unique name):

```bash
ls /dev/serial/by-id/
# usb-Klipper_rp2350_XXXXXXXXXXXXXXXX-if00
```

Later Klipper updates can be flashed without pressing BOOT:
`make flash FLASH_DEVICE=/dev/serial/by-id/usb-Klipper_rp2350_...-if00`

## 3. Add the config

1. Copy [`klipper/tinyfan.cfg`](../klipper/tinyfan.cfg) next to your `printer.cfg`.
2. Paste in your serial id under `[mcu tinyfan]`.
3. Add `[include tinyfan.cfg]` to `printer.cfg`.
4. Delete the sections for anything you haven't connected, or put `#` in front of each line to switch it off. **A thermistor section with no thermistor plugged in stops Klipper** with the error "ADC out of range".
5. Type `FIRMWARE_RESTART` in the Mainsail/Fluidd console.

## 4. Test

Type these in the console, one at a time:

```
SET_FAN_SPEED FAN=fan1 SPEED=0.5
QUERY_ADC                                 ; optional
SET_LED LED=led1 RED=0.2 GREEN=0 BLUE=0
```

The first line should start fan 1 at half speed, and the last should light LED strip 1 dim red. Fan RPM shows in Mainsail/Fluidd next to each fan. If RPM shows 0 while the fan spins, the fan's tach wire is not on pin 3 of the plug, or the fan has no tach wire.

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

- **4-pin fans** get a 25 kHz speed signal (`cycle_time: 0.00004`, the standard for PC fans). Each port has its own hardware timer, so the ports don't affect each other.
- **2/3-pin fans** (MODE jumper on the left, `2/3`) need `cycle_time: 0.010` (100 Hz). That is already in the commented example in `tinyfan.cfg`.
  - **Important: set `cycle_time: 0.010` for every port whose MODE (JM) jumper is on `2/3`.** At the default 25 kHz signal the 2/3-pin fan switch (MOSFET) on the board overheats.
  - **RPM readings are not meaningful while a 2/3-pin fan is being PWM'd** - the tach pin only shows the switch-on level. Ignore any RPM value on those ports.
- The RPM inputs already have resistors on the board, so **don't** add `^` in front of `tachometer_pin`.
- The board's thermistor resistor is 4.7k, so keep `pullup_resistor: 4700`.
- `sensor_type: Generic 3950` suits most 100k thermistors. For a 104GT probe use `ATC Semitec 104GT-2`.
- To give a port a job (controller fan, temperature-controlled fan, Nevermore filter), copy one of the examples at the bottom of `tinyfan.cfg`. First delete that port's `fan_generic` section, because Klipper lets each pin be used only once.
