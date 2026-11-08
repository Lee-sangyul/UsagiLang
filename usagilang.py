#!/usr/bin/env python3
"""UsagiLang v0.1 — 비공식 우사기어 기반 교육용 인터프리터 (Python 3.10+).

사용법: python usagilang.py examples/hello.usagi
        python usagilang.py -c 'ウラ "야하!"'
"""

from __future__ import annotations

import argparse
import json
import math as pymath
import random as pyrandom
import time
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any, Callable, TextIO


# 한국어/일본어 표기는 모두 동일한 토큰으로 처리한다.
KEYWORDS = {
    "プルャ": "LET", "푸루야": "LET",
    "ウラ": "PRINT", "우라": "PRINT",
    "ハァヤハウラ": "INPUT", "하아야하우라": "INPUT", "하이야하우나": "INPUT",
    "ヤハ": "TRUE", "야하": "TRUE",
    "ウーラーヤハヤハ": "FALSE", "우라야하야하": "FALSE", "우나야하야하": "FALSE",
    "ハァ": "IF", "하아": "IF",
    "フゥン": "ELSE", "후웅": "ELSE",
    "プルルルル": "WHILE", "푸루루루루": "WHILE", "푸루루루": "WHILE",
    "ツツウラウラ": "FOR", "츠츠우라우라": "FOR",
    "ウラララ": "RETURN", "우라라라": "RETURN",
    "サクッ": "BREAK", "사쿠": "BREAK",
    "プワッ": "CONTINUE", "푸왓": "CONTINUE",
    "ウララヤハ": "FUNC", "우라라야하": "FUNC",
    "in": "IN", "안에": "IN",
    "and": "AND", "그리고": "AND",
    "or": "OR", "또는": "OR",
    "not": "NOT", "아님": "NOT",
    "ナシ": "NONE", "없음": "NONE", "null": "NONE",
    "import": "IMPORT", "가져와": "IMPORT", "インポート": "IMPORT",
    "as": "AS", "별칭": "AS", "として": "AS",
    "class": "CLASS", "클래스": "CLASS", "クラス": "CLASS",
    "try": "TRY", "시도": "TRY", "ためす": "TRY",
    "catch": "CATCH", "잡기": "CATCH", "つかまえる": "CATCH",
    "throw": "THROW", "던지기": "THROW", "なげる": "THROW",
}

OPERATORS = {
    "==": "EQ", "!=": "NE", "<=": "LE", ">=": "GE",
    "&&": "AND", "||": "OR",
    "+": "PLUS", "-": "MINUS", "*": "STAR", "/": "SLASH", "%": "PERCENT",
    "<": "LT", ">": "GT", "!": "NOT", "=": "ASSIGN",
    "(": "LPAREN", ")": "RPAREN", "{": "LBRACE", "}": "RBRACE",
    "[": "LBRACKET", "]": "RBRACKET", ",": "COMMA", ";": "SEP", ".": "DOT",
}


class UsagiError(Exception):
    def __init__(self, message: str, line: int = 0, column: int = 0,
                 code: str = "E100"):
        super().__init__(message)
        self.line = line
        self.column = column
        self.code = code


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    value: Any
    line: int
    column: int


