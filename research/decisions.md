# Research trail

Why the thesis is shaped the way it is. Read this to answer "why did we choose X?".

How to use it:

- **Decisions (D)** are choices we made. **Findings (F)** are facts we checked,
  with where they come from. **Proposals (P)** are ideas not yet chosen.
  **Open questions (Q)** are things we still need to answer.
- Add new entries at the bottom of their section with the next number. Never
  rewrite or delete an old entry. If a decision changes, add a new one that
  says "replaces D2", and mark the old one `replaced by Dn`.
- Every claim gets a source: a finding, a reference in `thesis/references.bib`,
  or the label **unverified** until someone checks it.

## Constraints

- **C1 · Timeline.** Proposal defense in January 2027. Final defense about
  4–5 months later (May–June 2027). Clay samples take days to saturate and
  weeks to consolidate, so lab time is the scarce resource.
- **C2 · Equipment.** We assume Arra can use the same rig as S1 and S2 at the
  PAU ITB Geotechnical Lab (see F6). Not yet confirmed with the lab.

## Decisions

### D1 · Use clay (tanah lempung) as the medium

- **Date:** 2026-11-07 · **Status:** decided
- **What:** Test clay, not the sands used before (Ottawa in S1, Garut in S2).
- **Why:** Same supervisor, same lab and rig as S1 and S2, so the thesis
  extends their work instead of starting from zero. Clay is the soil type
  they did not cover.
- **Considered:** Repeating the sand design with another sand. Rejected:
  it would only replicate S1 and S2.

### D2 · Frame the thesis as cyclic softening (pelunakan siklik)

- **Date:** 2026-11-07 · **Status:** provisional, confirm with the supervisor
- **What:** Use "pelunakan siklik" instead of "likuefaksi" in the working
  title and research question.
- **Why:** Plastic clay usually does not liquefy the way sand does. Under
  repeated shaking it loses stiffness and strength step by step, which is
  called cyclic softening. Whether a soil behaves like sand or like clay
  depends mostly on its plasticity index (PI). **Unverified:** from
  Boulanger & Idriss (2006) and Bray & Sancio (2006), still to be checked in
  the literature pass. S2 already cites a related Boulanger & Idriss (2008)
  paper.
- **Considered:** Keeping "likuefaksi" to match S1 and S2. Risky: an examiner
  could object that clay does not liquefy in the classic sense.
- **Revisit if:** the supervisor wants "likuefaksi" in the title, or the
  clay we get has a low PI and behaves like sand.

## Findings

### F1 · S2's accelerations are computed from frequency, not measured

S2 Tables IV.3 and IV.4 match a = A(2πf)² with A = 0.05 m (the table's 5 cm
amplitude) exactly: 1.5631 Hz → 4.82 m/s², 1.7585 Hz → 6.10 m/s²,
1.9539 Hz → 7.54 m/s². So S2's conclusion that "higher frequency gives higher
acceleration" holds by construction and says nothing about the soil.

### F2 · S1's accelerations are also computed from frequency

S1 Table IV.3: 9 of 10 rows match a = A(2πf)² with A = 0.01 m (for example,
3.0952 Hz → 3.7822 m/s²). Rows with the same frequency give the same
acceleration to four digits. The first row (1.19048 Hz → 1.4323 m/s²) does
not fit. Both theses mention an accelerometer, but the reported values behave
like calculations. With amplitude fixed, frequency and acceleration cannot be
separated in that rig.

### F3 · Both theses detect liquefaction by eye

S1 (III.3.3 step 5) and S2 (III.3.3 step 6) define the onset of liquefaction
as the moment a 35 g screwdriver standing in the sand starts to sway. It is
a yes/no visual call, not a measurement.

### F4 · Neither thesis measured pore water pressure or saturation

Both list adding a pore pressure sensor as future work (S1 V.2 item 3,
S2 V.2 item 3). Saturation is assumed when the water level reaches the sand
surface. It is never checked.

### F5 · Vs was measured before and after shaking, not during

In the undrained tests, S1 measures Vs "sesaat setelah likuefaksi" (right
after liquefaction). S2 measures it before shaking. Only S1's drained test
(0.5 Hz, 3 hours) takes Vs readings during shaking, every 15–30 minutes.

### F6 · The rig

