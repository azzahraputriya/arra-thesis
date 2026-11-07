# Template

`itbfisika.cls` is the ITB Sarjana Fisika thesis format (Buku TA), ported
from the official template v1.0 (21 Feb 2022): `BUKU_TA_FISIKA_V1.0.zip`
from https://fi.itb.ac.id, sha256
`61bb5debbcf9e426b9408d980faf28038fb2f9d37818db00e9dabbd8710b8036`.
The class header lists what changed from the original and why.
`logo-itb.pdf` is the template's logo.

`make` adds this folder to the LaTeX search path, so `thesis/main.tex` uses
`\documentclass{itbfisika}`.

If fi.itb.ac.id publishes a newer template, compare its `preamble.tex` and
page files against the class and carry the changes over.