@dataclass(frozen=True)
class Node:
    kind: str
    args: tuple[Any, ...]
    line: int


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    i, line, col = 0, 1, 1

    def add(kind: str, raw: str, value: Any = None, at_line: int | None = None, at_col: int | None = None) -> None:
        tokens.append(Token(kind, raw, raw if value is None else value,
                            line if at_line is None else at_line,
                            col if at_col is None else at_col))

    while i < len(source):
        ch = source[i]
        start_line, start_col = line, col

        if ch in " \t\r":
            i += 1
            col += 1
            continue
        if ch == "\n":
            add("SEP", "\\n")
            i += 1
            line += 1
            col = 1
            continue
        if ch == "#" or source.startswith("//", i):
            while i < len(source) and source[i] != "\n":
                i += 1
                col += 1
            continue
        if ch in ('"', "'"):
            quote = ch
            i += 1
            col += 1
            chars: list[str] = []
            escapes = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "'": "'"}
            while i < len(source) and source[i] != quote:
                if source[i] == "\n":
                    raise UsagiError("문자열이 닫히지 않았어요.", start_line, start_col)
                if source[i] == "\\":
                    i += 1
                    col += 1
                    if i >= len(source) or source[i] not in escapes:
                        raise UsagiError("지원하지 않는 문자열 이스케이프예요.", line, col)
                    chars.append(escapes[source[i]])
                else:
                    chars.append(source[i])
                i += 1
                col += 1
            if i >= len(source):
                raise UsagiError("문자열이 닫히지 않았어요.", start_line, start_col)
            i += 1
            col += 1
            add("STRING", source[i - (col - start_col):i], "".join(chars), start_line, start_col)
            continue
        if ch.isdigit():
            start = i
            while i < len(source) and source[i].isdigit():
                i += 1
            if i + 1 < len(source) and source[i] == "." and source[i + 1].isdigit():
                i += 1
                while i < len(source) and source[i].isdigit():
                    i += 1
            raw = source[start:i]
            add("NUMBER", raw, float(raw) if "." in raw else int(raw))
            col += i - start
            continue
        if ch.isalpha() or ch == "_":
            start = i
            while i < len(source) and (source[i].isalnum() or source[i] == "_"):
                i += 1
            raw = source[start:i]
            add(KEYWORDS.get(raw, "NAME"), raw)
            col += i - start
            continue
        op = next((x for x in ("==", "!=", "<=", ">=", "&&", "||") if source.startswith(x, i)), None)
        if op is None:
            op = ch if ch in OPERATORS else None
        if op is None:
            raise UsagiError(f"알 수 없는 문자: {ch!r}", line, col)
        add(OPERATORS[op], op)
        i += len(op)
        col += len(op)

    tokens.append(Token("EOF", "", None, line, col))
    return tokens


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    @property
    def cur(self) -> Token:
        return self.tokens[self.pos]

    def peek(self, offset: int = 1) -> Token:
        return self.tokens[min(self.pos + offset, len(self.tokens) - 1)]

    def take(self, kind: str | None = None) -> Token:
        token = self.cur
        if kind is not None and token.kind != kind:
            raise UsagiError(f"{kind} 토큰이 필요하지만 {token.text!r}를 만났어요.", token.line, token.column)
        self.pos += 1
        return token

    def accept(self, kind: str) -> bool:
        if self.cur.kind == kind:
            self.pos += 1
            return True
        return False

    def skip_seps(self) -> None:
        while self.accept("SEP"):
            pass

    def parse(self) -> list[Node]:
        result: list[Node] = []
        self.skip_seps()
        while self.cur.kind != "EOF":
            if self.cur.kind == "RBRACE":
                raise UsagiError("닫는 중괄호가 너무 많아요.", self.cur.line, self.cur.column)
            stmt = self.statement()
            result.append(stmt)
            self.require_separator(stmt)
            self.skip_seps()
        return result

    def require_separator(self, stmt: Node) -> None:
        # 블록문은 중괄호가 구문을 나누므로 별도 줄바꿈이 필수가 아니다.
        if stmt.kind in ("if", "while", "for", "func", "class", "try"):
            return
        if (self.cur.kind not in ("SEP", "EOF", "RBRACE")
                and self.tokens[self.pos - 1].kind != "SEP"):
            t = self.cur
            raise UsagiError("명령어 사이에 줄바꿈 또는 ; 이 필요해요.", t.line, t.column)

    def block(self) -> list[Node]:
        self.take("LBRACE")
        result: list[Node] = []
        self.skip_seps()
        while self.cur.kind not in ("RBRACE", "EOF"):
            stmt = self.statement()
            result.append(stmt)
            self.require_separator(stmt)
            self.skip_seps()
        self.take("RBRACE")
        return result

    def statement(self) -> Node:
        t = self.cur
        if self.accept("IMPORT"):
            filename = self.take("STRING").value
            alias = self.take("NAME").text if self.accept("AS") else None
            return Node("import", (filename, alias), t.line)
        if self.accept("CLASS"):
            name = self.take("NAME").text
            methods = self.block()
            if any(method.kind != "func" for method in methods):
                raise UsagiError("클래스 안에는 함수 선언만 넣을 수 있어요.", t.line)
            if len({method.args[0] for method in methods}) != len(methods):
                raise UsagiError("클래스 메서드가 중복됐어요.", t.line)
            return Node("class", (name, methods), t.line)
        if self.accept("TRY"):
            body = self.block()
            self.skip_seps()
            self.take("CATCH")
            name = self.take("NAME").text
            handler = self.block()
            return Node("try", (body, name, handler), t.line)
        if self.accept("THROW"):
            return Node("throw", (self.expr(),), t.line)
        if self.accept("LET"):
            name = self.take("NAME").text
            self.take("ASSIGN")
            return Node("let", (name, self.expr()), t.line)
        if self.accept("PRINT"):
            values = []
            if self.cur.kind not in ("SEP", "EOF", "RBRACE"):
                values.append(self.expr())
                while self.accept("COMMA"):
                    values.append(self.expr())
            return Node("print", (values,), t.line)
        if self.accept("IF"):
            condition = self.expr()
            yes = self.block()
            self.skip_seps()
            no = self.block() if self.accept("ELSE") else []
            return Node("if", (condition, yes, no), t.line)
        if self.accept("WHILE"):
            condition = self.expr()
            return Node("while", (condition, self.block()), t.line)
        if self.accept("FOR"):
            name = self.take("NAME").text
            self.take("IN")
            iterable = self.expr()
            return Node("for", (name, iterable, self.block()), t.line)
        if self.accept("FUNC"):
            name = self.take("NAME").text
            self.take("LPAREN")
            params: list[str] = []
            if self.cur.kind != "RPAREN":
                params.append(self.take("NAME").text)
                while self.accept("COMMA"):
                    params.append(self.take("NAME").text)
            self.take("RPAREN")
            if len(set(params)) != len(params):
                raise UsagiError("함수 매개변수 이름이 중복됐어요.", t.line)
            return Node("func", (name, params, self.block()), t.line)
        if self.accept("RETURN"):
            value = None if self.cur.kind in ("SEP", "EOF", "RBRACE") else self.expr()
            return Node("return", (value,), t.line)
        if self.accept("BREAK"):
            return Node("break", (), t.line)
        if self.accept("CONTINUE"):
            return Node("continue", (), t.line)
        target = self.expr()
        if self.accept("ASSIGN"):
            if target.kind not in ("name", "index", "member"):
                raise UsagiError("대입 대상이 유효하지 않아요.", t.line, t.column)
            return Node("set", (target, self.expr()), t.line)
        return Node("expr_stmt", (target,), t.line)

    def expr(self) -> Node:
        return self.or_expr()

    def or_expr(self) -> Node:
        node = self.and_expr()
        while self.cur.kind == "OR":
            t = self.take()
            node = Node("binary", (t.kind, node, self.and_expr()), t.line)
        return node

    def and_expr(self) -> Node:
        node = self.equality()
        while self.cur.kind == "AND":
            t = self.take()
            node = Node("binary", (t.kind, node, self.equality()), t.line)
        return node

    def equality(self) -> Node:
        node = self.comparison()
        while self.cur.kind in ("EQ", "NE"):
            t = self.take()
            node = Node("binary", (t.kind, node, self.comparison()), t.line)
        return node

    def comparison(self) -> Node:
        node = self.term()
        while self.cur.kind in ("LT", "LE", "GT", "GE"):
            t = self.take()
            node = Node("binary", (t.kind, node, self.term()), t.line)
        return node

    def term(self) -> Node:
        node = self.factor()
        while self.cur.kind in ("PLUS", "MINUS"):
            t = self.take()
            node = Node("binary", (t.kind, node, self.factor()), t.line)
        return node

    def factor(self) -> Node:
        node = self.unary()
        while self.cur.kind in ("STAR", "SLASH", "PERCENT"):
            t = self.take()
            node = Node("binary", (t.kind, node, self.unary()), t.line)
        return node

    def unary(self) -> Node:
        if self.cur.kind in ("MINUS", "NOT"):
            t = self.take()
            return Node("unary", (t.kind, self.unary()), t.line)
        return self.postfix()

    def postfix(self) -> Node:
        node = self.primary()
        while self.cur.kind in ("LPAREN", "LBRACKET", "DOT"):
            t = self.take()
            if t.kind == "LPAREN":
                args: list[Node] = []
                if self.cur.kind != "RPAREN":
                    args.append(self.expr())
                    while self.accept("COMMA"):
                        args.append(self.expr())
                self.take("RPAREN")
                node = Node("call", (node, args), t.line)
            elif t.kind == "LBRACKET":
                index = self.expr()
                self.take("RBRACKET")
                node = Node("index", (node, index), t.line)
            else:
                member = self.take("NAME").text
                node = Node("member", (node, member), t.line)
        return node

    def primary(self) -> Node:
        t = self.take()
        if t.kind in ("NUMBER", "STRING"):
            return Node("literal", (t.value,), t.line)
        if t.kind == "TRUE":
            return Node("literal", (True,), t.line)
        if t.kind == "FALSE":
            return Node("literal", (False,), t.line)
        if t.kind == "NONE":
            return Node("literal", (None,), t.line)
        if t.kind in ("NAME", "INPUT"):
            return Node("name", ("input" if t.kind == "INPUT" else t.text,), t.line)
        if t.kind == "LPAREN":
            node = self.expr()
            self.take("RPAREN")
            return node
        if t.kind == "LBRACKET":
            elems: list[Node] = []
            if self.cur.kind != "RBRACKET":
                elems.append(self.expr())
                while self.accept("COMMA"):
                    elems.append(self.expr())
            self.take("RBRACKET")
            return Node("list", (elems,), t.line)
        raise UsagiError(f"표현식이 와야 할 위치에 {t.text!r}가 있어요.", t.line, t.column)


