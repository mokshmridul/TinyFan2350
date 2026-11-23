## Pictures

### Board
![](./TinyFan2350_top.png)
![](./TinyFan2350_iso.png)
![](./TinyFan2350_bottom.png)

### Pinout, jumpers, wiring
![](./TinyFan2350_Pinout.png)
![](./TinyFan2350_Jumpers.png)
![](./TinyFan2350_Wiring.png)

### Flashing
![](./TinyFan2350_Flashing.png)
![](./Menuconfig_Katapult.png)
![](./Menuconfig_Klipper_Katapult.png)
![](./Menuconfig_Klipper.png)

### DIN rail mount
![](./TinyFan2350_DIN_Mount_BOM.png)
![](./TinyFan2350_DIN_Mount_Assembly.png)
![](./TinyFan2350_DIN_Mount.png)
![](./TinyFan2350_DIN_Mount_Underside.png)
![](./TinyFan2350_DIN_Mount_Exploded.png)
![](./TinyFan2350_DIN_Mount_Bottom.png)
![](./TinyFan2350_DIN_Mount_Side.png)

### How the drawings are made
The pinout, jumper, wiring, flashing and menuconfig pictures are drawn by the scripts in [`src`](./src), in the style of
the original [TinyFan](https://github.com/Gi7mo/TinyFan) pictures. The menuconfig pictures are drawings of the screens,
not screenshots.

After a board change:
1. `dump_layout.py` (run with KiCad's Python) reads the board and writes `layout.json`.
2. `make_illustrations.py` (Python with matplotlib) redraws the pictures.

The lettering is [osifont](https://github.com/hikikomori82/osifont) (LGPL v3 with font exception).
