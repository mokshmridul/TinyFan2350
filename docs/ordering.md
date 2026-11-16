# Ordering a fully built board (JLCPCB or PCBWay)

All the files are in [`hardware/fab/`](../hardware/fab):

| File | What it is | Upload it to |
|---|---|---|
| `TinyFan2350_GERBERS_upload.zip` | Copper, mask, silk, paste, outline and drill | JLCPCB and PCBWay, PCB step |
| `TinyFan2350_BOM_JLCPCB.csv` | Bill of materials with LCSC part numbers | JLCPCB assembly step ("BOM") |
| `TinyFan2350_CPL_JLCPCB.csv` | Where each part goes, and its rotation | JLCPCB assembly step ("CPL") and PCBWay ("Centroid") |
| `TinyFan2350_BOM_PCBWay.csv` | The same BOM with makers and maker part numbers | PCBWay assembly step |
| `TinyFan2350-pos.csv` | KiCad's own position file (raw, for reference) | Any assembler that wants KiCad format |

**What the assembler does not fit:**

- **U1, the RP2350-Zero.** It sits in female header sockets that you solder yourself: 2 x 1x9 and 1 x 1x5, cut from a 2.54 mm female strip (5 minutes, see [assembly.md](assembly.md)). Solder male headers to the module too, if it didn't come with them.
- **J5, the EXP header.** Optional. Solder a 1x4 male header if you want it.
- You fit the **fuses** (F1: 7.5A, F2: 5A mini blade) and the **6 jumper caps** yourself.

The two Keystone 3568 fuse holders (F1, F2) **are** in the BOM (LCSC C5249699). If you'd rather fit your own, delete that line from the BOM before you upload it, and the assembler will leave the holes empty.

If JLCPCB shows a shortage: for **F1/F2** untick the line and fit the holders yourself (4 big through-hole pins). For **U2** the BOM already uses 74HCT2G17GW-Q100H (C547569). If that is short too, 74HCT2G34GW-Q100H (C547575) is a drop-in: same 5V HCT dual buffer, same pinout and package.

## JLCPCB

1. Go to jlcpcb.com, click **Order now** and drop in `TinyFan2350_GERBERS_upload.zip`. It should read the board as **100 x 63 mm, 2 layers**.
2. PCB options:
   - Base material FR-4, 2 layers, 1.6 mm. Leave the rest at the defaults.
   - Surface finish: HASL lead-free (cheapest) or ENIG.
   - PCB colour: **Black** (white silkscreen). Takes the same time as green at JLC.
   - Copper: **2 oz (required).** With six 0.8A fans the VIN traces carry up to ~7A; 1 oz would run them too hot.
   - "Remove order number": pick *Specify a location* only if you want it hidden. Otherwise any choice is fine.
3. Turn on **PCB Assembly**:
   - PCBA type: **Standard** (it needs through-hole soldering for the connectors).
   - **Assembly side: Both sides.** Most SMD parts are on the bottom; the 8 indicator LEDs and their resistors are on the top so you can see them. The connectors, caps and fuse holders on the top are through-hole, and JLCPCB solders those separately. (Both-side SMT adds a little to the setup cost.)
   - Tooling holes: *Added by JLCPCB*.
4. Click **Next**, then upload **`TinyFan2350_BOM_JLCPCB.csv`** as the BOM and **`TinyFan2350_CPL_JLCPCB.csv`** as the CPL.
5. On the parts page every line should be matched to its LCSC number. U1 and J5 will show as "not in BOM". That is expected.
   - U2 is the automotive version **74HCT2G17GW-Q100H** (C547569), the same chip as 74HCT2G17GW,125 (C547568), which often runs short. Do **not** accept a `74HC2G17` (no T): it won't read 3.3V reliably at 5V.
6. **Check the placement preview.** JLCPCB's footprints don't always use KiCad's zero rotation, so look at each part type once:
   - **D1-D6** (BAT54S) and **Q4-Q9** (AO3400A), both SOT-23: the single pin should be on the same side as the single pad.
   - **D7-D18** (SOD-123), **D21/D22** (big TVS diodes) and **LD1-LD8** (LEDs): the cathode band/mark should be on pad 1, the one marked on the silk.
   - **D19/D20** (BAT54S, SOT-23): single pin on the same side as the single pad.
   - **Q1-Q3** (BSS138DW) and **U2** (74HCT2G17): the pin-1 dot on the part should sit on the pad marked with the dot on the silk.
   - **RN1-RN6**: the four pads on each long side should line up with the part's terminals (it is not polarised, but it must not be turned 90°).
   - **C5 and C6**: the stripe (minus) should face away from the square pad.
   - Fix anything that is off with the rotate button. JLCPCB's engineers also check orientation and will email you if something looks wrong.
7. Confirm and pay. Lead time is usually a few days plus shipping.

## PCBWay

1. pcbway.com → **PCB Instant Quote** → upload `TinyFan2350_GERBERS_upload.zip`. 2 layers, 100 x 63 mm, 1.6 mm, **2 oz**, HASL or ENIG, solder mask **Black**, silkscreen White.
2. Tick **Assembly service**: *Turnkey*, **SMT on both sides** plus through-hole.
3. Upload **`TinyFan2350_BOM_PCBWay.csv`** as the BOM and **`TinyFan2350_CPL_JLCPCB.csv`** as the centroid file. PCBWay sources parts by the maker part number column. LCSC numbers are included as a second reference.
4. In the remarks, add: *"Do not fit U1 and J5. SMD on both sides (LEDs LD1-LD8 and R33-R40 on top, the rest on the bottom). Please confirm the orientation of D1-D22, Q1-Q9, U2, LD1-LD8 and C5/C6."*
   In the JLC/PCBWay preview, C6 (470 µF polymer) may show as bare pads with no 3D model. It is still in the BOM and centroid file, so it gets fitted. Polarity: + is the square pad. Screw terminals: wire openings face the board edge.
5. PCBWay reviews the files and sends a quote with any part questions. Answer those, then pay.

## When the boards arrive

1. Check for shorts with a meter before anything else ([assembly.md](assembly.md), "Before first power-up").
2. Solder the RP2350-Zero sockets.
3. Fit a 7.5A fuse in F1 and a 5A fuse in F2, set every fan jumper, then follow [wiring.md](wiring.md) and [klipper.md](klipper.md).