class Environment:
    def __init__(self, parent: Environment | None = None,
                 source_path: Path | None = None):
        self.parent = parent
        self.source_path = source_path if source_path is not None else (
            parent.source_path if parent is not None else None
        )
        self.values: dict[str, Any] = {}

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def get(self, name: str, line: int) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.get(name, line)
        raise UsagiError(f"정의되지 않은 이름: {name}", line)

    def assign(self, name: str, value: Any, line: int) -> None:
        if name in self.values:
            self.values[name] = value
        elif self.parent is not None:
            self.parent.assign(name, value, line)
        else:
            raise UsagiError(f"선언되지 않은 변수: {name} (プルャ/푸루야로 선언하세요)", line)


@dataclass
class UserFunction:
    name: str
    params: list[str]
    body: list[Node]
    closure: Environment


@dataclass
class Builtin:
    name: str
    fn: Callable[..., Any]
    minimum: int
    maximum: int | None


@dataclass
class ModuleNamespace:
    path: Path
    environment: Environment


@dataclass
class StandardNamespace:
    name: str
    members: dict[str, Any]


@dataclass
class ClassValue:
    name: str
    methods: dict[str, UserFunction]


@dataclass
class InstanceValue:
    cls: ClassValue
    fields: dict[str, Any]


@dataclass
class BoundMethod:
    function: UserFunction
    receiver: InstanceValue


