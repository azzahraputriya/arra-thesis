# `make` builds build/main.pdf. Tectonic fetches missing LaTeX packages on its
# own, so the only thing to install is tectonic itself.
# shortcut: BibTeX only. If the template uses biblatex+biber, tectonic calls a
# `biber` from PATH, which must match the biblatex version in tectonic's bundle.
pdf:
	mkdir -p build
	tectonic -Z search-path=template --outdir build thesis/main.tex

clean:
	rm -rf build

.PHONY: pdf clean