Acrylic box, 7 × 20 × 30 cm, 8 mm walls, rated to 2 bar, with a water inlet
at the bottom and an outlet port for pressure. S-wave transmitter and
receiver on opposite sides, driven by a sonic viewer (12 V battery) and read
on an oscilloscope. Shaker table with horizontal circular motion, up to 5 cm
amplitude. Sample mass: 4.5 kg (S1), 3 kg (S2). Source: S1 and S2, III.3.

### F7 · Results reported without repeats or error bars

- S1: Vs 276.9–339.15 m/s for saturated densities 1743–1898 kg/m³.
- S2: Vs 145.83–152.17 m/s (sieve #24) and 145.83–148.94 m/s (sieve #30).

Each value comes from a single run. S2's two ranges overlap, so the
grain-size effect may be within noise. S1's relative density treats the
loosest and densest of its own 10 samples as 0% and 100%, instead of using
standard minimum and maximum density tests.

### F8 · S1 used shaking frequency to switch drainage on and off

At 0.5 Hz the sand drained between cycles and compacted instead of
liquefying (S1 IV.2). S1 attributes this to the small scale of the box.
**Unverified:** clay lets water through thousands of times more slowly than
sand, so it may stay undrained at every frequency the table can reach. If so,
this switch does not carry over to clay.

## Proposals (not decided)

Ideas from the first planning session (2026-11-07). Each one fixes a finding
above. Promote one to a decision when Arra chooses it.

- **P1 · Track Vs during shaking.** Since stiffness G = ρVs², the ratio
  (Vs/Vs₀)² shows how much stiffness the clay has lost after each block of
  cycles. This replaces the screwdriver (F3, F5).
- **P2 · Make plasticity the main variable.** Measure the Atterberg limits,
  then test clay mixed with 0/20/40% sand. S2's Garut sand serves as the 0%
  clay end, so the thesis reads as a sand-to-clay series.
- **P3 · Add a pore pressure sensor** on the existing outlet port (F4, F6).
- **P4 · Repeat each test** (at least 3 times) and report error bars (F7).
- **P5 · Control the clay's state by consolidation**, squeezing it under
  known loads, instead of pouring and tapping it to a density.
- **P6 · Vary amplitude and frequency independently**, record the real
  accelerometer signal, and count cycles (F1, F2).

## Open questions

- **Q1 · Thesis sentence.** In one sentence, what should a reader believe
  after this thesis that they did not before?
- **Q2 · Clay source.** Where does the clay come from, and how much is needed?
- **Q3 · Atterberg limits in-house?** Likely yes (see Q3 notes below).
  Confirm the equipment exists.
- **Q4 · Pore pressure sensor.** Is one available, and does it fit the
  outlet port?
- **Q5 · Supervisor on D2.** Is "pelunakan siklik" acceptable in the title?
- **Q6 · Prior work.** Has a lab study already measured Vs during cyclic
  loading across a sand-to-clay series? To check in the literature pass.

**Q3 notes.** The standard test (ASTM D4318) needs: a Casagrande cup with a
grooving tool for the liquid limit (or a fall cone instead), a glass plate
for rolling 3 mm threads for the plastic limit, a 0.425 mm (#40) sieve, a
drying oven at about 110 °C, and a balance reading to 0.01 g. The oven and
the cup are the parts to check for.

## Sources

- **S1** · Ni Komang Linda Sopianti (10221023), *Pendugaan Potensi
  Likuefaksi Tanah Menggunakan Analisis Gelombang S Melalui Eksperimen
  Laboratorium dengan Medium Pasir Ottawa*, Tugas Akhir draft, Sarjana
  Fisika ITB, 2025. Supervisor: Gunawan Handayani.
- **S2** · Tsabita Kinanti Najwa Priatna (10222073), *Estimasi Potensi
  Likuefaksi Tanah Berbasis Pengukuran Kecepatan Gelombang S pada Eksperimen
  Laboratorium Menggunakan Medium Pasir Garut*, Tugas Akhir draft, Sarjana
  Fisika ITB, 2026. Supervisor: Gunawan Handayani.

The S1 and S2 PDFs are kept out of this repo on purpose. They are
unpublished, and their usage page says copying needs the author's
permission. Section and table numbers above refer to those drafts.
