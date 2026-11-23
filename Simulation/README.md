# Simulation

The SPICE decks behind the electrical numbers in [Build it](../Production). Each `.cir` file is complete on its own:
`ngspice -b <file>` runs it and its `.control` block prints the results. [results.txt](./results.txt) is that output,
from the ngspice that ships with KiCad 10.0.8.

**None of this is a measurement.** The board has not been built. The models are fitted to typical datasheet curves,
the loads are ideal, and the thermal model is a rough guess. Use the numbers to decide what to measure first.

## Results (v1.3)

|Deck|Question|Result|
|---|---|---|
|[power_two_20_led_rgb_strips.cir](./power_two_20_led_rgb_strips.cir)|Voltage at the connectors with five 0.6 A fans on 24 V and two 1.2 A strips on 5 V|fans 23.73 - 23.76 V, LED ports 4.83 V, 1.18 W lost in the board|
|[power_two_20_led_rgbw_strips.cir](./power_two_20_led_rgbw_strips.cir)|The same with 1.6 A per strip|LED ports 4.77 V, 1.50 W lost|
|[power_every_port_at_its_limit.cir](./power_every_port_at_its_limit.cir)|Stress case: 4.8 A on VIN, 4.2 A on 5 V|5 V LED port 4.66 V, 5 V fans 4.75 V, 3.11 W lost. Not an operating point: it is above the 3.75 A a 5 A fuse should carry continuously|
|[thermal_estimate.cir](./thermal_estimate.cir)|How warm, roughly?|first case: fuses 7 - 8 K, board 2 - 6 K above the air around it; stress case: fuses 22 - 24 K, board 6 - 16 K|
|[fan_switching.cir](./fan_switching.cir)|Drain voltage and current when a 2/3-mode channel switches a 0.6 A fan|drain peaks at 24.4 V on a 24.0 V supply and 26.8 V on 26.4 V (the MOSFET is rated 30 V). Switching on recharges the fan's own capacitor through the MOSFET: 22 A peak, above 5 A for 2 µs with the 1 µF fan assumed here|
|[fan_pwm_line.cir](./fan_pwm_line.cir)|PWM pin of a 4-wire fan at 25 kHz|swings 0 - 5 V with 0.24 V of overshoot, rises in 1.0 µs, falls in 5 ns|
|[tach_input.cir](./tach_input.cir)|What the RP2350 sees when a fan pulls its tach wire low, and when the wire sits at the fan voltage|0.47 V for a fan that pulls down to 0.2 V, 0.65 V for one that pulls to 0.4 V, the same with a 2N7002 at its maximum threshold (the diode of v1.2: 0.57 - 0.72 V and 0.77 - 0.91 V). The RP2350 guarantees a low below 0.8 V. With 26.4 V on the wire the pin stays at 3.30 - 3.31 V. The pin follows a fan's edge in 40 µs (rising) and 7 µs (falling)|
|[tach_pwm_edges.cir](./tach_pwm_edges.cir)|What the pin sees while a 2/3-mode fan with a tach wire is switched on and off|table below|
|[led_data.cir](./led_data.cir)|How much of a data pulse reaches the first pixel|table below|
|[led_low_level.cir](./led_low_level.cir)|LED data low level with parts at their limits|0.42 V typical; 0.50 V with a 2N7002 at its maximum threshold; 1.09 V with the weakest pad the RP2350 datasheet allows; 2.9 V, which is not a low, if both limits meet|
|[usb_only_leakage.cir](./usb_only_leakage.cir)|Can the USB-powered module feed the board's 5 V rail?|only through an LED data pin that is held high: 5 mA per pin at most, and the unpowered rail floats to 2.8 V at most. Klipper keeps those pins low between updates|

### LED data

Time the pixel's data input spends above 3.5 V (0.7 x 5 V), for a 200 ns and a 250 ns pulse (a Klipper "0" bit lies in
that range) and an 833 ns pulse (a "1" bit). The load is the cable plus the pixel input as one capacitor; three-wire
LED lead is roughly 100 - 150 pF per metre.

