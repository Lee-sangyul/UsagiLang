"""Local .usagi module import regression tests."""

import io
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from usagilang import Interpreter, UsagiError, tokenize


class ImportTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = pathlib.Path(self.tempdir.name)
        self.main = self.root / "main.usagi"

    def module(self, name, source):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source, encoding="utf-8")
        return target

    def execute(self, code, steps=100_000):
        stdout = io.StringIO()
        runner = Interpreter(stdout=stdout, max_steps=steps)
        runner.run(code, source_path=self.main)
        return stdout.getvalue()

    def test_import_japanese_and_korean(self):
        self.module("math.usagi", "ウララヤハ add(a,b) { ウラララ a+b }\nプルャ answer=42")
        code = ('import "math.usagi"\n'
                '우라 math.add(1, 2)\n'
                '가져와 "math.usagi" 별칭 계산\n'
                '우라 계산.answer\n'
                'インポート "math.usagi" として 数学\n'
                'ウラ 数学.add(3,4)')
        self.assertEqual(self.execute(code), "3\n42\n7\n")

    def test_separate_module_namespace(self):
        self.module("helpers.usagi", 'プルャ x=17\nウララヤハ get() { ウラララ x }')
        code = 'プルャ x=99\nimport "helpers.usagi" as h\nウラ x,h.get(),h.x'
        self.assertEqual(self.execute(code), "99 17 17\n")

    def test_does_not_expose_main_variables(self):
        self.module("bad.usagi", "ウラ hidden")
        with self.assertRaisesRegex(UsagiError, "정의되지 않은 이름"):
            self.execute('プルャ hidden=3\nimport "bad.usagi"')

    def test_repeated_import_runs_once(self):
        self.module("counter.usagi", 'ウラ "loaded"\nプルャ result=8')
        code = ('import "counter.usagi" as first\n'
                'import "./counter.usagi" as second\n'
                'ウラ first.result,second.result')
        self.assertEqual(self.execute(code), "loaded\n8 8\n")

    def test_nested_import_relative_to_module_file(self):
        self.module("values.usagi", "プルャ answer=7")
        self.module("sub/helper.usagi",
                    'ウララヤハ get() {\n'
                    ' import "../values.usagi" as values\n'
                    ' ウラララ values.answer\n'
                    '}')
        self.assertEqual(
            self.execute('import "sub/helper.usagi" as helper\nウラ helper.get()'),
            "7\n",
        )

    def test_unknown_member(self):
        self.module("library.usagi", "プルャ valid=1")
        with self.assertRaisesRegex(UsagiError, "정의되지 않은 이름"):
            self.execute('import "library.usagi" as lib\nウラ lib.missing')

    def test_member_on_non_module(self):
        with self.assertRaisesRegex(UsagiError, "모듈에서만"):
            self.execute('プルャ x=1\nウラ x.y')

    def test_reject_absolute_and_non_usagi_paths(self):
        self.module("python.py", 'print("No")')
        with self.assertRaisesRegex(UsagiError, "상대 경로"):
            self.execute('import "python.py"')
        with self.assertRaisesRegex(UsagiError, "상대 경로"):
            self.execute('import "/tmp/something.usagi"')

    def test_missing_module(self):
        with self.assertRaisesRegex(UsagiError, "import 파일 오류"):
            self.execute('import "missing.usagi"')

    def test_bad_module_syntax(self):
        self.module("broken.usagi", "ハァ ヤハ {")
        with self.assertRaisesRegex(UsagiError, "모듈 구문 오류"):
            self.execute('import "broken.usagi"')

    def test_circular_import(self):
        self.module("a.usagi", 'import "b.usagi"')
        self.module("b.usagi", 'import "a.usagi"')
        with self.assertRaisesRegex(UsagiError, "순환 import"):
            self.execute('import "a.usagi"')

    def test_module_counts_toward_step_limit(self):
        self.module("loop.usagi", "プルルルル ヤハ {}")
        with self.assertRaisesRegex(UsagiError, "실행 한도"):
            self.execute('import "loop.usagi"', steps=30)

    def test_module_error_has_path(self):
        self.module("broken.usagi", "ウラ missing")
        with self.assertRaisesRegex(UsagiError, r"broken\.usagi:1"):
            self.execute('import "broken.usagi"')

    def test_invalid_inferred_alias_needs_as(self):
        self.module("my-lib.usagi", "プルャ x=1")
        with self.assertRaisesRegex(UsagiError, "as/별칭/として"):
            self.execute('import "my-lib.usagi"')
        self.assertEqual(self.execute('import "my-lib.usagi" as usable\nウラ usable.x'), "1\n")

    def test_repository_example(self):
        code_path = ROOT / "examples" / "imports.usagi"
        code = code_path.read_text(encoding="utf-8")
        output = io.StringIO()
        Interpreter(stdout=output).run(code, source_path=code_path)
        self.assertEqual(output.getvalue(),
                         "4 squared = 16\n2 + 3 = 5\npi = 3.14159\n")

    def test_import_tokens(self):
        kinds = [t.kind for t in tokenize('import 가져와 インポート as 별칭 として')]
        self.assertEqual(kinds, ['IMPORT', 'IMPORT', 'IMPORT', 'AS', 'AS', 'AS', 'EOF'])


if __name__ == "__main__":
    unittest.main()
