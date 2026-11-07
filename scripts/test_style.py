"""Tests for style.py. Offline: a fake KBBI cache and saved KBBI pages.

Run: python3 -m unittest discover -s scripts
"""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import style

FIXTURES = Path(__file__).parent / "fixtures" / "kbbi"
CACHE = {w: ("baku", "") for w in
         "contoh sitasi nilai gelombang butir tanah pasir bangunan subbab dan di lihat hasil "
         "hal ini menunjukkan bahwa uji tulis kata pengantar abstrak sini pada potensi tinjauan pendahuluan".split()}
CACHE.update({"likuifaksi": ("tidak-baku", "likuefaksi"), "dimana": ("tidak-ada", ""),
              "shear": ("tidak-ada", ""), "gelombangnya": ("tidak-ada", "")})


class ParseKbbiTest(unittest.TestCase):
    def parse(self, name):
        return style.parse_kbbi((FIXTURES / f"{name}.html").read_text(encoding="utf-8"))

    def test_standard_word(self):
        self.assertEqual(self.parse("likuefaksi"), ("baku", ""))

    def test_non_standard_word_points_to_standard(self):
        self.assertEqual(self.parse("likuifaksi"), ("tidak-baku", "likuefaksi"))

    def test_word_not_in_kbbi(self):
        self.assertEqual(self.parse("berprilaku"), ("tidak-ada", ""))

    def test_derived_word(self):
        self.assertEqual(self.parse("berperilaku"), ("baku", ""))

    def test_word_with_numbered_meanings(self):
        self.assertEqual(self.parse("analisis"), ("baku", ""))

    def test_daily_limit_page(self):
        page = (FIXTURES / "batas-sehari.html").read_text(encoding="utf-8")
        self.assertTrue(style.is_daily_limit(page))
        self.assertIsNone(style.parse_kbbi(page))

    def test_update_stops_at_daily_limit(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        (root / "style").mkdir()
        (root / "thesis").mkdir()
        (root / "thesis" / "a.tex").write_text("satu dua tiga\n")
        calls = []

        def fake_fetch(word):
            calls.append(word)
            if word == "dua":
                raise style.DailyLimit()
            return ("baku", "")

        cache = {}
        with mock.patch.object(style, "STYLE_DIR", root / "style"), \
                mock.patch.object(style, "fetch_kbbi", fake_fetch), mock.patch.object(style.time, "sleep"), \
                redirect_stdout(io.StringIO()):
            style.update(root / "thesis", cache)
        self.assertEqual(calls, ["satu", "dua"])  # stops at the limit, doesn't try "tiga"
        self.assertEqual(cache, {"satu": ("baku", "")})
        self.assertIn("satu\tbaku", (root / "style" / "kbbi.tsv").read_text())

    def test_target_is_url_decoded(self):
        page = ('<h2>x</h2><ul class="adjusted-par"><li>&rarr; <a href="../../entri/beri%20tahu">beri tahu</a></li>'
                '</ul> Pesan Redaksi Badan Pengembangan dan Pembinaan Bahasa')
        self.assertEqual(style.parse_kbbi(page), ("tidak-baku", "beri tahu"))

    def test_update_saves_when_cut_short(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        (root / "style").mkdir()
        (root / "thesis").mkdir()
        (root / "thesis" / "a.tex").write_text("satu dua\n")

        def fake_fetch(word):
            if word == "dua":
                raise KeyboardInterrupt
            return ("baku", "")

        with mock.patch.object(style, "STYLE_DIR", root / "style"), \
                mock.patch.object(style, "fetch_kbbi", fake_fetch), mock.patch.object(style.time, "sleep"), \
                redirect_stdout(io.StringIO()), self.assertRaises(KeyboardInterrupt):
            style.update(root / "thesis", {})
        self.assertIn("satu\tbaku", (root / "style" / "kbbi.tsv").read_text())

    def test_odd_pages_are_unknown_not_cached(self):
        self.assertIsNone(style.parse_kbbi("<html>Error</html>"))
        self.assertIsNone(style.parse_kbbi("Badan Pengembangan dan Pembinaan Bahasa, no entry"))


class CheckTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        (self.root / "style").mkdir()
        (self.root / "style" / "allow.txt").write_text("cm  # unit\nkramer  # name\n")
        (self.root / "style" / "filler.txt").write_text("# comment\nhal ini menunjukkan bahwa\n")
        patcher = mock.patch.object(style, "STYLE_DIR", self.root / "style")
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_check(self, body, extra=None):
        files = {"thesis/chapters/01-x.tex": body, **(extra or {})}
        for name, text in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        return style.check(self.root / "thesis", CACHE)

    def errors(self, body, extra=None):
        return [m for _, _, m in self.run_check(body, extra)[0]]

    def assertError(self, body, fragment):
        found = self.errors(body)
        self.assertTrue(any(fragment in m for m in found), f"{fragment!r} not in {found}")

    def test_clean_text_passes(self):
        body = "\\chapter{PENDAHULUAN}\nContoh sitasi \\cite{Kramer1996} pada \\ref{fig:uji-rig}.\n"
        self.assertEqual(self.errors(body), [])

    def test_non_standard_word(self):
        self.assertError("Contoh likuifaksi.\n", "write 'likuefaksi'")

    def test_word_not_in_kbbi(self):
        self.assertError("Contoh dimana sitasi.\n", "'dimana' is not in KBBI")

    def test_italic_foreign_term_passes(self):
        self.assertEqual(self.errors("Contoh \\textit{shear wave} dan \\emph{sonic viewer}.\n"), [])

    def test_foreign_term_without_italics(self):
        self.assertError("Contoh shear sitasi.\n", "'shear' is not in KBBI")

    def test_unchecked_word_warns(self):
        errors, warnings = self.run_check("Contoh sitasi baru.\n")
        self.assertEqual(errors, [])
        self.assertTrue(any("run `make kbbi`" in m for _, _, m in warnings))

    def test_unchecked_word_fails_when_strict(self):
        path = self.root / "thesis/chapters/01-x.tex"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("Contoh sitasi baru.\n")
        errors, _ = style.check(self.root / "thesis", CACHE, strict=True)
        self.assertTrue(any("run `make kbbi`" in m for _, _, m in errors))

    def test_clitic_falls_back_to_base(self):
        self.assertEqual(self.errors("Contoh gelombangnya.\n"), [])

    def test_reduplication_checks_base(self):
        self.assertEqual(self.errors("Contoh butir-butir tanah.\n"), [])

    def test_name_inside_sentence_skipped(self):
        self.assertEqual(self.errors("Contoh sitasi Terzaghi dan Palu.\n"), [])

    def test_sentence_start_is_checked(self):
        self.assertError("Contoh sitasi. Likuifaksi dan tanah.\n", "write 'likuefaksi'")

    def test_abbreviation_skipped(self):
        self.assertEqual(self.errors("Contoh SPT dan CPT.\n"), [])

    def test_allow_list(self):
        self.assertEqual(self.errors("Contoh 5 cm.\n"), [])

    def test_math_words_skipped(self):
        self.assertEqual(self.errors("Contoh $V_s = \\sqrt{\\mu / \\rho}$.\n"), [])

    def test_decimal_point_in_prose(self):
        self.assertError("Nilai 1.5631 Hz.\n", "write 1,5631")

    def test_decimal_point_at_sentence_end(self):
        self.assertError("Nilai 1.5.\n", "write 1,5")

    def test_decimal_point_in_math(self):
        self.assertError("Nilai $v = 1.5$.\n", "write 1,5")

    def test_valid_numbers_pass(self):
        body = ("Nilai 1,5 dan $v = 0,25$ dan 2.895 bangunan pada subbab II.3.1.\n"
                "\\includegraphics[width=0.5\\textwidth]{rig}\\hspace{0.5cm} dan 0.8\\linewidth\n")
        self.assertEqual(self.errors(body), [])

    def test_english_abstract_and_main_skipped(self):
        extra = {"thesis/front/abstract.tex": "\\begin{abstract}\nThe value is 0.5 here.\n\\end{abstract}\n",
                 "thesis/main.tex": "\\judulinggris{Shear Wave Velocity 0.5}\n"}
        self.assertEqual(self.errors("Contoh sitasi.\n", extra), [])

    def test_filler_is_warning_across_lines(self):
        errors, warnings = self.run_check("Hasil uji. Hal ini\nmenunjukkan bahwa tanah.\n")
        self.assertEqual(errors, [])
        self.assertEqual([(n, "filler" in m) for _, n, m in warnings], [(1, True)])

    def test_line_numbers(self):
        errors, _ = self.run_check("Contoh sitasi.\n% likuifaksi in a comment\n\nNilai likuifaksi.\n")
        self.assertEqual([n for _, n, _ in errors], [4])

    # Cases from the code review.
    def test_equation_block_skipped_but_decimals_checked(self):
        body = "Contoh sitasi.\n\\begin{equation}\n u_{max} = 0,5 \\tau\n\\end{equation}\n"
        self.assertEqual(self.errors(body), [])
        self.assertError(body.replace("0,5", "0.5"), "write 0,5")

    def test_line_break_with_spacing_is_not_math(self):
        self.assertError("Contoh\\\\[2mm] likuifaksi \\[ x \\]\n", "write 'likuefaksi'")

    def test_leading_zero_is_never_thousands(self):
        self.assertError("Nilai 0.125.\n", "write 0,125")

    def test_float_options_and_table_spec_skipped(self):
        body = "\\begin{figure}[htbp]\nContoh.\n\\end{figure}\n\\begin{tabular}{lcr}\nnilai & tanah\n\\end{tabular}\n"
        self.assertEqual(self.errors(body), [])

    def test_headings_checked_whatever_the_case(self):
        self.assertError("\\section{Potensi Likuifaksi Tanah}\nContoh.\n", "write 'likuefaksi'")
        self.assertError("\\chapter{TINJAUAN LIKUIFAKSI}\nContoh.\n", "write 'likuefaksi'")
        self.assertEqual(self.errors("\\section{Potensi SPT}\nContoh.\n"), [])

    def test_numbers_with_several_dots_pass(self):
        self.assertEqual(self.errors("Contoh 2.3.1 dan 1.234.567 tanah.\n"), [])

    def test_github_annotations(self):
        out = io.StringIO()
        with mock.patch.dict(os.environ, {"GITHUB_ACTIONS": "true", "GITHUB_STEP_SUMMARY": ""}), redirect_stdout(out):
            style.report([(Path("a.tex"), 3, "bad")], [(Path("a.tex"), 4, "meh")])
        self.assertIn("::error file=a.tex,line=3::bad", out.getvalue())
        self.assertIn("::warning file=a.tex,line=4::meh", out.getvalue())


if __name__ == "__main__":
    unittest.main()
