# Writing

How the thesis text is written: spelling, numbers, italics and style. The
`style` check enforces these decisions on every PR.

## Decisions

### D3 · Use a comma as the decimal separator

- **Date:** 2026-11-07 · **Status:** decided
- **Keywords:** decimal separator
- **What:** Write decimals with a comma (`0,5 Hz`) and thousands with a
  point (`2.895 bangunan`), in text and in math.
- **Why:** This is the Indonesian convention. **Unverified:** the exact rule
  in EYD V (Badan Bahasa) is still to be cited. Both earlier theses mixed
  commas and points (S2 writes "1,76 Hz" in its text but "1.5631" in its
  conclusion).
- **Considered:** A decimal point, as in English. Rejected: the body is in
  Bahasa Indonesia.
- **Revisit if:** ITB's thesis guide requires otherwise.

### D4 · Spell every word as KBBI's standard (baku) form

- **Date:** 2026-11-07 · **Status:** decided
- **Keywords:** KBBI
- **What:** Every Indonesian word must be in KBBI in its standard form. The
  `style` check looks each new word up in KBBI daring and keeps the answer
  in a committed cache. Words KBBI marks as non-standard fail, with the
  standard form given. Words KBBI doesn't know fail unless they are in
  italics (D5) or on the allowed list.
- **Why:** Both earlier theses have non-standard or misspelled words that
  KBBI flags (F9).
- **Considered:** An offline spell checker (hunspell-id). Rejected: it accepts
  both *likuefaksi* and *likuifaksi*, so it can't enforce the standard form.

### D5 · Put foreign terms in italics

- **Date:** 2026-11-07 · **Status:** decided
- **Keywords:** italics, KBBI
- **What:** Foreign terms with no standard Indonesian form go in
  `\textit{...}`, e.g. `\textit{shear wave}`, `\textit{sonic viewer}`.
- **Why:** This is the Indonesian convention for foreign terms. It also lets
  the KBBI check (D4) tell a foreign term apart from a typo: anything in
  italics is skipped, anything else must be in KBBI.

### D6 · Warn on filler phrases, don't fail

- **Date:** 2026-11-07 · **Status:** decided
- **Keywords:** filler phrase
- **What:** The `style` check flags phrases like "Hal ini menunjukkan bahwa"
  as warnings. The check still passes.
- **Why:** Whether a phrase is filler depends on the sentence, so it's a
  judgment call, not a rule.

## Findings

### F9 · KBBI on words from the earlier theses

- **Keywords:** KBBI, prior work
- Looked up on KBBI daring (kbbi.kemendikdasmen.go.id/entri/…) on
  2026-11-07:
  - *likuefaksi* is standard, and its entry lists *likuifaksi* as
    non-standard (bentuk tidak baku). S2 mixes both: *Likuefaksi* in its
    title, *likuifaksi* in its abstract.
  - *frekuensi* is standard (*frekwensi* is not). *analisis* is standard
    (*analisa* is not).
  - *berprilaku* and *dimana* are not in KBBI. The standard forms are
    *berperilaku* and *di mana*. S1 writes *berprilaku* (I.1).
  - *sitasi*, *kejenuhan*, *pelunakan*, *siklik*, *densitas*, *saturasi*,
    *drainase* and *konsolidasi* are all in KBBI.
- 30 lookups at one per second from an anonymous session hit no limit.
- **Source:** KBBI daring, S1 I.1, S2 abstract.

### F10 · Decimal commas in math need the icomma package

- **Keywords:** decimal separator
- Without it, LaTeX prints `$v = 1,5$` as "1, 5". With `\usepackage{icomma}`
  it prints "1,5", while `$(a, b)$` keeps its space. Tested with tectonic on
  2026-11-07. The class doesn't load icomma yet.
