#!/usr/bin/env python3
"""Check the thesis sources against the rules in CLAUDE.md.

Usage: python3 scripts/lint.py [thesis_dir]   (default: thesis)
Prints one `path:line: message` per problem and exits 1 if there are any.

Only rules CLAUDE.md already sets live here. Style rules (decimal comma,
term spelling, italics) wait until they are agreed in research/.
"""
import os
import re
import sys
from pathlib import Path

CHAPTER_NAME = re.compile(r"\d\d-[a-z0-9-]+\.tex")
APPENDIX_NAME = re.compile(r"lampiran[a-z0-9-]*\.tex")
BIB_KEY = re.compile(r"[A-Z][A-Za-z]*\d{4}[a-z]?")
BIB_ENTRY = re.compile(r"@(\w+)\s*[{(]\s*([^,\s]+)\s*,")
PREAMBLE = re.compile(r"\\(documentclass|usepackage|RequirePackage)\b|\\(begin|end)\{document\}")
# \cite{...}, \cite[p. 5]{...}, \nocite{...} and any other \cite... command.
CITE = re.compile(r"\\((?:no)?cite[a-zA-Z]*)\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}")
GRAPHICS = re.compile(r"\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}")
CHAPTER = re.compile(r"\\chapter\s*\*?\s*(?:\[[^\]]*\])?\s*\{")
FIGURE_EXTS = (".pdf", ".png", ".jpg", ".jpeg")


def strip_comment(line):
    """Drop a LaTeX comment. A % is escaped only after an odd run of backslashes."""
    i = 0
    while i < len(line):
        if line[i] == "\\":
            i += 2  # skip the escaped character, so \\% still starts a comment
        elif line[i] == "%":
            return line[:i]
        else:
            i += 1
    return line


def tex_text(path):
    """The file's text with comments removed; line numbers are kept."""
    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(strip_comment(l) for l in lines)


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def braced(text, pos):
    """The contents of the {...} group opening just before pos, nested braces included."""
    depth, i = 1, pos
    while i < len(text) and depth:
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        i += 1
    return text[pos:i - 1]


def bib_keys(bib, problems):
    keys = {}
    if not bib.exists():
        return keys
    text = bib.read_text(encoding="utf-8")
    for m in BIB_ENTRY.finditer(text):
        if m.group(1).lower() in ("comment", "string", "preamble"):
            continue
        key, n = m.group(2), line_of(text, m.start())
        if key in keys:
            problems.append((bib, n, f"duplicate bib key '{key}' (first on line {keys[key]})"))
        elif not BIB_KEY.fullmatch(key):
            problems.append((bib, n, f"bib key '{key}' is not AuthorYear, e.g. Kramer1996"))
        keys.setdefault(key, n)
    return keys


def check(root):
    root = Path(root)
    problems = []
    keys = bib_keys(root / "references.bib", problems)
    texts = {path: tex_text(path) for path in sorted(root.rglob("*.tex"))}

    inputs = set()
    for path, text in texts.items():
        for m in re.finditer(r"\\input\s*\{([^}]*)\}", text):
            target = m.group(1).strip().removesuffix(".tex")
            inputs.add(target)
            if not (root / (target + ".tex")).exists():
                problems.append((path, line_of(text, m.start()), f"\\input{{{target}}} points to a missing file"))

    chapters = root / "chapters"
    for path in sorted(chapters.glob("*.tex")) if chapters.exists() else []:
        if APPENDIX_NAME.fullmatch(path.name):
            continue
        if not CHAPTER_NAME.fullmatch(path.name):
            problems.append((path, 1, "chapter files are named NN-name.tex, e.g. 02-tinjauan-pustaka.tex"))
            continue
        if f"chapters/{path.stem}" not in inputs:
            problems.append((path, 1, "chapter is not \\input in main.tex"))
        text = texts[path]
        body = text.lstrip()
        n = line_of(text, len(text) - len(body))
        m = CHAPTER.match(body)
        if not m:
            problems.append((path, n, "chapter file must start with \\chapter{TITLE}"))
            continue
        # Only the words count: commands like \textit and inline math may stay lowercase.
        words = re.sub(r"\\[a-zA-Z]+|\$[^$]*\$", "", braced(body, m.end()))
        if words != words.upper():
            problems.append((path, n, "chapter title must be uppercase"))

    for path, text in texts.items():
        where = lambda m: (path, line_of(text, m.start()))
        if path.relative_to(root).parts[0] in ("chapters", "front"):
            problems.extend((*where(m), "no preamble in chapter or front files; the class handles it")
                            for m in PREAMBLE.finditer(text))
        problems.extend((*where(m), "use \\input, not \\include (tectonic's BibTeX run fails on it)")
                        for m in re.finditer(r"\\include\s*\{", text))
        for m in CITE.finditer(text):
            cmd, arg = m.groups()
            if cmd not in ("cite", "nocite"):
                problems.append((*where(m), f"\\{cmd} doesn't exist in this class; use \\cite"))
            for key in (k.strip() for k in arg.split(",")):
                if key == "*":
                    problems.append((*where(m), "no \\nocite{*}: the reference list only shows cited works"))
                elif key and key not in keys:
                    problems.append((*where(m), f"\\cite key '{key}' is not in references.bib"))
        for m in GRAPHICS.finditer(text):
            problems.extend((*where(m), msg) for msg in figure_problems(root / "figures", m.group(1).strip()))

    return problems


def figure_problems(figures, name):
    if "/" in name:
        return [f"\\includegraphics{{{name}}}: drop the folder, use the bare file name"]
    if name.lower().endswith(".eps"):
        return [f"\\includegraphics{{{name}}}: EPS isn't readable by tectonic; use PDF, PNG or JPG"]
    # Compare against the real names so a Mac (case-insensitive disk) gives the same answer as CI.
    present = set(os.listdir(figures)) if figures.is_dir() else set()
    candidates = [name] if name.lower().endswith(FIGURE_EXTS) else [name + e for e in FIGURE_EXTS]
    if not present.intersection(candidates):
        return [f"\\includegraphics{{{name}}}: no PDF, PNG or JPG with that name in thesis/figures/"
                " (extensions must be lowercase)"]
    return []


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "thesis"
    problems = check(root)
    for path, n, msg in problems:
        print(f"{path}:{n}: {msg}")
    print(f"{len(problems)} problem(s)" if problems else "lint: ok")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
