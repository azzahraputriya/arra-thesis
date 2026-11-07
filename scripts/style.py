#!/usr/bin/env python3
"""Check the thesis text against the agreed writing style (research/writing.md).

Usage:
  python3 scripts/style.py [thesis_dir]           check, offline (CI runs this)
  python3 scripts/style.py --update [thesis_dir]  look up new words on KBBI first
  python3 scripts/style.py --strict [thesis_dir]  also fail on words not looked up yet

Errors (exit 1):
  - a word KBBI marks as non-standard (D4), with the standard form;
  - a word KBBI doesn't know, outside \\textit{} or \\emph{} (D4, D5);
  - a decimal point instead of a comma (D3).
Warnings (exit 0):
  - a word not looked up yet: run `make kbbi`. With --strict this is an
    error; the final PDF must pass --strict (D7);
  - filler phrases from style/filler.txt (D6).

KBBI answers are cached in style/kbbi.tsv, so the check itself never goes
online. Words KBBI lacks but the thesis needs (names, agreed terms) go in
style/allow.txt.
"""
import html
import os
import re
import sys
import time
import http.client
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from lint import braced, line_of, tex_text  # noqa: E402

STYLE_DIR = Path(__file__).resolve().parent.parent / "style"
KBBI_URL = "https://kbbi.kemendikdasmen.go.id/entri/"
KBBI_FOOTER = "Badan Pengembangan dan Pembinaan Bahasa"
CLITICS = ("nya", "lah", "kah", "pun", "ku", "mu")

# Arguments that are not prose: their text is blanked before any check.
NON_PROSE_ARGS = re.compile(
    r"\\(label|ref|eqref|pageref|autoref|cite[a-zA-Z]*|nocite|includegraphics|input|url|href"
    r"|end|hspace\*?|vspace\*?|setlength|addtolength|rule|resizebox|scalebox|parbox"
    r"|makebox|graphicspath|bibliography|bibliographystyle)\s*(?:\[[^\]]*\])*\s*\{"
)
BEGIN = re.compile(r"\\begin\s*\{([^}]*)\}(?:\s*\[[^\]]*\])?")  # \begin{figure}[htbp]
SPEC_ARGS = {"tabular": 1, "tabular*": 2, "tabularx": 2, "array": 1, "longtable": 1, "minipage": 1, "wrapfigure": 2}
ITALIC_ARGS = re.compile(r"\\(textit|emph)\s*\{")
HEADING = re.compile(r"\\(chapter|section|subsection|subsubsection|paragraph|caption)\*?\s*(?:\[[^\]]*\])?\s*\{")
MATH = re.compile(
    r"\\begin\{(equation|align|gather|multline|eqnarray)\*?\}.*?\\end\{\1\*?\}"
    r"|(?<!\\)\$\$.*?\$\$|(?<!\\)\$.*?(?<!\\)\$|(?<!\\)\\\(.*?\\\)|(?<!\\)\\\[.*?\\\]",
    re.S,
)  # (?<!\\) keeps \\[2mm] (a line break) and \$ (a dollar sign) from opening math
ENGLISH = re.compile(r"\\begin\{abstract\}.*?\\end\{abstract\}", re.S)
TEX_UNITS = r"pt|em|ex|cm|mm|in|bp|pc|sp|textwidth|linewidth|columnwidth|textheight|paperwidth|baselineskip"
# A number with one decimal point: 1.5, 0.25. Numbers with several dots
# (II.3.1, 1.2.3, 1.234.567) and TeX lengths (0.5\textwidth, 0.5cm) don't count.
DECIMAL = re.compile(rf"(?<![\w.\\])\d+\.\d+(?![\w]|\.\d|\s*\\(?:{TEX_UNITS})\b)")
# 2.895 is a valid Indonesian thousands separator. A number starting with 0 never is.
# shortcut: 2.718 (meant as a decimal) passes as "2718"; only a reader catches that.
THOUSANDS = re.compile(r"[1-9]\d{0,2}(?:\.\d{3})+")
WORD = re.compile(r"[A-Za-z]+(?:-[A-Za-z]+)*")


def blank(text, start, end):
    """Replace text[start:end] with spaces, keeping newlines so line numbers hold."""
    return text[:start] + re.sub(r"[^\n]", " ", text[start:end]) + text[end:]


def blank_args(text, pattern):
    """Blank each matching command together with its {...} argument."""
    for m in reversed(list(pattern.finditer(text))):
        arg = braced(text, m.end())
        text = blank(text, m.start(), m.end() + len(arg) + 1)
    return text


def blank_begins(text):
    """Blank \\begin{env}[options], plus the column spec of tables and similar."""
    for m in reversed(list(BEGIN.finditer(text))):
        end = m.end()
        for _ in range(SPEC_ARGS.get(m.group(1).strip(), 0)):
            group = re.match(r"\s*\{", text[end:])
            if not group:
                break
            end += group.end() + len(braced(text, end + group.end())) + 1
        text = blank(text, m.start(), end)
    return text


