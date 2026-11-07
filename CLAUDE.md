# arra-thesis

Azzahra Putriya Ahmad's (Arra's) thesis. Research and writing run through the
`academic-research-skills` plugin (ARS), enabled in `.claude/settings.json`.

## How changes land

- Never commit to `main`. Every change goes through a PR. GitHub can't enforce
  this on a free private repo, so it's on us.
- One PR = one piece of thesis progress: a finding, a chapter plan, a
  literature pass, a draft section. Don't mix unrelated progress in one PR.
- PRs merge by squash only (the repo allows nothing else). The PR title becomes
  the commit title on `main`, so `git log` reads as a list of progress.
- Titles use conventional commits with the thesis area as scope, e.g.
  `feat(lit-review): map studies on X`, `docs(ch2): plan method chapter`,
  `chore: update ARS plugin`.
- PR body: what was found or decided, in plain words, then what changed.