class ReturnFlow(Exception):
    def __init__(self, value: Any):
        self.value = value


class BreakFlow(Exception):
    pass


class ContinueFlow(Exception):
    pass


class Interpreter:
    def __init__(self, stdin: TextIO | None = None, stdout: TextIO | None = None,
                 max_steps: int = 100_000):
        self.stdin = stdin if stdin is not None else sys.stdin
        self.stdout = stdout if stdout is not None else sys.stdout
        self.max_steps = max_steps
        self.steps = 0
        self.builtins = Environment()
        self.globals = Environment(self.builtins)
        self.module_cache: dict[Path, ModuleNamespace] = {}
        self.loading_modules: set[Path] = set()
        self.builtins.define("input", Builtin("input", self.read_input, 0, 1))
        self.builtins.define("len", Builtin("len", len, 1, 1))
        self.builtins.define("int", Builtin("int", int, 1, 1))
        self.builtins.define("float", Builtin("float", float, 1, 1))
        self.builtins.define("str", Builtin("str", self.stringify, 1, 1))
        self.builtins.define("range", Builtin("range", range, 1, 3))

    @staticmethod
    def stringify(value: Any) -> str:
        if value is True:
            return "ヤハ"
        if value is False:
            return "ウーラーヤハヤハ"
        if value is None:
            return "ナシ"
        if isinstance(value, list):
            return "[" + ", ".join(Interpreter.stringify(v) for v in value) + "]"
        return str(value)

    def read_input(self, prompt: Any = "") -> str:
        self.stdout.write(self.stringify(prompt))
        self.stdout.flush()
        answer = self.stdin.readline()
        if answer == "":
            raise UsagiError("입력 스트림이 종료됐어요.")
        return answer.rstrip("\r\n")

    def tick(self, line: int) -> None:
        self.steps += 1
        if self.steps > self.max_steps:
            raise UsagiError(f"명령 실행 한도({self.max_steps}회)를 넘었어요. 무한 반복인지 확인하세요.", line)

    def run(self, source: str, source_path: str | Path | None = None) -> None:
        self.globals.source_path = Path(source_path).resolve() if source_path is not None else None
        program = Parser(tokenize(source)).parse()
        try:
            self.exec_block(program, self.globals)
        except ReturnFlow:
            raise UsagiError("함수 밖에서는 ウラララ/우라라라를 사용할 수 없어요.") from None
        except BreakFlow:
            raise UsagiError("반복문 밖에서는 サクッ/사쿠를 사용할 수 없어요.") from None
        except ContinueFlow:
            raise UsagiError("반복문 밖에서는 プワッ/푸왓을 사용할 수 없어요.") from None

    def import_module(self, filename: str, env: Environment, line: int) -> ModuleNamespace:
        relative = Path(filename)
        if not filename or relative.is_absolute() or relative.suffix != ".usagi":
            raise UsagiError('import 경로는 상대 경로의 .usagi 파일이어야 해요.', line)
        base = env.source_path.parent if env.source_path is not None else Path.cwd()
        path = (base / relative).resolve()
        if path in self.loading_modules:
            raise UsagiError(f"순환 import가 발생했어요: {path}", line)
        if path in self.module_cache:
            return self.module_cache[path]

        try:
            source = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as ex:
            raise UsagiError(f"import 파일 오류 ({path}): {ex}", line) from None
        try:
            program = Parser(tokenize(source)).parse()
        except UsagiError as ex:
            location = f"{path}:{ex.line}" if ex.line else str(path)
            raise UsagiError(f"모듈 구문 오류 ({location}): {ex}", line) from None

        scope = Environment(self.builtins, source_path=path)
        self.loading_modules.add(path)
        try:
            self.exec_block(program, scope)
        except UsagiError as ex:
            location = f"{path}:{ex.line}" if ex.line else str(path)
            raise UsagiError(f"모듈 실행 오류 ({location}): {ex}", line) from None
        except (ReturnFlow, BreakFlow, ContinueFlow):
            raise UsagiError(f"모듈 최상위에는 return/break/continue를 사용할 수 없어요: {path}", line) from None
        finally:
            self.loading_modules.remove(path)

        module = ModuleNamespace(path, scope)
        self.module_cache[path] = module
        return module

    def exec_block(self, stmts: list[Node], env: Environment) -> None:
        for stmt in stmts:
            self.tick(stmt.line)
            self.execute(stmt, env)

    def execute(self, n: Node, env: Environment) -> None:
        k, a = n.kind, n.args
        if k == "import":
            alias = a[1] if a[1] is not None else Path(a[0]).stem
            if not alias.isidentifier() or alias in KEYWORDS:
                raise UsagiError("모듈 이름이 유효하지 않아요. as/별칭/として로 이름을 지정하세요.", n.line)
            env.define(alias, self.import_module(a[0], env, n.line))
        elif k == "let":
            env.define(a[0], self.evaluate(a[1], env))
        elif k == "assign":
            env.assign(a[0], self.evaluate(a[1], env), n.line)
        elif k == "print":
            print(*(self.stringify(self.evaluate(e, env)) for e in a[0]), file=self.stdout)
        elif k == "expr_stmt":
            self.evaluate(a[0], env)
        elif k == "if":
            self.exec_block(a[1] if self.evaluate(a[0], env) else a[2], env)
        elif k == "while":
            while self.evaluate(a[0], env):
                self.tick(n.line)  # 빈 본문이라도 실행 횟수를 제한한다.
                try:
                    self.exec_block(a[1], env)
                except ContinueFlow:
                    continue
                except BreakFlow:
                    break
        elif k == "for":
            values = self.evaluate(a[1], env)
            try:
                iterator = iter(values)
            except TypeError:
                raise UsagiError("반복할 수 없는 값이에요. 리스트/문자열/range를 사용하세요.", n.line) from None
            env.define(a[0], None)
            for item in iterator:
                self.tick(n.line)
                env.assign(a[0], item, n.line)
                try:
                    self.exec_block(a[2], env)
                except ContinueFlow:
                    continue
                except BreakFlow:
                    break
        elif k == "func":
            env.define(a[0], UserFunction(a[0], a[1], a[2], env))
        elif k == "return":
            raise ReturnFlow(self.evaluate(a[0], env) if a[0] is not None else None)
        elif k == "break":
            raise BreakFlow()
        elif k == "continue":
            raise ContinueFlow()
        else:
            raise UsagiError(f"구현되지 않은 명령: {k}", n.line)

    def evaluate(self, n: Node, env: Environment) -> Any:
        k, a = n.kind, n.args
        if k == "literal":
            return a[0]
        if k == "name":
            return env.get(a[0], n.line)
        if k == "member":
            module = self.evaluate(a[0], env)
            if not isinstance(module, ModuleNamespace):
                raise UsagiError("점(.) 접근은 import한 모듈에서만 사용할 수 있어요.", n.line)
            if a[1] not in module.environment.values:
                raise UsagiError(f"모듈 {module.path.name}에 정의되지 않은 이름: {a[1]}", n.line)
            return module.environment.values[a[1]]
        if k == "list":
            return [self.evaluate(e, env) for e in a[0]]
        if k == "unary":
            value = self.evaluate(a[1], env)
            try:
                return -value if a[0] == "MINUS" else not value
            except (TypeError, ValueError) as ex:
                raise UsagiError(str(ex), n.line) from None
        if k == "binary":
            op, left_node, right_node = a
            left = self.evaluate(left_node, env)
            if op == "AND":
                return bool(left) and bool(self.evaluate(right_node, env))
            if op == "OR":
                return bool(left) or bool(self.evaluate(right_node, env))
            right = self.evaluate(right_node, env)
            operations = {
                "PLUS": lambda x, y: x + y, "MINUS": lambda x, y: x - y,
                "STAR": lambda x, y: x * y, "SLASH": lambda x, y: x / y,
                "PERCENT": lambda x, y: x % y, "EQ": lambda x, y: x == y,
                "NE": lambda x, y: x != y, "LT": lambda x, y: x < y,
                "LE": lambda x, y: x <= y, "GT": lambda x, y: x > y,
                "GE": lambda x, y: x >= y,
            }
            try:
                return operations[op](left, right)
            except (TypeError, ValueError, ZeroDivisionError, OverflowError) as ex:
                raise UsagiError(f"연산 오류: {ex}", n.line) from None
        if k == "index":
            target = self.evaluate(a[0], env)
            index = self.evaluate(a[1], env)
            try:
                return target[index]
            except (TypeError, IndexError, KeyError) as ex:
                raise UsagiError(f"인덱스 오류: {ex}", n.line) from None
        if k == "call":
            fn = self.evaluate(a[0], env)
            args = [self.evaluate(x, env) for x in a[1]]
            if isinstance(fn, Builtin):
                if len(args) < fn.minimum or (fn.maximum is not None and len(args) > fn.maximum):
                    raise UsagiError(f"{fn.name}() 인자 수가 잘못됐어요: {len(args)}개", n.line)
                try:
                    return fn.fn(*args)
                except UsagiError:
                    raise
                except (TypeError, ValueError, OverflowError) as ex:
                    raise UsagiError(f"{fn.name}() 호출 오류: {ex}", n.line) from None
            if isinstance(fn, UserFunction):
                if len(args) != len(fn.params):
                    raise UsagiError(f"{fn.name}()는 인자 {len(fn.params)}개가 필요해요.", n.line)
                local = Environment(fn.closure)
                for name, value in zip(fn.params, args):
                    local.define(name, value)
                try:
                    self.exec_block(fn.body, local)
                except ReturnFlow as ret:
                    return ret.value
                except (BreakFlow, ContinueFlow):
                    raise UsagiError("함수 안의 반복문 밖에서 사쿠/푸왓을 사용할 수 없어요.", n.line) from None
                return None
            raise UsagiError("호출할 수 있는 함수가 아니에요.", n.line)
        raise UsagiError(f"알 수 없는 식: {k}", n.line)


