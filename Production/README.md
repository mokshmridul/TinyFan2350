# Build it

## Order the PCB

Files in this folder:

|File|Use|
|---|---|
|[GERBER-TinyFan2350.zip](./GERBER-TinyFan2350.zip)|the PCB (Gerbers + drill)|
|[JLC-Economic-BOM-bottom.csv](./JLC-Economic-BOM-bottom.csv)|JLCPCB assembly: parts list|
|[JLC-Economic-CPL-bottom.csv](./JLC-Economic-CPL-bottom.csv)|JLCPCB assembly: part positions|
|[TinyFan2350_Schematic.pdf](./TinyFan2350_Schematic.pdf)|schematic|

**PCB only** (e.g. [jlcpcb](https://jlcpcb.com/) or [pcbway](https://www.pcbway.com/)): upload the Gerber zip.
2 layers, 1.6 mm, 1 oz copper, **black** solder mask.

**PCB with the SMD parts fitted (JLCPCB Economic assembly)** - you only solder the through-hole parts:
1. Upload the Gerber zip, enable **PCB Assembly**, choose **Economic**, assembly side **Bottom Side**.
2. Upload the BOM and the CPL file.
3. Check every part in the placement preview. Things to check: Q1-Q7 (SOT-23) and the cathode bar of D1-D13
   (D14 works either way round). If JLC shows a part rotated, fix it in the preview (usually 180°).

All 38 SMD parts are JLCPCB **Basic** parts, so there are no extended-part fees. Stock changes daily: if a part is out
of stock, pick an equivalent Basic part in the JLC BOM step.

## Parts

|Reference|Qty|Part|LCSC|Fitted by|
|---|---|---|---|---|
|Q1 - Q5|5|AO3400A (SOT-23)|C20917|JLCPCB|
|Q6 Q7|2|2N7002 (SOT-23)|C8545|JLCPCB|
|D3 - D8|6|B5819W SL (SOD-123)|C8598|JLCPCB|
|D9 - D13|5|1N4148WS (SOD-323)|C2128|JLCPCB|
|D1 D2|2|SS54 (SMA)|C22452|JLCPCB|
|D14|1|P6SMB6.8CA (SMB)|C78395|JLCPCB|
|R3 - R11|9|4.7k 0603|C23162|JLCPCB|
|R1 R2|2|330R 0603|C23138|JLCPCB|
|R12 R13|2|470R 0603|C23179|JLCPCB|
|C4 - C7|4|100nF 0603|C14663|JLCPCB|
|C1|1|100uF 35V radial 8mm, pitch 3.5|-|you|
|C2|1|100uF 16V radial 6.3mm, pitch 2.5|-|you|
|F1 F2|2|Keystone 3568 mini blade fuse holder|C5249699 (verify)|you|
|F1 F2 fuse|2|ATM mini blade fuse, 3-5A|-|you|
|J1 J2|2|Screw terminal 2-pin, 5.08mm|-|you|
|J3 - J7|5|JST B4B-XH-A|C144395 (verify)|you|
|J8 J9|2|JST B3B-XH-A|C144394 (verify)|you|
|J10 - J13|4|JST B2B-XH-A|C158012 (verify)|you|
|JP1 - JP12|12|Pin header 1x3 2.54mm + jumper cap|C2937625 (verify)|you|
|J14|1|Pin header 1x6 2.54mm|C492405 (verify)|you|
|U1 socket|2|Female header 1x9 2.54mm, 8.5mm high|C39576 (verify)|you|
|U1 socket|1|Female header 1x5 2.54mm, 8.5mm high|C50950 (verify)|you|
|U1|1|Waveshare RP2350-Zero (with pin headers)|-|plug in|

The LCSC numbers of the SMD parts were checked against jlcpcb.com. The ones marked *verify* were not.

## Solder the through-hole parts

All through-hole parts go on the **top**: C1 C2, the fuse holders, the screw terminals (wire entry to the board edge),
the JST connectors, the jumper and EXP headers and the three female headers for the RP2350-Zero.

- Solder the male pin headers onto the RP2350-Zero, then plug it in with the USB-C pointing off the board edge.
- Before the first power-up: set all jumpers, fit the fuses and check the polarity of both inputs
  (+ is the lower screw of each terminal). See [Set it up](../Klipper).

## Board

- 100 x 65 mm, 4x M3 mounting holes 3.5 mm from the edges (93 x 58 mm)
- 2 layers, 1 oz copper, 1.6 mm FR4, black solder mask, white silkscreen
- All SMD parts on the bottom, all through-hole parts on the top
- KiCad 10 project: [KiCad](../KiCad). After a board change, [Tools](../Tools) regenerates the files in this folder.

## Safety notes
- Inputs are fused. Reverse polarity on either input is shorted by an SS54 diode and blows the fuse; 12/24V on the 5V input is clamped by the TVS (D14) and blows F2. Use fast-acting fuses sized to your load (5A max).
- The VIN input has no TVS (there is no JLC Basic part for it): use a regulated 12V or 24V supply. The fan MOSFETs are rated 30V.
- There is no per-channel fan protection: a shorted fan cable in 2/3 mode can destroy that channel's MOSFET before a large fuse blows - keep fuse ratings close to the real load.
- 5V fans / 5V LED strips on a VIN jumper setting will be destroyed.
- Thermistor inputs connect directly to the RP2350 ADC; never route thermistor wires together with heater / 24V wires.
- USB and the 5V input are separated by a Schottky diode (USB cannot power the fans); a 5V PSU set much above 5.2V can push a little current back into a connected USB host.
