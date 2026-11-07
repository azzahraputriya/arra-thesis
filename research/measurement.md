# Measurement

What we measure, how failure is detected, and how far the numbers can be
trusted.

## Findings

### F3 · Both theses detect liquefaction by eye

- **Keywords:** liquefaction, prior work
- The onset of liquefaction is defined as the moment a 35 g screwdriver
  standing in the sand starts to sway. It is a yes/no visual call, not a
  measurement.
- **Source:** S1 III.3.3 step 5, S2 III.3.3 step 6.

### F4 · Neither thesis measured pore water pressure or saturation

- **Keywords:** pore water pressure, saturation, prior work
- Both list a pore pressure sensor as future work. Saturation is assumed when
  the water level reaches the sand surface. It is never checked.
- **Source:** S1 V.2 item 3, S2 V.2 item 3, S1 and S2 III.3.3.

### F5 · Vs was measured before and after shaking, not during

- **Keywords:** Vs, prior work
- In the undrained tests, S1 measures Vs right after liquefaction ("sesaat
  setelah likuefaksi") and S2 measures it before shaking. Only S1's drained
  test (0.5 Hz, 3 hours) takes Vs readings during shaking, every 15–30
  minutes.
- **Source:** S1 III.3.3, S2 III.3.3.

### F7 · Results reported without repeats or error bars

- **Keywords:** Vs, repeatability, relative density, prior work
- S1: Vs 276.9–339.15 m/s for saturated densities 1743–1898 kg/m³.
  S2: Vs 145.83–152.17 m/s (sieve #24) and 145.83–148.94 m/s (sieve #30).
  Each value comes from a single run. S2's two ranges overlap, so the
  grain-size effect may be within noise. S1's relative density treats the
  loosest and densest of its own 10 samples as 0% and 100%, instead of
  using standard minimum and maximum density tests.
- **Source:** S1 Table IV.1 and V.1, S2 V.1.

## Proposals

### P1 · Track Vs during shaking

- **Keywords:** Vs, stiffness, cyclic softening, cycles
- Since G = ρVs², the ratio (Vs/Vs₀)² shows how much stiffness the clay has
  lost after each block of cycles. This replaces the screwdriver (F3, F5).

### P4 · Repeat each test

- **Keywords:** repeatability
- Run each condition at least 3 times and report error bars (F7).
