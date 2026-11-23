## TinyFan2350 PCB Sources:
- KiCad project: `../TinyFan2350.kicad_pro` (KiCad 10), project libraries `../TinyFan2350.kicad_sym`, `../TinyFan2350.pretty`, 3D model in `../3d`
- Schematic as PDF: [TinyFan2350_Schematic.pdf](./TinyFan2350_Schematic.pdf)
- ProductionFiles folder: Gerber + drill (zip), full BOM, JLCPCB Economic BOM + CPL (bottom SMD only), KiCad position file
- `make_production_files.py`: regenerates the production files from the board

## Board specs:
- 100 x 65 mm, 4x M3 mounting holes (3.5 mm from the edges)
- **2 layers, 1 oz copper, 1.6 mm FR4, black solder mask, white silkscreen**
- All SMD parts on the **bottom**, all through-hole parts on the **top**
- Power: VIN 12-24V input and 5V input (screw terminals), each with a mini blade fuse (5A max) and a reverse-polarity Schottky crowbar (SS54); the 5V input also has a TVS against over-voltage. No converters on the board.
- 5x fan ports (JST-XH 4-pin, 2/3/4-pin fans), 0.6A each, independent PWM + tacho, VIN or 5V per port
- 2x addressable LED ports (JST-XH 3-pin), data level-shifted to 5V (2N7002), VIN or 5V per port, 3A max each
- 4x thermistor ports (JST-XH 2-pin), 4.7k pull-up
- EXP header: GND, 3V3, GP12-GP15
- MCU: Waveshare RP2350-Zero in a socket (2x 1x9 + 1x5 female headers, 8.5 mm)

## BOM:
|Reference                    |Quantity|Value                          |LCSC              |Side|
|-----------------------------|--------|-------------------------------|------------------|----|
|Q1 Q2 Q3 Q4 Q5               |5       |AO3400A (SOT-23)               |C20917            |bottom|
|Q6 Q7                        |2       |2N7002 (SOT-23)                |C8545             |bottom|
|D3 D4 D5 D6 D7 D8            |6       |B5819W SL (SOD-123)            |C8598             |bottom|
|D9 D10 D11 D12 D13           |5       |1N4148WS (SOD-323)             |C2128             |bottom|
|D1 D2                        |2       |SS54 (SMA)                     |C22452            |bottom|
|D14                          |1       |P6SMB6.8CA (SMB)               |C78395            |bottom|
|R3 - R11                     |9       |4.7k 0603                      |C23162            |bottom|
|R1 R2                        |2       |330R 0603                      |C23138            |bottom|
|R12 R13                      |2       |470R 0603                      |C23179            |bottom|
|C4 - C7                      |4       |100nF 0603                     |C14663            |bottom|
|C1                           |1       |100uF 35V radial 8mm, P3.5     |-                 |top|
|C2                           |1       |100uF 16V radial 6.3mm, P2.5   |-                 |top|
|F1 F2                        |2       |Keystone 3568 mini blade holder|C5249699 (verify) |top|
|F1 F2 fuse                   |2       |ATM mini blade fuse, 3-5A      |-                 |-|
|J1 J2                        |2       |Screw terminal 2P 5.08mm       |-                 |top|
|J3 - J7                      |5       |JST B4B-XH-A                   |C144395 (verify)  |top|
|J8 J9                        |2       |JST B3B-XH-A                   |C144394 (verify)  |top|
|J10 - J13                    |4       |JST B2B-XH-A                   |C158012 (verify)  |top|
|JP1 - JP12                   |12      |Pin header 1x3 2.54mm + jumper cap|C2937625 (verify)|top|
|J14                          |1       |Pin header 1x6 2.54mm          |C492405 (verify)  |top|
|RP2350 9Pin Female Headers   |2       |1x9 2.54mm, 8.5mm              |C39576 (verify)   |top|
|RP2350 5Pin Female Headers   |1       |1x5 2.54mm, 8.5mm              |C50950 (verify)   |top|
|U1                           |1       |Waveshare RP2350-Zero (with pin headers)|-        |socket|

