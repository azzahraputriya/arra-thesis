"""Fixture tests for lint.py: a clean thesis passes, each broken rule is caught.

Run: python3 -m unittest discover -s scripts
"""
import tempfile
import unittest
from pathlib import Path

from lint import check

MAIN = r"""\documentclass{itbfisika}
\begin{document}
\input{chapters/01-pendahuluan}
% \input{chapters/lampiran}   commented out, must be ignored
\end{document}
"""
CHAPTER = "% note\n\\chapter{PENDAHULUAN}\nSeperti \\cite[hlm. 5]{Kramer1996, Seed1971}. Diskon 5\\%.\n\\includegraphics{rig}\n"
BIB = "@book{Kramer1996,\n title={x}}\n@article{Seed1971,\n title={y}}\n"


def build(test, files):
    tmp = tempfile.TemporaryDirectory()
    test.addCleanup(tmp.cleanup)
    root = Path(tmp.name)
    for name, text in {"main.tex": MAIN, "chapters/01-pendahuluan.tex": CHAPTER,
                       "references.bib": BIB, "figures/rig.png": "", **files}.items():
        if text is None:
            continue
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


class LintTest(unittest.TestCase):
    def messages(self, files):
        return [msg for _, _, msg in check(build(self, files))]

    def test_clean_thesis_passes(self):
        self.assertEqual(self.messages({}), [])

    def assertCaught(self, files, fragment):
        found = self.messages(files)
        self.assertTrue(any(fragment in m for m in found), f"{fragment!r} not in {found}")

    def test_include(self):
        self.assertCaught({"main.tex": MAIN.replace("\\input{chapters/01", "\\include{chapters/01")}, "use \\input")

    def test_missing_input(self):
        self.assertCaught({"main.tex": MAIN + "\\input{chapters/02-metode}\n"}, "missing file")

    def test_chapter_not_input(self):
        self.assertCaught({"chapters/02-metode.tex": "\\chapter{METODE}\n"}, "not \\input")

    def test_chapter_name(self):
        self.assertCaught({"chapters/metode.tex": "\\chapter{METODE}\n"}, "NN-name.tex")

    def test_appendix_name_allowed(self):
        self.assertEqual(self.messages({"chapters/lampiran.tex": "\\chapter{LAMPIRAN A}\n"}), [])

    def test_chapter_must_start_with_chapter(self):
        self.assertCaught({"chapters/01-pendahuluan.tex": "Teks dulu.\n\\chapter{PENDAHULUAN}\n"}, "start with \\chapter")

    def test_chapter_title_uppercase(self):
        self.assertCaught({"chapters/01-pendahuluan.tex": "\\chapter{Pendahuluan}\n"}, "uppercase")

    def test_preamble_in_chapter(self):
        self.assertCaught({"chapters/01-pendahuluan.tex": CHAPTER + "\\usepackage{xcolor}\n"}, "no preamble")

    def test_citet(self):
        self.assertCaught({"chapters/01-pendahuluan.tex": CHAPTER + "\\citet{Kramer1996}\n"}, "doesn't exist")

    def test_unknown_cite_key(self):
        self.assertCaught({"chapters/01-pendahuluan.tex": CHAPTER + "\\cite{Andrus2000}\n"}, "'Andrus2000' is not")

    def test_bib_key_format(self):
        self.assertCaught({"references.bib": BIB + "@misc{andrus_2000,\n}\n"}, "not AuthorYear")

    def test_duplicate_bib_key(self):
        self.assertCaught({"references.bib": BIB + "@misc{Seed1971,\n}\n"}, "duplicate")

    def test_figure_folder_prefix(self):
        self.assertCaught({"chapters/01-pendahuluan.tex": CHAPTER + "\\includegraphics{figures/rig}\n"}, "drop the folder")

    def test_figure_eps(self):
        self.assertCaught({"chapters/01-pendahuluan.tex": CHAPTER + "\\includegraphics[width=5cm]{rig.eps}\n"}, "EPS")

    def test_figure_missing(self):
        self.assertCaught({"chapters/01-pendahuluan.tex": CHAPTER + "\\includegraphics{shaker}\n"}, "no PDF, PNG or JPG")

    # Cases from the code review.
    def test_nocite_star(self):
        self.assertCaught({"chapters/01-pendahuluan.tex": CHAPTER + "\\nocite{*}\n"}, "no \\nocite{*}")

    def test_nocite_unknown_key(self):
        self.assertCaught({"chapters/01-pendahuluan.tex": CHAPTER + "\\nocite{Bogus2000}\n"}, "'Bogus2000' is not")

    def test_title_with_commands_passes(self):
        ch = "\\chapter{TINJAUAN \\textit{IN VITRO} $\\alpha$}\n"
        self.assertEqual(self.messages({"chapters/01-pendahuluan.tex": ch}), [])

    def test_starred_and_short_chapter_pass(self):
        for ch in ("\\chapter*{PENDAHULUAN}\n", "\\chapter[PENDAHULUAN]{PENDAHULUAN}\n"):
            self.assertEqual(self.messages({"chapters/01-pendahuluan.tex": ch}), [])

    def test_bib_key_on_next_line(self):
        bib = "@book{\n  Kramer1996,\n title={x}}\n@article(Seed1971,\n title={y})\n"
        self.assertEqual(self.messages({"references.bib": bib}), [])

    def test_comment_after_line_break(self):
        self.assertEqual(self.messages({"chapters/01-pendahuluan.tex": CHAPTER + "Baris\\\\% \\cite{Bogus2000}\n"}), [])

    def test_cite_across_lines(self):
        self.assertCaught({"chapters/01-pendahuluan.tex": CHAPTER + "\\cite{Kramer1996,\n Bogus2000}\n"}, "'Bogus2000' is not")

    def test_preamble_in_subfolder(self):
        self.assertCaught({"chapters/sub/x.tex": "\\usepackage{x}\n"}, "no preamble")

    def test_include_outside_main(self):
        self.assertCaught({"chapters/01-pendahuluan.tex": CHAPTER + "\\include{chapters/lampiran}\n",
                           "chapters/lampiran.tex": "\\chapter{LAMPIRAN}\n"}, "use \\input")

    def test_nested_input_counts(self):
        self.assertEqual(self.messages({"chapters/01-pendahuluan.tex": CHAPTER + "\\input{chapters/02-metode}\n",
                                        "chapters/02-metode.tex": "\\chapter{METODE}\n"}), [])

    def test_uppercase_extension_rejected(self):
        self.assertCaught({"figures/rig.png": None, "figures/foto.JPG": "",
                           "chapters/01-pendahuluan.tex": "\\chapter{PENDAHULUAN}\n\\includegraphics{foto}\n"},
                          "extensions must be lowercase")


if __name__ == "__main__":
    unittest.main()
