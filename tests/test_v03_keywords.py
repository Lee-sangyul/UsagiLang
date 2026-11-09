import io
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from usagilang import Interpreter, tokenize


class V03KeywordsTests(unittest.TestCase):
    def execute(self, source, path=None):
        output = io.StringIO()
        Interpreter(stdin=io.StringIO(), stdout=output).run(source, source_path=path)
        return output.getvalue()

    def test_all_keyword_aliases(self):
        aliases = {
            "ウラウラ": "IN", "우라우라": "IN",
            "ウルウル": "AND", "우루우루": "AND",
            "ヤハヤハ": "OR", "야하야하": "OR",
            "イヤハ": "NOT", "이야하": "NOT",
            "ナイナイ": "NONE", "나이나이": "NONE",
            "ハイ": "IMPORT", "하이": "IMPORT",
            "ウララ": "AS", "우라라": "AS",
            "プルップラッ": "TRY", "푸룻푸랏": "TRY",
            "ウギッ": "CATCH", "우깃": "CATCH",
        }
        for word, expected in aliases.items():
            with self.subTest(word=word):
                self.assertEqual(tokenize(word)[0].kind, expected)

    def test_for_and_logic(self):
        source = """
푸루야 total = 0
츠츠우라우라 x 우라우라 [1,2,3] {
    하아 x > 1 우루우루 이야하 (x == 3) { total = total + x }
}
하아 total == 2 야하야하 우나야하야하 { 우라 total }
우라 나이나이
"""
        self.assertEqual(self.execute(source), "2\nナシ\n")

    def test_japanese_logic(self):
        source = 'ハァ ヤハ ウルウル イヤハ ウーラーヤハヤハ { ウラ "OK" }'
        self.assertEqual(self.execute(source), "OK\n")

    def test_try_catch(self):
        self.assertEqual(self.execute('푸룻푸랏 { 던지기 "boom" } 우깃 e { 우라 e }'), "boom\n")
        self.assertEqual(self.execute('プルップラッ { なげる "error" } ウギッ e { ウラ e }'), "error\n")

    def test_import_alias_both_languages(self):
        with tempfile.TemporaryDirectory() as directory:
            main = pathlib.Path(directory) / "main.usagi"
            (pathlib.Path(directory) / "lib.usagi").write_text('プルャ answer = 42', encoding="utf-8")
            self.assertEqual(self.execute('ハイ "lib.usagi" ウララ module\nウラ module.answer', main), "42\n")
            self.assertEqual(self.execute('하이 "lib.usagi" 우라라 module\n우라 module.answer', main), "42\n")

    def test_legacy_syntax_still_works(self):
        source = 'try { throw "old" } catch e { print(e) }'
        # 'print' is not a keyword; ensure legacy PRINT spelling remains usable.
        source = 'try { throw "old" } catch e { ウラ e }'
        self.assertEqual(self.execute(source), "old\n")
        self.assertEqual(self.execute('츠츠우라우라 x in [1] { 우라 x }'), "1\n")


if __name__ == "__main__":
    unittest.main()