def main(argv: list[str] | None = None) -> int:
    cli = argparse.ArgumentParser(description="UsagiLang v0.1 인터프리터 🐰")
    cli.add_argument("file", nargs="?", help="실행할 .usagi 파일")
    cli.add_argument("-c", "--code", help="문자열로 입력한 UsagiLang 코드 실행")
    cli.add_argument("--max-steps", type=int, default=100_000, help="실행 명령 상한(기본 100000)")
    args = cli.parse_args(argv)
    if bool(args.file) == (args.code is not None):
        cli.error("파일 경로나 -c 코드 중 하나를 지정하세요.")
    if args.max_steps < 1:
        cli.error("--max-steps는 1 이상이어야 해요.")
    label = args.file or "<code>"
    try:
        src = Path(args.file).read_text(encoding="utf-8-sig") if args.file else args.code
        Interpreter(max_steps=args.max_steps).run(src, source_path=args.file)
        return 0
    except (OSError, UnicodeError) as ex:
        print(f"파일 오류: {ex}", file=sys.stderr)
    except UsagiError as ex:
        where = f"{label}:{ex.line}" + (f":{ex.column}" if ex.column else "") if ex.line else label
        print(f"🐰 {where}: {ex}", file=sys.stderr)
    except RecursionError:
        print(f"🐰 {label}: 재귀 호출이 너무 깊어요.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())