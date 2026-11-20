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
| 14 | **2.54 mm jumper caps** | One for each 3-pin jumper: 6 x MODE (JM), 6 x FAN V (JP), 2 x LED V (JL) |
| - | JST-XH housings and crimp pins | To fit your fans, LEDs and thermistors with the right plugs (see [wiring.md](wiring.md)) |
| optional | 1 x 4 male pin header | Only if you want the EXP header (J5) |

The two main fuses (F1/F2, Littelfuse Nano2 5 A, LCSC C66503) are small SMD parts on the bottom and **are** fitted by the factory. You don't need to buy fuses. If you want a spare in the drawer, the same part is sold on Robu as *Littelfuse 0452005.MRL*.

## JLCPCB, step by step

1. Go to jlcpcb.com, click **Order now** and drop in `TinyFan2350_GERBERS_upload.zip`. It should show **89 x 58.1 mm, 2 layers**.
2. Board options. Leave everything not listed here at the default:
   - **Base material** FR-4, **Layers** 2, **Thickness** 1.6 mm.
   - **PCB colour: Black** (it comes with white text). It takes the same time as green at JLC.
   - **Surface finish:** HASL lead-free (cheapest) or ENIG (gold-coloured, a bit more expensive). Both are fine.
   - **Copper weight: 1 oz** is enough for the recommended loads (up to 4 A on VIN and 3.5 A on 5 V). Choose **2 oz** if you want extra margin or plan to run more current; it costs a little more and halves the copper heating (see [design notes](design-notes.md#copper-1-oz)).
   - **Remove order number:** any choice is fine.
3. Switch on **PCB Assembly**:
   - **PCBA type: Standard** (the connectors are through-hole parts, so Economic can't be used for a full build).
   - **Assembly side.** There are two options:
     - **Both sides**: you get a finished board. Only the RP2350-Zero socket is left for you to solder.
     - **Bottom side only**: cheaper, because there is only one setup fee. Every small part except the 8 green LEDs is on the bottom. You then solder the LEDs (LD1-LD8) on the top yourself; they are easy 0805 size. See [assembly.md](assembly.md).
   - **Tooling holes:** *Added by JLCPCB*.
4. Click **Next**. Upload **`TinyFan2350_BOM_JLCPCB.csv`** as the BOM and **`TinyFan2350_CPL_JLCPCB.csv`** as the CPL.
5. **Parts page.** Every line should be matched to a part with a tick. **U1 and J5 show as "not in BOM". That is expected**, because you fit them yourself.
   - A few parts are JLC "extended" parts (for example the fan switch MOSFETs SI2308A, the reverse-polarity MOSFETs AO4485 / AO4407A, the Nano2 fuses, the input protection diode SMCJ30A and the self-resetting fuses). JLC adds a small one-time fee for each extended part type. That is normal.
   - **U2** must be **74HCT2G17**, with **HCT** (it is listed as 74HCT2G17GW-Q100H, C547569). Do **not** accept a "74HC2G17" (without the T) as a substitute: it does not reliably read the RP2350's 3.3 V signals.
   - If a part is out of stock, see [If a part is out of stock](#if-a-part-is-out-of-stock) below.
6. **Check the placement preview.** JLC draws each part on the board. Sometimes a part is turned the wrong way, so check one of each kind:
   - **3-legged parts** (D1-D6, D19, D20, Q4-Q15, all SOT-23): the single leg must sit on the single pad.
   - **Diodes and LEDs** (D7-D18, D21-D24, LD1-LD8): the stripe on the part must be at the pad marked on the board (pad 1).
   - **U2** (6 tiny legs): the dot on the chip must be at the dot on the board.
   - **Q1 and Q2** (8 legs, near the screw terminals): the dot on the chip (pin 1) must be at pin 1 marked on the board. **Check these two carefully.** JLC's library sometimes draws this package turned by 180°. A turned Q1/Q2 would leave that input dead (it would not damage anything, but the board would not get power).
   - **C5 and C6** (the two round capacitors): the + leg goes in the square pad.
   - **C6 may show only as bare pads** with no 3D picture. It is still in the BOM and will be fitted.
   - If something is turned wrong, select it and press rotate until it matches. JLC's engineers also check this and will email you if anything looks wrong.
7. Confirm and pay. Production is usually a few days, plus shipping.

## PCBWay, step by step

1. pcbway.com → **PCB Instant Quote** → upload `TinyFan2350_GERBERS_upload.zip`. Choose 2 layers, 89 x 58.1 mm, 1.6 mm thick, **1 oz** copper (or 2 oz for extra margin), HASL or ENIG, solder mask **Black**, silkscreen **White**.
2. Tick **Assembly service**: *Turnkey* (PCBWay buys the parts), **SMT on both sides** plus through-hole.
3. Upload **`TinyFan2350_BOM_PCBWay.csv`** as the BOM and **`TinyFan2350_CPL_JLCPCB.csv`** as the centroid (position) file. PCBWay buys parts using the maker part number column. The LCSC numbers are there as a second reference.
4. In the remarks box, paste this:
   *"Do not fit U1 and J5. SMD parts on both sides (LEDs LD1-LD8 on top, the rest on the bottom). Please confirm the orientation of D1-D24, Q1, Q2, Q4-Q15, U2, LD1-LD8 and C5/C6. C6 is polarised: + is the square pad. Screw terminals: wire openings face the board edge. Q1/Q2 (SOIC-8): pin 1 at the pin-1 mark."*
5. PCBWay checks the files and sends you a quote, sometimes with questions about parts. Answer those, then pay.

## If a part is out of stock

- **F1/F2 (Nano2 5 A slow-blow):** another 5 A **slow-blow** fuse in the same 2410 (Nano2) size, rated 32 V or more, for example from Littelfuse's 454 series (0454005.MRL). Do not use a fast-acting fuse; the fans' start-up surge could blow it.
- **Q1 (AO4485):** any P-channel MOSFET in SOIC-8, at least **-40 V**, at least 8 A, gate rated ±20 V, below about 30 mΩ at -4.5 V (for example AO4407A is **not** enough here: it is only 30 V).
- **Q2 (AO4407A):** any P-channel SOIC-8 MOSFET, at least -20 V, at least 8 A, below about 25 mΩ at **-4.5 V** gate drive (it only gets 5 V of gate drive). AO4485 also works.
- **U2:** 74HCT2G34GW-Q100H (C547575) works the same: it is also a 5 V HCT dual buffer, with the same legs and size.
- **Q4-Q9 (SI2308A):** use another **60 V** N-channel MOSFET in SOT-23 with pin 1 = Gate, 2 = Source, 3 = Drain and at most about 0.15 ohm at 4.5 V gate drive (for example IRLML0060). **Do not go back to a 30 V part such as AO3400A**: that would remove the safety margin on 24 V.
- **F3-F10 (self-resetting fuses):** any 1812-size PTC rated **at least 33 V**, with 1.5 A hold current for F3-F8 and 2 A hold current for F9-F10.
- **D21 (SMCJ30A):** any SMCJ30A (stand-off 30 V, SMC size) from another maker.

## When the boards arrive

1. Before anything else, check with a meter that the power inputs are not shorted ([assembly.md](assembly.md#before-you-power-it-on-the-first-time)).
2. Solder the RP2350-Zero socket strips.
3. Set every jumper, then follow [wiring.md](wiring.md) and [klipper.md](klipper.md).
