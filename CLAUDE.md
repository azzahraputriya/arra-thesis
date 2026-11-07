# arra-thesis

Azzahra Putriya Ahmad's (Arra's) thesis. Research and writing run through the
`academic-research-skills` plugin (ARS), enabled in `.claude/settings.json`.

## Writing in LaTeX

The thesis output is LaTeX, built with `make` (tectonic) into `build/main.pdf`.
The body is in Bahasa Indonesia, with an English abstract next to the Indonesian one.
When an ARS skill produces thesis text, follow these rules over its defaults:

- `template/itbfisika.cls` is the ITB Sarjana Fisika format. Never edit it
  while writing, and never generate your own preamble or document class.
  Change it only in a PR about the format itself.
- `thesis/main.tex` holds the identity (`\judul`, `\penulis`, `\pembimbing`,
  ...) and the page order. Fixed pages are commands (`\sampul`,
  `\pengesahan`, `\daftarisi`, ...). Don't rewrite them by hand.
- Front matter lives in `thesis/front/`, inside the class's environments:
  `abstrak`, `abstract` (English), `katapengantar`, `daftarnotasi`,
  `daftarsingkatan`.
- Each chapter is one file, `thesis/chapters/NN-name.tex`, starting at
  `\chapter{UPPERCASE TITLE}`, e.g. `\chapter{TINJAUAN PUSTAKA}`. Chapter
  files hold body text only, with no preamble. Add each new chapter to
  `thesis/main.tex` with `\input`, not `\include` (tectonic's BibTeX run
  fails on the extra files `\include` makes).
- References go in `thesis/references.bib` with `AuthorYear` keys. Cite with
  `\cite{key}` or `\cite{a,b}`, which prints [Author, Year]. `\citet` /
  `\citep` don't exist in this class. The list is APA-like and only shows
  works that are cited. If a template rule conflicts with an ARS default,
  the template wins.
- Figures go in `thesis/figures/` as PDF, PNG or JPG (not EPS: tectonic
  can't read it). Use `\includegraphics{name}`, no folder prefix.
- Run `make` after writing and fix any LaTeX errors before opening the PR.

## How changes land

- Never commit to `main`. Every change goes through a PR. A GitHub ruleset
  ("main via PR") blocks direct pushes, force pushes, and deleting `main`.
- One PR = one piece of thesis progress: a finding, a chapter plan, a
  literature pass, a draft section. Don't mix unrelated progress in one PR.
- PRs merge by squash only (the repo allows nothing else). The PR title becomes
  the commit title on `main`, so `git log` reads as a list of progress.
- Titles use conventional commits with the thesis area as scope, e.g.
  `feat(lit-review): map studies on X`, `docs(ch2): plan method chapter`,
  `chore: update ARS plugin`.
- PR body: what was found or decided, in plain words, then what changed.
