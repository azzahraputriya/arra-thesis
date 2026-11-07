# arra-thesis

Azzahra Putriya Ahmad (10223085)

## Setup

This repo uses [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) (ARS) through Claude Code.

1. Open this folder in Claude Code and trust it.
2. Accept the prompt to install the `academic-research-skills` plugin. It is already listed in `.claude/settings.json`.
3. Turn on auto-update for it in `/plugin`. ARS ships updates every week or two.

Check it works: run `/ars-plan` and describe the thesis.

## Building the PDF

1. Install [tectonic](https://tectonic-typesetting.github.io/en-US/install.html).
2. Run `make`. The PDF is written to `build/main.pdf`.

| Path | What goes there |
|---|---|
| `template/` | ITB Sarjana Fisika thesis class and logo |
| `thesis/main.tex` | Title, name, supervisors, and the order of pages |
| `thesis/front/` | Abstrak, abstract, kata pengantar |
| `thesis/chapters/` | One `.tex` file per chapter |
| `thesis/references.bib` | All references |
| `thesis/figures/` | Images |
| `research/` | Why we chose what we chose, by topic. Start at `research/README.md` |

## Where to start

| I want to... | Say or run |
|---|---|
| Shape a vague idea into a research question | Describe the idea, ask to be guided |
| Plan chapters | `/ars-plan` |
| Get a literature review | `/ars-lit-review "topic"` |
| Get a draft reviewed | "Review this paper", then attach it |
| Go from question to finished paper | "I want a complete research paper about ..." |

ARS stops at every stage for your confirmation. You stay the author.

## How changes land

Every change goes through a PR, one per piece of progress (a finding, a chapter plan, a draft section). PRs are squash-merged, so each one becomes a single commit on `main`. Details are in `CLAUDE.md`.