def blank_tex(text):
    """Blank arguments that aren't prose, environment syntax and \\command[options]."""
    text = blank_begins(blank_args(text, NON_PROSE_ARGS))
    for m in reversed(list(re.finditer(r"\\[a-zA-Z@]+\*?\s*\[[^\]]*\]", text))):
        text = blank(text, m.start(), m.end())
    return text


def prepare(text):
    """Return (with_math, prose, headings) for a file's comment-free text.

    with_math keeps math, for the decimal check. prose also drops math,
    italics and command names, leaving only the Indonesian words. headings
    lists the (start, end) spans of heading and caption titles.
    """
    for m in reversed(list(ENGLISH.finditer(text))):
        text = blank(text, m.start(), m.end())
    headings = [(m.end(), m.end() + len(braced(text, m.end()))) for m in HEADING.finditer(text)]
    with_math = blank_tex(text)
    prose = text
    for m in reversed(list(MATH.finditer(prose))):
        prose = blank(prose, m.start(), m.end())
    prose = blank_args(blank_tex(prose), ITALIC_ARGS)
    prose = re.sub(r"\\[a-zA-Z@]+\*?|\\.", lambda m: " " * len(m.group()), prose)
    return with_math, prose, headings


def sentence_start(text, pos):
    """True if the word at pos opens a sentence, a paragraph, or a {group}."""
    i, newlines = pos - 1, 0
    while i >= 0 and text[i].isspace():
        newlines += text[i] == "\n"
        i -= 1
    return i < 0 or text[i] in ".!?:{}" or newlines >= 2


def words(prose, headings=()):
    """(position, lowercase word) for each word to look up.

    In running text, capitalised words inside a sentence are names and
    all-caps words are abbreviations, so both are skipped. In headings and
    captions every word longer than 3 letters is checked, whatever its case.
    shortcut: a name at the start of a sentence or in a heading is checked;
    add it to allow.txt.
    """
    for m in WORD.finditer(prose):
        in_heading = any(a <= m.start() < b for a, b in headings)
        for part in dict.fromkeys(m.group().split("-")):  # butir-butir checks "butir" once
            if len(part) < 2:
                continue
            if in_heading:
                if len(part) > 3 or not part.isupper():
                    yield m.start(), part.lower()
                continue
            if part.isupper() or part[0].isupper() and not sentence_start(prose, m.start()):
                continue
            yield m.start(), part.lower()


def load_cache():
    cache = {}
    path = STYLE_DIR / "kbbi.tsv"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line and not line.startswith("#"):
                word, status, *rest = line.split("\t")
                cache[word] = (status, rest[0] if rest else "")
    return cache


def save_cache(cache):
    rows = "".join(f"{w}\t{s}\t{b}\n" for w, (s, b) in sorted(cache.items()))
    header = "# KBBI answers for style.py. Written by `make kbbi`; don't edit by hand.\n# word\tstatus (baku | tidak-baku | tidak-ada)\tstandard form\n"
    (STYLE_DIR / "kbbi.tsv").write_text(header + rows, encoding="utf-8")


def word_list(name):
    path = STYLE_DIR / name
    if not path.exists():
        return []
    lines = (l.split("#")[0].strip() for l in path.read_text(encoding="utf-8").splitlines())
    return [l for l in lines if l]


def parse_kbbi(page):
    """Read a KBBI daring entry page: ("baku" | "tidak-baku" | "tidak-ada", standard form).

    Returns None when the page isn't a normal entry page (an error, a limit,
    a login wall), so the answer is never cached by mistake.
    """
    if KBBI_FOOTER not in page or "<h2" not in page:
        return None
    if "Entri tidak ditemukan" in page:
        return ("tidak-ada", "")
    # The entries sit between the first heading and the editors' notice, whose
    # own list (benefits of signing up) must not count as a definition.
    start = page.index("<h2")
    end = page.find("Pesan Redaksi", start)
    entries = page[start:end if end != -1 else page.index(KBBI_FOOTER)]
    targets = []
    for li in re.findall(r"<li>(.*?)</li>", entries, re.S):
        text = " ".join(re.sub(r"<[^>]+>", " ", html.unescape(li)).split())
        link = re.search(r'href="[^"]*/entri/([^"]+)"', li)
        if not (text.startswith("→") and link):
            return ("baku", "")  # at least one real definition
        targets.append(urllib.parse.unquote(html.unescape(link.group(1))))
    return ("tidak-baku", targets[0]) if targets else None


class DailyLimit(Exception):
    """KBBI daring allows unregistered visitors a limited number of lookups a day."""


def is_daily_limit(page):
    return "BatasSehari" in page or "batas maksimum" in page


