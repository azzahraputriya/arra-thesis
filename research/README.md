# Research trail

Why the thesis is shaped the way it is. Read this folder to answer "why did we
choose X?".

Entries are grouped by topic, one file per topic. The topics and the
keywords are defined in [glossary.md](glossary.md). Only terms in the glossary
may be used as topics or keywords.

## Kinds of entry

| ID | Kind | Meaning |
|---|---|---|
| `C` | Constraint | A limit we work within (time, equipment) |
| `D` | Decision | A choice we made |
| `F` | Finding | A fact we checked, with its source |
| `P` | Proposal | An idea not yet chosen |
| `Q` | Open question | Something we still need to answer |
| `S` | Source | A document that entries cite |

IDs are numbered across the whole folder, not per file, so `D2` means one
entry wherever it lives. To get the next number, find the highest one in use
(swap `D` for the kind you need):
`grep -rhoE '^### D[0-9]+' research --exclude=README.md | sort -V | tail -1`.

## Rules

- Put each entry in the file for its main topic. List any other topics it
  touches under **Keywords**.
- Never rewrite or delete an old entry. If a decision changes, add a new one
  that says "replaces D2", and set the old one's status to `replaced by Dn`.
  When a question is answered, add the answer as a decision or finding and
  mark the question `answered by Dn`.
- Every claim gets a source: a finding, an `S` source, a reference in
  `thesis/references.bib`, or the label **unverified** until someone checks it.
- To add a topic or keyword, add it to the glossary in the same PR. The PR
  review is where it gets agreed.
- The git history is the changelog. PRs are squash-merged, and the squash
  commit carries the PR body, so `git log -- research/` lists every change
  to this folder with its summary. Every PR that touches this folder puts
  a line in its body that names each ID it touched, one by one (no ranges
  like F1–F8, so a search for one ID finds it):

  ```
  Trail: added D3, F9 · changed D2 → decided · answered Q3
  ```

  `git log --grep 'D2'` then shows every PR that touched D2.

## Entry format

```markdown
### D3 · Short title

- **Date:** 2026-11-07 · **Status:** decided | provisional | replaced by D4
- **Keywords:** cyclic softening, plasticity index
- **What:** the choice.
- **Why:** the reasons, each with a source.
- **Considered:** the other options and why we dropped them.
- **Revisit if:** what would make us change it.
```

Findings, proposals and questions use the same heading. They need only
**Keywords** and a short body. Findings also give the exact table or page
they come from.
