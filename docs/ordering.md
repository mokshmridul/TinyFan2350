# Ordering the board (JLCPCB or PCBWay)

The easiest way to get a TinyFan2350 is to have a PCB factory make it **and** solder the parts on. You upload three files, choose a few options and pay. This page goes through it step by step.

## The files

Everything is in [`hardware/fab/`](../hardware/fab). Download these three, and leave them as they are (don't unzip the zip):

| File | What it is | Where it goes |
|---|---|---|
| `TinyFan2350_GERBERS_upload.zip` | The board itself: copper, colours, text, outline, holes | First page of the order (JLCPCB and PCBWay) |
| `TinyFan2350_BOM_JLCPCB.csv` | **BOM** = Bill Of Materials, the parts list with LCSC part numbers | JLCPCB assembly page, "BOM" |
| `TinyFan2350_CPL_JLCPCB.csv` | **CPL** = where each part sits and which way it turns | JLCPCB "CPL", and PCBWay "Centroid" |
| `TinyFan2350_BOM_PCBWay.csv` | The same parts list, with each maker's part number | PCBWay assembly page, instead of the JLCPCB BOM |

`TinyFan2350-pos.csv` is KiCad's raw position file. You only need it if an assembler asks for the KiCad format.

## What you buy yourself

The factory does not fit these. They are cheap and easy to find (Robu, Amazon, AliExpress, LCSC):

| Qty | Part | Notes |
|---|---|---|
| 1 | **Waveshare RP2350-Zero** | With its pin headers. If the headers are not soldered on, you solder them (see [assembly.md](assembly.md)) |
| 1 strip | **2.54 mm female header strip** | You cut two 9-pin pieces and one 5-pin piece from it, for the RP2350-Zero socket |
| 2 | **5 A mini blade fuse** (ATM / "mini", 32 V) | One in F1, one in F2. Buy a few spares |
| 14 | **2.54 mm jumper caps** | One for each 3-pin jumper: 6 x MODE (JM), 6 x FAN V (JP), 2 x LED V (JL) |
| - | JST-XH housings and crimp pins | To fit your fans, LEDs and thermistors with the right plugs (see [wiring.md](wiring.md)) |
| optional | 1 x 4 male pin header | Only if you want the EXP header (J5) |

The two blade fuse holders (Keystone 3568) **are** in the factory BOM. If you'd rather solder your own, delete that line from the BOM before you upload it, and the factory will leave the holes empty.

## JLCPCB, step by step

1. Go to jlcpcb.com, click **Order now** and drop in `TinyFan2350_GERBERS_upload.zip`. It should show **100 x 63 mm, 2 layers**.
2. Board options. Leave everything not listed here at the default:
   - **Base material** FR-4, **Layers** 2, **Thickness** 1.6 mm.
   - **PCB colour: Black** (it comes with white text). It takes the same time as green at JLC.
   - **Surface finish:** HASL lead-free (cheapest) or ENIG (gold-coloured, a bit more expensive). Both are fine.
   - **Copper weight: 1 oz.** That is enough for everything this board is rated for (up to 5 A on VIN). You don't need 2 oz.
   - **Remove order number:** any choice is fine.
3. Switch on **PCB Assembly**:
   - **PCBA type: Standard** (the connectors are through-hole parts, so Economic can't be used for a full build).
   - **Assembly side.** There are two options:
     - **Both sides**: you get a finished board. Only the RP2350-Zero socket is left for you to solder.
     - **Bottom side only**: cheaper, because there is only one setup fee. Almost every small part is on the bottom. You then solder the 8 small green LEDs (LD1-LD8) on the top yourself; they are easy 0805 size. See [assembly.md](assembly.md).
   - **Tooling holes:** *Added by JLCPCB*.
4. Click **Next**. Upload **`TinyFan2350_BOM_JLCPCB.csv`** as the BOM and **`TinyFan2350_CPL_JLCPCB.csv`** as the CPL.
5. **Parts page.** Every line should be matched to a part with a tick. **U1 and J5 show as "not in BOM". That is expected**, because you fit them yourself.
   - A few parts are JLC "extended" parts (for example the fan switch MOSFETs SI2308A, the input protection diode SMCJ30A and the self-resetting fuses). JLC adds a small one-time fee for each extended part type. That is normal.
   - **U2** must be **74HCT2G17**, with **HCT** (it is listed as 74HCT2G17GW-Q100H, C547569). Do **not** accept a "74HC2G17" (without the T) as a substitute: it does not reliably read the RP2350's 3.3 V signals.
   - If a part is out of stock, see [If a part is out of stock](#if-a-part-is-out-of-stock) below.
6. **Check the placement preview.** JLC draws each part on the board. Sometimes a part is turned the wrong way, so check one of each kind:
   - **3-legged parts** (D1-D6, D19, D20, Q4-Q15, all SOT-23): the single leg must sit on the single pad.
   - **Diodes and LEDs** (D7-D18, D21, D22, LD1-LD8): the stripe on the part must be at the pad marked on the board (pad 1).
   - **U2** (6 tiny legs): the dot on the chip must be at the dot on the board.
   - **C5 and C6** (the two round capacitors): the + leg goes in the square pad.
   - **C6 may show only as bare pads** with no 3D picture. It is still in the BOM and will be fitted.
   - If something is turned wrong, select it and press rotate until it matches. JLC's engineers also check this and will email you if anything looks wrong.
7. Confirm and pay. Production is usually a few days, plus shipping.

## PCBWay, step by step

1. pcbway.com → **PCB Instant Quote** → upload `TinyFan2350_GERBERS_upload.zip`. Choose 2 layers, 100 x 63 mm, 1.6 mm thick, **1 oz** copper, HASL or ENIG, solder mask **Black**, silkscreen **White**.
2. Tick **Assembly service**: *Turnkey* (PCBWay buys the parts), **SMT on both sides** plus through-hole.
3. Upload **`TinyFan2350_BOM_PCBWay.csv`** as the BOM and **`TinyFan2350_CPL_JLCPCB.csv`** as the centroid (position) file. PCBWay buys parts using the maker part number column. The LCSC numbers are there as a second reference.
4. In the remarks box, paste this:
   *"Do not fit U1 and J5. SMD parts on both sides (LEDs LD1-LD8 on top, the rest on the bottom). Please confirm the orientation of D1-D22, Q4-Q15, U2, LD1-LD8 and C5/C6. C6 is polarised: + is the square pad. Screw terminals: wire openings face the board edge."*
5. PCBWay checks the files and sends you a quote, sometimes with questions about parts. Answer those, then pay.

## If a part is out of stock

- **F1/F2 fuse holders:** untick the line and solder the holders yourself (4 big pins each).
- **U2:** 74HCT2G34GW-Q100H (C547575) works the same: it is also a 5 V HCT dual buffer, with the same legs and size.
- **Q4-Q9 (SI2308A):** use another **60 V** N-channel MOSFET in SOT-23 with pin 1 = Gate, 2 = Source, 3 = Drain and at most about 0.15 ohm at 4.5 V gate drive (for example IRLML0060). **Do not go back to a 30 V part such as AO3400A**: that would remove the safety margin on 24 V.
- **F3-F10 (self-resetting fuses):** any 1812-size PTC rated **at least 33 V**, with 1.5 A hold current for F3-F8 and 2 A hold current for F9-F10.
- **D21 (SMCJ30A):** any SMCJ30A (stand-off 30 V, SMC size) from another maker.

## When the boards arrive

1. Before anything else, check with a meter that the power inputs are not shorted ([assembly.md](assembly.md#before-you-power-it-on-the-first-time)).
2. Solder the RP2350-Zero socket strips.
3. Put a 5 A fuse in F1 and in F2, set every jumper, then follow [wiring.md](wiring.md) and [klipper.md](klipper.md).
