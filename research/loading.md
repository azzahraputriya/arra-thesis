# Loading

How the sample is shaken: frequency, amplitude, acceleration, number of
cycles, and whether water can drain.

## Findings

### F1 · S2's accelerations are computed from frequency, not measured

- **Keywords:** acceleration, amplitude, prior work
- S2's values match a = A(2πf)² with A = 0.05 m (the table's 5 cm amplitude)
  exactly: 1.5631 Hz → 4.82 m/s², 1.7585 Hz → 6.10 m/s²,
  1.9539 Hz → 7.54 m/s². So S2's conclusion that "higher frequency gives
  higher acceleration" holds by construction and says nothing about the soil.
- **Source:** S2 Tables IV.3 and IV.4.

### F2 · S1's accelerations are also computed from frequency

- **Keywords:** acceleration, amplitude, prior work
- 9 of 10 rows match a = A(2πf)² with A = 0.01 m (for example,
  3.0952 Hz → 3.7822 m/s²). Rows with the same frequency give the same
  acceleration to four digits. The first row (1.19048 Hz → 1.4323 m/s²) does
  not fit. Both theses mention an accelerometer, but the reported values
  behave like calculations. With amplitude fixed, frequency and acceleration
  cannot be separated in that rig.
- **Source:** S1 Table IV.3.

### F8 · S1 used shaking frequency to switch drainage on and off

- **Keywords:** drainage, prior work
- At 0.5 Hz the sand drained between cycles and compacted instead of
  liquefying. S1 puts this down to the small scale of the box.
  **Unverified:** clay lets water through thousands of times more slowly
  than sand, so it may stay undrained at every frequency the table can reach.
  If so, this switch does not carry over to clay.
- **Source:** S1 IV.2.

## Proposals

### P6 · Vary amplitude and frequency independently

- **Keywords:** amplitude, acceleration, cycles, shaker table
- Record the real accelerometer signal and count cycles, so acceleration is
  measured rather than computed (F1, F2).
