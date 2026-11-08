"""Feature regression tests for UsagiLang v0.2."""

import contextlib
import io
import os
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from usagilang import Interpreter, UsagiError, diagnostic, main, repl_loop, tokenize
from usagi_packages import command, PackageError


class FeatureTests(unittest.TestCase):
    def run_program(self, src):
        output = io.StringIO()
        Interpreter(stdout=output).run(src)
        return output.getvalue()

    def test_index_assignment(self):
        self.assertEqual(self.run_program(
            'プルャ xs=[1,2]\nxs[0]=9\nウラ xs'
        ), '[9, 2]\n')

    def test_append_and_pop(self):
        self.assertEqual(self.run_program(
            'プルャ xs=[1]\nxs.append(2)\nウラ xs.pop(),len(xs)'
        ), '2 1\n')

    def test_insert_and_global_append(self):
        self.assertEqual(self.run_program(
            'プルャ xs=[2]\nxs.insert(0,1)\nappend(xs,3)\nウラ xs'
        ), '[1, 2, 3]\n')

    def test_invalid_list_assignment(self):
        with self.assertRaisesRegex(UsagiError, '리스트 요소'):
            self.run_program('プルャ s="abc"\ns[0]=10')

    def test_stdlib_math(self):
        self.assertEqual(self.run_program(
            'ウラ math.sqrt(16), math.floor(2.8), abs(-3)'
        ), '4.0 2 3\n')

    def test_stdlib_text(self):
        self.assertEqual(self.run_program(
            'ウラ text.upper("hello"),text.join("-",text.split("a,b",","))'
        ), 'HELLO a-b\n')

    def test_stdlib_random(self):
        self.assertEqual(self.run_program('ウラ random.randint(1,1)'), '1\n')

    def test_stdlib_clock(self):
        self.assertEqual(self.run_program('ウラ clock.now()>0'), 'ヤハ\n')

    def test_class_fields_and_methods(self):
        code = """
class Counter {
    func init(self, n) {
        self.n = n
    }
    func inc(self) {
        self.n = self.n + 1
        return self.n
    }
}
プルャ c = Counter(4)
ウラ c.inc(), c.n
"""
        self.assertEqual(self.run_program(code), '5 5\n')

    def test_class_japanese_korean_aliases(self):
        code = """
クラス Thing {
    우라라야하 init(self) { self.value = 6 }
}
プルャ t = Thing()
ウラ t.value
"""
        self.assertEqual(self.run_program(code), '6\n')

    def test_class_without_initializer(self):
        self.assertEqual(self.run_program(
            'class Empty {}\nプルャ a=Empty()\na.name="Usagi"\nウラ a.name'
        ), 'Usagi\n')

    def test_invalid_member_assignment(self):
        with self.assertRaisesRegex(UsagiError, '인스턴스 필드'):
            self.run_program('プルャ x=[1]\nx.bad=2')

    def test_exception_handling(self):
        self.assertEqual(self.run_program(
            'try { throw "ouch" } catch err { ウラ err }'
        ), 'ouch\n')

    def test_exception_aliases(self):
        self.assertEqual(self.run_program(
            '시도 { 던지기 "야하!" } 잡기 문제 { 우라 문제 }'
        ), '야하!\n')

    def test_exception_on_builtin(self):
        self.assertIn('sqrt', self.run_program(
            'ためす { ウラ math.sqrt(-1) } つかまえる e { ウラ e }'
        ))

    def test_uncaught_throw(self):
        with self.assertRaisesRegex(UsagiError, 'oops'):
            self.run_program('throw "oops"')

    def test_error_code_and_diagnostic(self):
        err = UsagiError("정의되지 않은 이름: thing", 1, 4)
        rendered = diagnostic(err, "ウラ thing", "demo.usagi")
        self.assertIn("ヤダ", rendered)
        self.assertIn("[E100]", rendered)
        self.assertIn("demo.usagi:1:4", rendered)
        self.assertIn("^", rendered)
        self.assertIn("💡", rendered)

    def test_plain_diagnostic(self):
        msg = diagnostic(UsagiError("bad", 1), 'x', themed=False)
        self.assertNotIn('ヤダ', msg)

    def test_repl_state_and_reset(self):
        reader = io.StringIO(
            'プルャ x=4\nウラ x\n:reset\nプルャ x=9\nウラ x\n:exit\n'
        )
        output, errors = io.StringIO(), io.StringIO()
        self.assertEqual(repl_loop(reader, output, errors), 0)
        self.assertEqual(errors.getvalue(), '')
        self.assertIn('4\n', output.getvalue())
        self.assertIn('9\n', output.getvalue())

    def test_repl_multiline(self):
        reader = io.StringIO('プルャ x=0\nプルルルル x<2 {\nx=x+1\n}\nウラ x\n:exit\n')
        output, errors = io.StringIO(), io.StringIO()
        repl_loop(reader, output, errors)
        self.assertEqual(errors.getvalue(), '')
        self.assertIn('2\n', output.getvalue())

    def test_repl_bad_statement_continue(self):
        reader = io.StringIO('ウラ unknown\nウラ "ok"\n:exit\n')
        output, errors = io.StringIO(), io.StringIO()
        repl_loop(reader, output, errors)
        self.assertIn('ok\n', output.getvalue())
        self.assertIn('정의되지 않은 이름', errors.getvalue())

    def test_check_does_not_execute(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "a.usagi"
            path.write_text('ウラ "should not print"', encoding='utf-8')
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = main(['check', str(path)])
            self.assertEqual(result, 0)
            self.assertNotIn('should not print', output.getvalue())

    def test_legacy_cli(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(['-c', 'ウラ "legacy"'])
        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), 'legacy\n')

    def test_run_cli(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(['run', '-c', 'ウラ "new"'])
        self.assertEqual(result, 0)
        self.assertEqual(output.getvalue(), 'new\n')

    def test_syntax_failure_check(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "a.usagi"
            path.write_text("ハァ ヤハ {", encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stderr(output):
                result = main(['check', str(path)])
            self.assertEqual(result, 1)
            self.assertIn('ヤダ', output.getvalue())

    def test_keywords(self):
        kinds = [t.kind for t in tokenize(
            'class 클래스 クラス try 시도 ためす catch 잡기 つかまえる throw 던지기 なげる'
        )]
        self.assertEqual(kinds[:-1], [
            'CLASS','CLASS','CLASS','TRY','TRY','TRY',
            'CATCH','CATCH','CATCH','THROW','THROW','THROW'
        ])

    def test_package_manager_local_roundtrip(self):
        with tempfile.TemporaryDirectory() as temp:
            old = pathlib.Path.cwd()
            try:
                os.chdir(temp)
                pathlib.Path("helper.usagi").write_text(
                    'func add(a,b) { return a+b }', encoding="utf-8"
                )
                out = io.StringIO()
                self.assertEqual(command(['init'], out), 0)
                self.assertEqual(command(['add', 'helper', 'helper.usagi'], out), 0)
                self.assertEqual(command(['verify'], out), 0)
                code = 'import "pkg:helper" as helper\nウラ helper.add(2,3)'
                out2 = io.StringIO()
                Interpreter(stdout=out2).run(code, source_path=pathlib.Path(temp)/"main.usagi")
                self.assertEqual(out2.getvalue(), '5\n')
                self.assertEqual(command(['remove', 'helper'], out), 0)
            finally:
                os.chdir(old)

    def test_package_manager_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            old = pathlib.Path.cwd()
            try:
                os.chdir(root)
                command(['init'], io.StringIO())
                with self.assertRaises(PackageError):
                    command(['add','unsafe','../outside.usagi'], io.StringIO())
            finally:
                os.chdir(old)


if __name__ == "__main__":
    unittest.main()
