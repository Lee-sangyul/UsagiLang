import io
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from usagilang import Interpreter, UsagiError, tokenize


class UsagiLangTests(unittest.TestCase):
    def run_program(self, source, stdin="", steps=100_000):
        output = io.StringIO()
        Interpreter(io.StringIO(stdin), output, max_steps=steps).run(source)
        return output.getvalue()

    def test_hello(self):
        self.assertEqual(self.run_program('ウラ "Hello!"\n우라 "야하!"'), "Hello!\n야하!\n")

    def test_mixed_aliases_and_if(self):
        source = '푸루야 yes = ヤハ\n하아 yes { 우라 "OK" } 후웅 { ウラ "NO" }'
        self.assertEqual(self.run_program(source), "OK\n")

    def test_while(self):
        self.assertEqual(self.run_program('プルャ n=0\nプルルルル n<3 { ウラ n\nn=n+1 }'), '0\n1\n2\n')

    def test_for_and_continue_break(self):
        source = '츠츠우라우라 x 안에 [1,2,3,4] { 하아 x==2 { 푸왓 } 하아 x==4 { 사쿠 } 우라 x }'
        self.assertEqual(self.run_program(source), '1\n3\n')

    def test_function_and_recursion(self):
        code = (ROOT / 'examples' / 'functions.usagi').read_text(encoding='utf-8')
        self.assertEqual(self.run_program(code), '5! = 120\n')

    def test_input_jp_and_ko(self):
        source = '푸루야 x=하이야하우나("이름? ")\nウラ x'
        self.assertEqual(self.run_program(source, '토끼\n'), '이름? 토끼\n')

    def test_bool_and_lists(self):
        self.assertEqual(self.run_program('ウラ ヤハ\n우라 우나야하야하\n우라 [1,2][1]'), 'ヤハ\nウーラーヤハヤハ\n2\n')

    def test_logic_short_circuit(self):
        self.assertEqual(self.run_program('우라 ヤハ 그리고 not 우나야하야하'), 'ヤハ\n')

    def test_undefined_variable_error(self):
        with self.assertRaisesRegex(UsagiError, '정의되지 않은 이름'):
            self.run_program('ウラ missing')

    def test_divide_zero_error(self):
        with self.assertRaisesRegex(UsagiError, '연산 오류'):
            self.run_program('ウラ 1/0')

    def test_step_limit(self):
        with self.assertRaisesRegex(UsagiError, '실행 한도'):
            self.run_program('プルルルル ヤハ {}', steps=100)

    def test_string_escape_and_comments(self):
        self.assertEqual(self.run_program('우라 "A\\nB" // comment\n# comment\n우라 "C"'), 'A\nB\nC\n')

    def test_bad_syntax(self):
        with self.assertRaises(UsagiError):
            self.run_program('ハァ ヤハ { ウラ "x"')

    def test_korean_and_japanese_lexer(self):
        kinds = [t.kind for t in tokenize('ウーラーヤハヤハ 우나야하야하 ウララヤハ 우라라야하')]
        self.assertEqual(kinds, ['FALSE', 'FALSE', 'FUNC', 'FUNC', 'EOF'])

    def test_range_function(self):
        self.assertEqual(self.run_program('츠츠우라우라 n in range(3) { 우라 n }'), '0\n1\n2\n')

    def test_else_branch(self):
        self.assertEqual(self.run_program('ハァ ウーラーヤハヤハ { ウラ "no" } フゥン { 우라 "yes" }'), 'yes\n')

    def test_mandatory_separator(self):
        with self.assertRaisesRegex(UsagiError, '줄바꿈'):
            self.run_program('우라 1 우라 2')

    def test_return_outside_function(self):
        with self.assertRaisesRegex(UsagiError, '함수 밖'):
            self.run_program('ウラララ 10')

    def test_examples(self):
        for filename in ['hello.usagi', 'mixed.usagi', 'lists.usagi', 'fizzbuzz.usagi']:
            with self.subTest(filename=filename):
                code = (ROOT / 'examples' / filename).read_text(encoding='utf-8')
                self.assertTrue(self.run_program(code))


if __name__ == '__main__':
    unittest.main()