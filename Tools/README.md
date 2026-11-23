# Tools

Scripts that regenerate the outputs after a change to the KiCad board. Nothing here is needed to build or use the board.

|Script|Run with|Writes|
|---|---|---|
|`make_production_files.py`|KiCad's Python|Gerber zip, JLCPCB BOM + CPL and schematic PDF in [Production](../Production); the four board pictures in [Images](../Images)|
|`dump_layout.py`|KiCad's Python|`layout.json`, the part positions used by the drawings|
|`make_illustrations.py`|Python with matplotlib|pinout, jumper, wiring, flashing and menuconfig pictures in [Images](../Images)|
|`make_rp2350_zero_model.py`|Python with CadQuery|the simplified RP2350-Zero 3D model in [KiCad/3d](../KiCad/3d)|

After a board change (Windows, KiCad 10):
```
"C:\Program Files\KiCad\10.0\bin\python.exe" Tools\make_production_files.py
"C:\Program Files\KiCad\10.0\bin\python.exe" Tools\dump_layout.py
python Tools\make_illustrations.py
```

`make_production_files.py` stops with an error if an SMD part sits on the top side or has no LCSC number.
Parts marked *do not populate* in KiCad are left out of the BOM, the placement file and the pictures.
The picture of the top side without the RP2350-Zero is rendered from a temporary copy of the board that has the
module's 3D model taken out.
`tinyfan_art.py` is the drawing library; the lettering is [osifont](https://github.com/hikikomori82/osifont) (LGPL v3 with font exception).
