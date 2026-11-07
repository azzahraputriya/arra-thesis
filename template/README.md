# Template

Put the thesis template files here: `.cls`, `.sty`, `.bst`, logos. Keep
them unchanged so a newer version can be dropped in over them.

`make` adds this folder to the LaTeX search path, so `thesis/main.tex` can
use `\documentclass{<name>}` with no folder in front of the name.

After adding the files, update the preamble and title page in
`thesis/main.tex` to match the template's own example.
