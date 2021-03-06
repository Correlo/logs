## run 1

uninsulated oven prototype, no compensation.

soldered a 20k in parallel with the 10k below the thermistor, to ajust the set-point to a higher temperature.

measuring the difference between the inverting and non-inverting op amp inputs, using a Keithley 2015.


## run 2

removing 20k parallel resistor.

measuring the difference between the inverting and non-inverting op amp inputs, using a Keithley 2015.


## run 3

New setup: I discovered I had mistakenly thought that pin 1 was the base of the current limiting transistor,
when in fact this is pin 2.  This is why my circuit wasn't behaving.

I have constructed another Hammond 1590B case, with foam insulation, which simply has an MJE3055 and two
10k thermistors epoxied to the bottom (using Arctic Silver thermal epoxy), with all of the control
circuitry off-board on a breadboard.

I am now logging the ambient temperature (using an Si7021) and the temperature of one of the affixed thermistors (using the "TEMP" function of a Keithley 2015).

Initial log will simply be logging the off-state behavior of the device.


## run 4

turned on the power to the LM723 circuit.

hmm, it turned on and just railed to the current-limited output (140mA) the entire time, shooting way past the set-point.


## run 6

attempted to reverse which position the thermistor was in (lower half of non-inverting divider, rather than upper half of inverting divider), but ran into the same problems (the circuit keeps heating past the set-point).


## run 7

created a similar circuit based on an OP07 op amp.

unfortunately I neglected to realize that the opamp output can't swing to the negative rail, which means it
can't shut off the MJE3055 entirely.  it looks like the closest it can get is about 1.4V.


## run 8, 9

used a 3.3V zener (reverse biased) on the output of the opamp, which allows it to turn the MJE3055 fully off.

Parts used:
- US Sensor 103JG1J 5% 10k thermistor
- Yageo MFP 0.1% 10k resistors (25ppm/C)

started logging with no compensation.  this produced a sawtooth between 23.9C and 23.6C.  Bit strange that this
set-point is so far away from 25C.

compensation networks attempted:
- A: no compensation
- B: 0.1uF ceramic + 1M (from inverting input to after the output zener)
- C: 0.1uF ceramic + 10M
- D: 1uF ceramic + 10M
- E: 2uF ceramic + 10M
- F: 2uF ceramic + 10M (attached to top of current shunt)
  - this was less effective than from inverting input to after output zener.
- G: back-to-back 10uF electrolytics + 10M (from inverting input to after the output zener)
  - caps are positioned negative to negative.
- H: back-to-back 47uF electrolytics + 10M
- I: back-to-back 47uF electrolytics + 10M (from inverting input to before the output zener)
- J: back-to-back 47uF electrolytics + 10M (from inverting input to before the output zener)
  - reversed the polarity of the caps (positive to positive)
- K: back-to-back 47uF electrolytics + 20M (from inverting input to before the output zener)
- L: swapped around the bridge (thermistor now on bottom half of non-inverting input)
  - forgot to swap the compensation network, which nulled its effect.
- M: corrected the compensation network
- N: changed out the 10k/10k fixed divider for a 100k/100k divider
  - yay the oscillations stopped!
- O: 1uF ceramic + 20M
  - this still worked!
- P: 1uF ceramic + 10M
  - this still worked as well!
- Q: 0.1uF ceramic + 10M
  - this caused the oscillations to return (though smaller than before)

looks like the 100k/100k divider with 1uF+10M compensation is the way to go.


## run 10

pointed a fan at both thermistors and alternated measuring either one.

The thermistors should be at the same temperature, so this will reveal their offset.


## run 11

placed a 120k in parallel with the 10k resistor to adjust the temperature set-point closer to 25C.

it looks like this is still a bit under-damped.

## run 12

starting from cold.  trying 2uF+10M this time.

## run 13

starting from cold.  trying 4uF+10M this time.


## run 14

revisiting the LM723 circuit with corrections.

- 10k/10k divider, 100k + 47uF-47uF compensation
- 100k/100k divider, 100k + 47uF-47uF compensation
  - stable
- 100k/100k divider, 100k + 10uF-10uF compensation
  - unstable
- 100k/100k divider, 1M + 10uF-10uF compensation
  - eventually stable, very ringy
- 100k/100k divider, 10M + 10uF-10uF compensation
  - unstable
- 1M/1M divider, 10M + 10uF-10uF compensation
  - unstable (stuck on heat?)
- 1M/1M divider, 1M + 10uF-10uF compensation
  - too slow (huge overshoot)
- 1M/1M divider, 1M + 1uF compensation
  - oh, now I see, the compensation network is affecting the set-point (pulling it up to ~27C)
- 100k/100k divider, 1M + 9uF ceramics compensation
  - 4.7R current shunt (140mA limit), compensation connected to shunt
  - this is very well damped


## run 15

continuation of run 14

- 100k/100k divider, 1M + 9uF ceramics compensation
  - 2.2R + 2.2R current shunt, current limit in middle tap (300mA limit), compensation connected to top of shunt
  - this is very well damped


## run 16

continuation of run 15

- 100k/100k divider, 1M + 1uF ceramic compensation
  - 2.2R + 2.2R current shunt, current limit in middle tap (300mA limit), compensation connected to top of shunt


## run 17, 18

start-up and overnight run of the lm723 oven.

## run 19

thermistor in a large styrofoam drinking cup filled with water.

## run 20

thermistor in a styrofoam beer cooler filled with water.

