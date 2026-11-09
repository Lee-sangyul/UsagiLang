#!/usr/bin/env python3
"""UsagiLang v0.3 — 비공식 우사기어 기반 교육용 인터프리터 (Python 3.10+).

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
    "func": "FUNC", "return": "RETURN",
    "ウラウラ": "IN", "우라우라": "IN",
    "in": "IN", "안에": "IN",
    "ウルウル": "AND", "우루우루": "AND",
    "and": "AND", "그리고": "AND",
    "ヤハヤハ": "OR", "야하야하": "OR",
    "or": "OR", "또는": "OR",
    "イヤハ": "NOT", "이야하": "NOT",
    "not": "NOT", "아님": "NOT",
    "ナイナイ": "NONE", "나이나이": "NONE",
    "ナシ": "NONE", "없음": "NONE", "null": "NONE",
    "ハイ": "IMPORT", "하이": "IMPORT",
    "import": "IMPORT", "가져와": "IMPORT", "インポート": "IMPORT",
    "ウララ": "AS", "우라라": "AS",
    "as": "AS", "별칭": "AS", "として": "AS",
    "class": "CLASS", "클래스": "CLASS", "クラス": "CLASS",
    "プルップラッ": "TRY", "푸룻푸랏": "TRY",
    "try": "TRY", "시도": "TRY", "ためす": "TRY",
    "ウギッ": "CATCH", "우깃": "CATCH",
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
        self.builtins.define("abs", Builtin("abs", abs, 1, 1))
        self.builtins.define("round", Builtin("round", round, 1, 2))
        self.builtins.define("sum", Builtin("sum", sum, 1, 1))
        self.builtins.define("min", Builtin("min", min, 1, None))
        self.builtins.define("max", Builtin("max", max, 1, None))
        self.builtins.define("append", Builtin("append", self.list_append, 2, 2))
        self.builtins.define("pop", Builtin("pop", self.list_pop, 1, 2))
        self.builtins.define("math", StandardNamespace("math", {
            "sqrt": Builtin("math.sqrt", pymath.sqrt, 1, 1),
            "floor": Builtin("math.floor", pymath.floor, 1, 1),
            "ceil": Builtin("math.ceil", pymath.ceil, 1, 1),
            "pow": Builtin("math.pow", pymath.pow, 2, 2),
            "pi": pymath.pi,
        }))
        self.builtins.define("text", StandardNamespace("text", {
            "upper": Builtin("text.upper", self.text_upper, 1, 1),
            "lower": Builtin("text.lower", self.text_lower, 1, 1),
            "split": Builtin("text.split", self.text_split, 1, 2),
            "join": Builtin("text.join", self.text_join, 2, 2),
        }))
        self.builtins.define("random", StandardNamespace("random", {
            "randint": Builtin("random.randint", pyrandom.randint, 2, 2),
            "choice": Builtin("random.choice", pyrandom.choice, 1, 1),
        }))
        self.builtins.define("clock", StandardNamespace("clock", {
            "now": Builtin("clock.now", time.time, 0, 0),
        }))

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
        if isinstance(value, InstanceValue):
            return f"<{value.cls.name} instance>"
        return str(value)

    @staticmethod
    def list_append(items: Any, value: Any) -> None:
        if not isinstance(items, list):
            raise UsagiError("append() 첫 번째 인자는 리스트여야 해요.")
        items.append(value)

    @staticmethod
    def list_pop(items: Any, index: int = -1) -> Any:
        if not isinstance(items, list):
            raise UsagiError("pop() 첫 번째 인자는 리스트여야 해요.")
        return items.pop(index)

    @staticmethod
    def text_upper(value: str) -> str:
        return value.upper()

    @staticmethod
    def text_lower(value: str) -> str:
        return value.lower()

    @staticmethod
    def text_split(value: str, separator: str | None = None) -> list[str]:
        return value.split(separator)

    @staticmethod
    def text_join(separator: str, values: list[str]) -> str:
        return separator.join(values)

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
        if filename.startswith("pkg:"):
            from usagi_packages import PackageError, resolve
            try:
                path = resolve(filename[4:], env.source_path)
            except PackageError as ex:
                raise UsagiError(f"패키지 가져오기 실패: {ex}", line) from None
        else:
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

    def call_value(self, fn: Any, args: list[Any], line: int) -> Any:
        if isinstance(fn, BoundMethod):
            return self.call_value(fn.function, [fn.receiver, *args], line)
        if isinstance(fn, ClassValue):
            instance = InstanceValue(fn, {})
            if "init" in fn.methods:
                self.call_value(BoundMethod(fn.methods["init"], instance), args, line)
            elif args:
                raise UsagiError(f"{fn.name}()은 생성자 인자를 받지 않아요.", line)
            return instance
        if isinstance(fn, Builtin):
            if len(args) < fn.minimum or (fn.maximum is not None and len(args) > fn.maximum):
                raise UsagiError(f"{fn.name}() 인자 수가 잘못됐어요: {len(args)}개", line)
            try:
                return fn.fn(*args)
            except UsagiError:
                raise
            except (TypeError, ValueError, OverflowError, IndexError, KeyError) as ex:
                raise UsagiError(f"{fn.name}() 호출 오류: {ex}", line) from None
        if isinstance(fn, UserFunction):
            if len(args) != len(fn.params):
                raise UsagiError(f"{fn.name}()는 인자 {len(fn.params)}개가 필요해요.", line)
            local = Environment(fn.closure)
            for name, value in zip(fn.params, args):
                local.define(name, value)
            try:
                self.exec_block(fn.body, local)
            except ReturnFlow as ret:
                return ret.value
            except (BreakFlow, ContinueFlow):
                raise UsagiError("함수의 반복문 밖에서 break/continue를 사용할 수 없어요.", line) from None
            return None
        raise UsagiError("호출할 수 있는 함수 또는 클래스가 아니에요.", line)

    def read_member(self, target: Any, name: str, line: int) -> Any:
        if isinstance(target, ModuleNamespace):
            if name not in target.environment.values:
                raise UsagiError(f"모듈 {target.path.name}에 정의되지 않은 이름: {name}", line)
            return target.environment.values[name]
        if isinstance(target, StandardNamespace):
            if name not in target.members:
                raise UsagiError(f"{target.name}에 없는 기능: {name}", line)
            return target.members[name]
        if isinstance(target, InstanceValue):
            if name in target.fields:
                return target.fields[name]
            if name in target.cls.methods:
                return BoundMethod(target.cls.methods[name], target)
            raise UsagiError(f"{target.cls.name}에 없는 속성: {name}", line)
        if isinstance(target, list):
            methods = {
                "append": Builtin("list.append", lambda value: self.list_append(target, value), 1, 1),
                "pop": Builtin("list.pop", lambda index=-1: self.list_pop(target, index), 0, 1),
                "insert": Builtin("list.insert", lambda index, value: target.insert(index, value), 2, 2),
            }
            if name in methods:
                return methods[name]
        raise UsagiError("해당 값에서는 점(.) 속성에 접근할 수 없어요.", line)

    def assign_target(self, target: Node, value: Any, env: Environment) -> None:
        if target.kind == "name":
            env.assign(target.args[0], value, target.line)
            return
        if target.kind == "index":
            obj = self.evaluate(target.args[0], env)
            index = self.evaluate(target.args[1], env)
            if not isinstance(obj, list):
                raise UsagiError("리스트 요소에만 대입할 수 있어요.", target.line)
            try:
                obj[index] = value
            except (TypeError, IndexError) as ex:
                raise UsagiError(f"리스트 대입 오류: {ex}", target.line) from None
            return
        if target.kind == "member":
            obj = self.evaluate(target.args[0], env)
            if not isinstance(obj, InstanceValue):
                raise UsagiError("인스턴스 필드에만 직접 대입할 수 있어요.", target.line)
            obj.fields[target.args[1]] = value
            return
        raise UsagiError("잘못된 대입 대상이에요.", target.line)

    def exec_block(self, stmts: list[Node], env: Environment) -> None:
        for stmt in stmts:
            self.tick(stmt.line)
            self.execute(stmt, env)

    def execute(self, n: Node, env: Environment) -> None:
        k, a = n.kind, n.args
        if k == "import":
            alias = a[1] if a[1] is not None else (
                a[0][4:] if a[0].startswith("pkg:") else Path(a[0]).stem
            )
            if not alias.isidentifier() or alias in KEYWORDS:
                raise UsagiError("모듈 이름이 유효하지 않아요. as/별칭/として로 이름을 지정하세요.", n.line)
            env.define(alias, self.import_module(a[0], env, n.line))
        elif k == "let":
            env.define(a[0], self.evaluate(a[1], env))
        elif k == "assign":
            env.assign(a[0], self.evaluate(a[1], env), n.line)
        elif k == "set":
            value = self.evaluate(a[1], env)
            self.assign_target(a[0], value, env)
        elif k == "class":
            methods = {method.args[0]: UserFunction(method.args[0], method.args[1],
                                                    method.args[2], env) for method in a[1]}
            env.define(a[0], ClassValue(a[0], methods))
        elif k == "throw":
            raise UsagiError(self.stringify(self.evaluate(a[0], env)), n.line, code="E300")
        elif k == "try":
            try:
                self.exec_block(a[0], env)
            except UsagiError as ex:
                handler = Environment(env)
                handler.define(a[1], str(ex))
                self.exec_block(a[2], handler)
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
            return self.read_member(self.evaluate(a[0], env), a[1], n.line)
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
            return self.call_value(fn, args, n.line)
        raise UsagiError(f"알 수 없는 식: {k}", n.line)


def diagnostic(error: UsagiError, source: str, label: str = "<code>",
               themed: bool = True) -> str:
    """User-friendly source diagnostics with stable error codes and line markers."""
    location = f"{label}:{error.line}" if error.line else label
    if error.column:
        location += f":{error.column}"
    message = f"{'🐰 ヤダ！ ' if themed else ''}[{error.code}] {location}: {error}"
    if error.line:
        lines = source.splitlines()
        if 1 <= error.line <= len(lines):
            excerpt = lines[error.line - 1]
            message += "\n  " + excerpt
            if error.column:
                message += "\n  " + (" " * (error.column - 1)) + "^"
    if "정의되지 않은 이름" in str(error):
        message += "\n💡 プルャ/푸루야로 변수를 먼저 선언하세요."
    return message


def incomplete_input(source: str) -> bool:
    """Detect unfinished blocks or parentheses to support multiline REPL."""
    try:
        tokens = tokenize(source)
    except UsagiError as exc:
        return "문자열이 닫히지 않았어요" in str(exc)
    depths = {"LBRACE": 0, "LPAREN": 0, "LBRACKET": 0}
    closes = {"RBRACE": "LBRACE", "RPAREN": "LPAREN", "RBRACKET": "LBRACKET"}
    for token in tokens:
        if token.kind in depths:
            depths[token.kind] += 1
        elif token.kind in closes:
            depths[closes[token.kind]] -= 1
    return any(n > 0 for n in depths.values())


def repl_loop(stdin: TextIO | None = None, stdout: TextIO | None = None,
              stderr: TextIO | None = None, max_steps: int = 100_000,
              themed: bool = True) -> int:
    reader = stdin if stdin is not None else sys.stdin
    writer = stdout if stdout is not None else sys.stdout
    errors = stderr if stderr is not None else sys.stderr
    runner = Interpreter(stdin=reader, stdout=writer, max_steps=max_steps)
    print("🐰 UsagiLang REPL v0.3 (:help, :reset, :exit)", file=writer)
    pending: list[str] = []
    while True:
        writer.write("... " if pending else ">>> ")
        writer.flush()
        line = reader.readline()
        if line == "":
            writer.write("\n")
            break
        stripped = line.strip()
        if not pending and stripped in (":quit", ":exit", ":q"):
            break
        if not pending and stripped == ":help":
            print(":help :reset :exit | Enter UsagiLang code", file=writer)
            continue
        if not pending and stripped == ":reset":
            runner = Interpreter(stdin=reader, stdout=writer, max_steps=max_steps)
            print("フゥン… 환경 초기화 완료", file=writer)
            continue
        if not pending and not stripped:
            continue
        pending.append(line)
        source = "".join(pending)
        if incomplete_input(source):
            continue
        try:
            runner.run(source)
        except UsagiError as ex:
            print(diagnostic(ex, source, "<repl>", themed), file=errors)
        except RecursionError:
            print("🐰 ヤダ！ [E900] 재귀 호출이 너무 깊어요.", file=errors)
        pending = []
    return 0


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] == "pkg":
        from usagi_packages import PackageError, command
        try:
            return command(arguments[1:], sys.stdout)
        except (PackageError, OSError, UnicodeError) as ex:
            print(f"🐰 ヤダ！ [E500] {ex}", file=sys.stderr)
            return 1

    command_name = arguments.pop(0) if arguments and arguments[0] in ("run", "check", "repl") else "run"
    cli = argparse.ArgumentParser(
        description="UsagiLang v0.3 (run / check / repl / pkg)"
    )
    if command_name != "repl":
        cli.add_argument("file", nargs="?", help="실행하거나 검사할 .usagi 파일")
        cli.add_argument("-c", "--code", help="직접 입력하는 UsagiLang 코드")
    cli.add_argument("--max-steps", type=int, default=100_000, help="실행 명령 상한")
    cli.add_argument("--plain-errors", action="store_true", help="우사기 테마 없이 오류 표시")
    args = cli.parse_args(arguments)
    if args.max_steps < 1:
        cli.error("--max-steps는 1 이상이어야 해요.")
    if command_name == "repl":
        return repl_loop(max_steps=args.max_steps, themed=not args.plain_errors)
    if bool(args.file) == (args.code is not None):
        cli.error("파일 경로나 -c 코드 중 하나를 지정하세요.")

    label = args.file or "<code>"
    source = ""
    try:
        source = Path(args.file).read_text(encoding="utf-8-sig") if args.file else args.code
        if command_name == "check":
            Parser(tokenize(source)).parse()
            print(f"🐰 문법 검사 통과: {label}")
            return 0
        Interpreter(max_steps=args.max_steps).run(source, source_path=args.file)
        return 0
    except (OSError, UnicodeError) as ex:
        print(f"🐰 ヤダ！ [E400] 파일 오류: {ex}", file=sys.stderr)
    except UsagiError as ex:
        print(diagnostic(ex, source, label, not args.plain_errors), file=sys.stderr)
    except RecursionError:
        print(f"🐰 ヤダ！ [E900] {label}: 재귀 호출이 너무 깊어요.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