|Load|v1.2, R1 = 100 Ω: 200 / 250 / 833 ns pulse|v1.1, R1 = 330 Ω|
|---|---|---|
|50 pF|164 / 214 / 797 ns|150 / 201 / 784 ns|
|100 pF|140 / 190 / 774 ns|109 / 161 / 747 ns|
|150 pF|114 / 166 / 751 ns|63 / 118 / 710 ns|
|200 pF|87 / 140 / 728 ns|12 / 71 / 673 ns|

This is why v1.2 changed R1 and R2 from 330 Ω to 100 Ω: at 150 pF a short pulse keeps about 50 ns more. The level
shifter is still a pull-up, not a driver, so the rule stays the same: keep the data wire short.

Q6 and Q7 stay 2N7002. An AO3400A would guarantee the low level at 3.3 V gate drive, but its output capacitance
(roughly 300 pF at these voltages, from the capacitance graph in its datasheet) sits on the 470 Ω pull-up and slows
the rising edge more than a metre of cable does.

### Tach input

In 2/3 mode the board switches the fan's ground. The fan's tach output hangs on that ground, so every switching
edge drags the tach wire along: below ground when a fan with an input capacitor is switched on (its ground dips to
about -4 V for 2 µs while the capacitor recharges), and up to 24 V within nanoseconds when an inductive fan is
switched off. Each cell gives the lowest and highest voltage at the RP2350 pin and the largest current pulled out
of the pin through its clamp diode to ground. The pin is rated for -0.5 V to 5.5 V.

|Fan, tach output|v1.0 - v1.2: diode in series|2N7002 alone|v1.3: 4.7 kΩ + 2N7002 + 1 nF|
|---|---|---|---|
|1 µF fan, open-drain output|-1.25 … 3.41 V, 88 mA|-1.39 … 3.97 V, 114 mA|0.39 … 3.30 V, none|
|1 µF fan, NPN output|-0.85 … 3.39 V, 18 mA|-0.86 … 3.80 V, 18 mA|0.40 … 3.30 V, none|
|inductive fan, open-drain output|-0.72 … 6.61 V, 2.4 mA|0.00 … 7.95 V, 0.2 mA|0.35 … 3.30 V, none|
|inductive fan, NPN output|-0.68 … 3.78 V, 0.7 mA|0.01 … 5.81 V, 0.1 mA|0.36 … 3.30 V, none|

This is why v1.3 has R14 - R18 and C8 - C12. The resistor limits what the fan can pull out of the pin, and the
capacitor takes up the charge that a fast edge pushes through the transistor. The price is a low level that is about
0.25 V higher than with the transistor alone, still below the diode of v1.2. The fans in this deck are assumptions;
real fans differ, and the RPM reading is still only valid at 100% in 2/3 mode.

## Assumptions

- **Copper:** every `R<net>_<n>` in the power decks is one track or zone segment read from the board file, 35 µm
  copper at 20 °C. The copper that carries current is the same in v1.1, v1.2 and v1.3.
- **Contacts and fuses:** screw terminal 1.5 mΩ, blade fuse 19 - 26 mΩ, fuse holder 4 mΩ, jumper shunt 15 mΩ,
  JST-XH contact 10 mΩ. Typical values, not measured ones.
- **Loads:** ideal current sinks. A real strip or fan draws less when its voltage sags.
- **RP2350 pin:** 3.3 V behind 40 Ω, typical for the 4 mA drive setting Klipper uses; 125 Ω is the weakest the
  datasheet allows (0.5 V at 4 mA). Tach input: 50 kΩ pull-up (the strong end of 50 - 80 kΩ), 5 pF, a clamp diode
  to ground and none to 3.3 V.
- **MOSFETs and diodes:** behavioural models fitted to the typical curves of the JLCPCB parts
  (2N7002 C8545, AO3400A C20917, B5819W C8598; the 1N4148WS of v1.2 only for comparison). The fit points are in
  the deck comments.
- **Fans in the tach decks:** assumed, not taken from a data sheet: a tach output that pulls down to 0.2 V or 0.4 V;
  for the switching edges a 40 Ω fan with a 1 µF input capacitor and 0.25 µH per supply wire, or 40 Ω in series
  with 1 mH, and a tach output that can sink about 15 mA (NPN) or has 20 Ω (open drain).
- **Thermal:** a five-node model for still air. No thermal resistance in it has been measured, and the split of the
  board loss over three zones is assumed.