def fetch_kbbi(word):
    request = urllib.request.Request(KBBI_URL + word, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            page = response.read().decode("utf-8", "replace")
            if is_daily_limit(response.geturl() + page):
                raise DailyLimit()
            return parse_kbbi(page)
    except (OSError, http.client.HTTPException):  # URLError, timeouts, resets
        return None


def lookups(word):
    """The word, then the word without a clitic (gelombangnya -> gelombang)."""
    yield word
    for c in CLITICS:
        if word.endswith(c) and len(word) - len(c) >= 3:
            yield word[: -len(c)]


def judge(word, cache, allowed):
    """None if the word is fine, else (kind, message) with kind "error" or "unchecked"."""
    if word in allowed:
        return None
    status, standard = cache.get(word, (None, ""))
    if status == "baku":
        return None
    if status == "tidak-baku":
        return "error", f"'{word}' is not standard in KBBI; write '{standard}' (D4)"
    unchecked = "unchecked", f"'{word}' hasn't been checked against KBBI yet; run `make kbbi` (D7)"
    if status is None:
        return unchecked
    for base in list(lookups(word))[1:]:
        if cache.get(base, (None,))[0] == "baku":
            return None
        if base not in cache:
            return unchecked
    return "error", (f"'{word}' is not in KBBI: fix the spelling, put a foreign term in \\textit{{}} (D5),"
            " or add it to style/allow.txt")


def check(root, cache, strict=False):
    root = Path(root)
    allowed = set(word_list("allow.txt"))
    fillers = [(p, re.compile(r"\b" + r"\s+".join(map(re.escape, p.split())) + r"\b", re.I))
               for p in word_list("filler.txt")]
    errors, warnings = [], []
    for path in sorted(root.rglob("*.tex")):
        if path.name == "main.tex":
            continue  # shortcut: identity and English title live here; check \judul by eye
        with_math, prose, headings = prepare(tex_text(path))
        for m in DECIMAL.finditer(with_math):
            if not THOUSANDS.fullmatch(m.group()):
                errors.append((path, line_of(with_math, m.start()),
                               f"decimal point in '{m.group()}': write {m.group().replace('.', ',')} (D3)"))
        for pos, word in words(prose, headings):
            verdict = judge(word, cache, allowed)
            if verdict:
                kind, msg = verdict
                # Not looked up yet: a warning while KBBI's daily limit slows lookups (D7).
                (errors if kind == "error" or strict else warnings).append((path, line_of(prose, pos), msg))
        for phrase, pattern in fillers:
            for m in pattern.finditer(prose):
                warnings.append((path, line_of(prose, m.start()),
                                 f"filler phrase '{phrase}': say the point directly (D6)"))
    return errors, warnings


def update(root, cache):
    """Look up every word the check needs that isn't cached yet, one per second."""
    allowed = set(word_list("allow.txt"))
    needed = []
    for path in sorted(Path(root).rglob("*.tex")):
        if path.name != "main.tex":
            _, prose, headings = prepare(tex_text(path))
            needed += [w for _, w in words(prose, headings)]
    queue = [w for w in dict.fromkeys(needed) if w not in allowed and w not in cache]
    failed = []
    try:  # save whatever was looked up, even if the run is cut short
        while queue:
            word = queue.pop(0)
            try:
                answer = fetch_kbbi(word)
            except DailyLimit:
                queue.insert(0, word)
                print(f"kbbi: reached KBBI's daily limit for unregistered visitors; {len(queue)} word(s)"
                      " still to look up. Run `make kbbi` again tomorrow.")
                break
            time.sleep(1)  # be gentle with KBBI daring
            if answer is None:
                failed.append(word)
                continue
            cache[word] = answer
            print(f"kbbi: {word} -> {answer[0]} {answer[1]}".rstrip())
            if answer[0] == "tidak-ada":
                queue += [b for b in list(lookups(word))[1:] if b not in cache and b not in queue]
    finally:
        save_cache(cache)
    if failed:
        print(f"kbbi: couldn't read KBBI for {len(failed)} word(s), try again later: {', '.join(failed)}")


def report(errors, warnings):
    """Print every problem; in GitHub Actions also annotate lines and fill the job summary."""
    actions = os.environ.get("GITHUB_ACTIONS") == "true"
    for kind, items in (("error", errors), ("warning", warnings)):
        for path, n, msg in items:
            print(f"{path}:{n}: {kind}: {msg}")
            if actions:  # GitHub shows only the first 10 of each kind inline; the log has all
                print(f"::{kind} file={path},line={n}::{msg}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary and (errors or warnings):
        rows = "".join(f"| {k} | `{p}:{n}` | {m} |\n" for k, items in (("error", errors), ("warning", warnings))
                       for p, n, m in items)
        with open(summary, "a", encoding="utf-8") as f:
            f.write(f"### Style: {len(errors)} error(s), {len(warnings)} warning(s)\n\n| | Where | Problem |\n|---|---|---|\n{rows}")
    print(f"style: {len(errors)} error(s), {len(warnings)} warning(s)" if errors or warnings else "style: ok")


def main():
    args = [a for a in sys.argv[1:] if a not in ("--update", "--strict")]
    root = args[0] if args else "thesis"
    cache = load_cache()
    if "--update" in sys.argv:
        update(root, cache)
    errors, warnings = check(root, cache, strict="--strict" in sys.argv)
    report(errors, warnings)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