**All 38 bottom-side SMD parts are JLCPCB Basic parts (no extended-part fees).** Their LCSC numbers were checked against jlcpcb.com. Through-hole LCSC numbers marked *verify* were not - you solder those yourself anyway.

Design rule for future changes: use JLCPCB **Basic** parts for anything on the bottom side.

## Assembly
**PCB:** order at e.g. [jlcpcb](https://jlcpcb.com/) or [pcbway](https://www.pcbway.com/): upload `ProductionFiles/GERBER-TinyFan2350.zip`, 2 layers, 1.6 mm, 1 oz, **black** solder mask.

**JLCPCB Economic PCBA (SMD bottom side only, you solder the through-hole parts):**
1. Upload `ProductionFiles/GERBER-TinyFan2350.zip`, enable **PCB Assembly**, choose **Economic**, assembly side **Bottom Side**.
2. BOM file: `ProductionFiles/JLC-Economic-BOM-bottom.csv`
3. CPL file: `ProductionFiles/JLC-Economic-CPL-bottom.csv`
4. Check every part in the placement preview before confirming. Pin 1 / cathode markings to check: Q1-Q7 (SOT-23), D1-D13 (diode cathode bar; D14 is bidirectional, orientation does not matter). If JLC shows a part rotated, fix it in the preview (usually 180°).

|BOM line|Parts|LCSC|JLC type|
|---|---|---|---|
|100nF 0603|C4-C7|C14663|Basic|
|SS54|D1 D2|C22452|Basic|
|B5819W SL|D3-D8|C8598|Basic|
|1N4148WS|D9-D13|C2128|Basic|
|P6SMB6.8CA|D14|C78395|Basic|
|AO3400A|Q1-Q5|C20917|Basic|
|2N7002|Q6 Q7|C8545|Basic|
|330R 0603|R1 R2|C23138|Basic|
|4.7k 0603|R3-R11|C23162|Basic|
|470R 0603|R12 R13|C23179|Basic|

38 parts, 10 lines, **0 extended parts**. Stock changes daily - if a part is out of stock, pick an equivalent Basic part in the JLC BOM step.

**Through-hole (hand soldered, top):** C1 C2, F1 F2 holders, J1 J2 terminals, J3-J13 JST-XH, JP1-JP12 + J14 headers, the 2x 1x9 + 1x5 female headers for the RP2350-Zero.
- Solder the male pin headers onto the RP2350-Zero (USB-C pointing to the board edge), the female headers onto the TinyFan2350, then plug the module in.
- Before the first power-up: set all mode and voltage jumpers, insert fuses, check the polarity of both inputs (+ is the lower terminal pin, - the upper).

**Regenerating the production files** after any board change (KiCad 10):
```
"C:\Program Files\KiCad\10.0\bin\python.exe" PCB\make_production_files.py
```
This rewrites the Gerber zip, the JLC BOM/CPL and the KiCad position file in `ProductionFiles`.

## Safety notes
- Inputs are fused. Reverse polarity on either input is shorted by an SS54 diode and blows the fuse; 12/24V on the 5V input is clamped by the TVS (D14) and blows F2. Use fast-acting fuses sized to your load (5A max).
- The VIN input has no TVS (there is no JLC Basic part for it): use a regulated 12V or 24V supply. The fan MOSFETs are rated 30V.
- There is no per-channel fan protection: a shorted fan cable in 2/3 mode can destroy that channel's MOSFET before a large fuse blows - keep fuse ratings close to the real load.
- 5V fans / 5V LED strips on a VIN jumper setting will be destroyed.
- Thermistor inputs connect directly to the RP2350 ADC; never route thermistor wires together with heater / 24V wires.
- USB and the 5V input are separated by a Schottky diode (USB cannot power the fans); a 5V PSU set much above 5.2V can push a little current back into a connected USB host.
