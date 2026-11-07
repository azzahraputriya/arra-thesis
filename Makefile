# `make` checks the writing rules, then builds build/main.pdf. The check runs
# first so a change that skipped the PR still can't compile while it breaks a
# rule. Tectonic fetches missing LaTeX packages on its own, so the only things
# to install are tectonic and Python 3.
# shortcut: BibTeX only. If the template uses biblatex+biber, tectonic calls a
# `biber` from PATH, which must match the biblatex version in tectonic's bundle.
pdf:
	python3 scripts/lint.py
	mkdir -p build
	tectonic -Z search-path=template --outdir build thesis/main.tex

# Checks the CLAUDE.md writing rules, then the checker's own tests.
lint:
	python3 scripts/lint.py
	python3 -m unittest discover -s scripts -q

# Checks the writing style (research/writing.md) offline, from the KBBI cache.
# `make style STRICT=1` also fails on words not looked up yet; the final PDF
# must pass it (D7).
style:
	python3 scripts/style.py $(if $(filter 1,$(STRICT)),--strict)

# Looks up new words on KBBI daring (one per second), then checks the style.
# Commit the updated style/kbbi.tsv with the text that needed it.
kbbi:
	python3 scripts/style.py --update

clean:
	rm -rf build

.PHONY: pdf lint style kbbi clean
