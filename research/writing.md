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

- **Date:** 2026-11-07 · **Status:** decided, amended by D7
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

### D7 · Words not looked up in KBBI yet are warnings for now

- **Date:** 2026-11-07 · **Status:** provisional, until Q7 is resolved
- **Keywords:** KBBI
- **What:** Amends D4. A word that is not in the KBBI cache yet is a
  warning, not an error. Words KBBI marks as non-standard or doesn't know
  still fail. The final defense PDF must pass `make style STRICT=1`, which
  turns the warnings back into errors.
- **Why:** KBBI daring allows only about 100 lookups a day without an
  account (F11), so a new chapter can take days to look up. Registering an
  account is stuck (Q7).
- **Considered:** Using an offline copy or kbbi.web.id instead. Rejected:
  both hold KBBI edition III from 2008 (F12).
- **Revisit if:** Arra gets a KBBI account. Then add login to `make kbbi`
  and make these words errors again.

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

### F11 · KBBI daring's daily limit without an account

- **Keywords:** KBBI
- After about 100 lookups in one day from an anonymous session, KBBI
  redirects every lookup to `/Beranda/BatasSehari`: "Pencarian Anda telah
  mencapai batas maksimum yang diberikan bagi pengguna tidak terdaftar
  dalam sehari." Lookups work again the next day. A registered account
  lifts or raises the limit; by how much isn't known yet.
- **Source:** kbbi.kemendikdasmen.go.id, tested 2026-11-07.

### F12 · The offline KBBI and kbbi.web.id hold edition III

- **Keywords:** KBBI
- `kbbi-offline` (code.google.com/archive/p/kbbi-offline) says in its own
  About box that its data comes from "KBBI Daring (edisi III)" and that the
  data is Pusat Bahasa's copyright. The data is in a compressed Windows
  format.
- kbbi.web.id says its main database "masih mengacu pada KBBI Daring Edisi
  III", and adds unofficial entries marked "Definisi Eksternal".
- Neither has *likuefaksi*. kbbi.web.id returns "tidak ditemukan" for
  *analisa*, *frekwensi* and *berperilaku* alike, so it can't tell a
  non-standard form from a typo or from a derived word.
- **Source:** both sites, checked 2026-11-07.

## Open questions

### Q7 · KBBI account for Arra

- **Keywords:** KBBI
- Registration at kbbi.kemendikdasmen.go.id/Account/Register never sent the
  confirmation email. To try: spam folders, logging in anyway, "Lupa kata
  sandi", another email address, or writing to adminkbbi@kemdikbud.go.id.
