# UsagiLang v0.3 개발 명령어 명세

> **중요**: 원작 표현은 어휘 창작의 소재이며, 코드상의 기능은 이 프로젝트에서 새롭게 정의했습니다.

## 표기 규칙

- 공식 문법 표기는 일본어. 한국어 표기는 동등한 별칭으로 취급됩니다.
- 예: `プルャ a = 1`과 `푸루야 a = 1`은 같습니다.
- 한 파일, 심지어 한 줄에서 일본어와 한국어를 섞어도 됩니다.
- 변수/함수 이름은 유니코드 문자(한글 포함), 영문, 숫자(첫 글자는 숫자 불가), `_`를 사용합니다.
- `{ }`는 블록 구분자이고 `;` 또는 줄바꿈이 일반 문장의 구분자입니다.

## 키워드

| 토큰 | 일본어 | 한국어 | 역할 | English | Short description (EN) |
|---|---|---|---|---|---|
| LET | `プルャ` | `푸루야` | 새 변수 정의 | Variable declaration | Declare a new variable. |
| PRINT | `ウラ` | `우라` | 출력문 | Output | Print one or more values. |
| INPUT | `ハァヤハウラ` | `하아야하우라`, `하이야하우나` | 문자열 입력 함수 | Input | Read a line of user input. |
| TRUE | `ヤハ` | `야하` | 참 | True | Boolean true value. |
| FALSE | `ウーラーヤハヤハ` | `우라야하야하`, `우나야하야하` | 거짓 | False | Boolean false value. |
| IF | `ハァ` | `하아` | 조건식 | If | Run code when a condition is true. |
| ELSE | `フゥン` | `후웅` | 조건문의 반대 분기 | Else | Run code when the if condition is false. |
| WHILE | `プルルルル` | `푸루루루루`, `푸루루루` | 조건 반복 | While | Repeat while a condition is true. |
| FOR | `ツツウラウラ` | `츠츠우라우라` | 순회 반복 | For | Iterate over items in a sequence. |
| FUNC | `ウララヤハ` | `우라라야하` | 함수 선언 | Function | Define a function. |
| RETURN | `ウラララ` | `우라라라` | 함수 반환 | Return | Return a value from a function. |
| BREAK | `サクッ` | `사쿠` | 현재 반복 중지 | Break | Exit the current loop. |
| CONTINUE | `プワッ` | `푸왓` | 다음 반복으로 진행 | Continue | Skip to the next loop iteration. |
| IN | `ウラウラ` | `우라우라` | 순회 대상 지정 | In | Specify a sequence to iterate over. |
| AND | `ウルウル` | `우루우루` | 논리곱 | Logical AND | True when both conditions are true. |
| OR | `ヤハヤハ` | `야하야하` | 논리합 | Logical OR | True when at least one condition is true. |
| NOT | `イヤハ` | `이야하` | 논리 부정 | Logical NOT | Reverse a boolean condition. |
| NONE | `ナイナイ` | `나이나이` | 값 없음 | None | Represent the absence of a value. |
| IMPORT | `ハイ` | `하이` | 모듈 불러오기 | Import | Load a local UsagiLang module. |
| AS | `ウララ` | `우라라` | 모듈 이름 붙이기 | Alias | Give an imported module a name. |
| CLASS | `class`, `クラス` | `클래스` | 클래스 선언 | Class | Define a class. |
| TRY | `プルップラッ` | `푸룻푸랏` | 예외 처리 시작 | Try | Start a block that may raise an error. |
| CATCH | `ウギッ` | `우깃` | 예외 포착 | Catch | Handle a raised language error. |
| THROW | `throw`, `なげる` | `던지기` | 예외 발생 | Throw | Raise a language error. |

**참고:** 영어 열은 의미 설명이며, 모든 영어 이름이 실행 가능한 공식 키워드라는 뜻은 아닙니다.

기존 v0.2 명령어(`in`, `and`, `or`, `not`, `import`, `as`, `try`, `catch`, `ナシ` 및 기존 별칭)는 하위 호환을 위해 그대로 지원합니다. `フゥン`은 else로 유지하며 `throw`도 기존과 동일합니다.

## 예시 모음

### 변수와 출력

```usagi
푸루야 n = 42
우라 "n=", n
n = n + 1
우라 "new=", n
```

### if / else

```usagi
하아 n > 40 {
    우라 "큼"
} 후웅 {
    우라 "작음"
}
```

### while

```usagi
푸루야 count = 0
푸루루루 count < 3 {
    우라 count
    count = count + 1
}
```

### for / break / continue

```usagi
츠츠우라우라 n 우라우라 range(1, 6) {
    하아 n == 2 { 푸왓 }
    하아 n == 5 { 사쿠 }
    우라 n
}
```

### 함수

```usagi
우라라야하 add(a, b) {
    우라라라 a + b
}
우라 add(4, 5)
```

### 입력

```usagi
푸루야 who = 하이야하우나("이름: ")
우라 "안녕, " + who
```

## 모듈 가져오기

```usagi
# examples/imports.usagi
ハイ "modules/math.usagi" ウララ 数学
ウラ 数学.square(4)
```

- `ハイ "math.usagi"`이면 기본 이름은 `math`.
- `하이 "math.usagi" 우라라 계산`으로 이름을 바꿀 수 있음.
- 모듈은 독립적인 변수 공간을 가지며 `계산.add(2, 3)`처럼 점 표기법으로 접근.
- 현재 실행 중 같은 모듈은 한 번만 로드하고, 순환 import는 오류.
- 경로는 가져오기를 실행하는 코드의 파일을 기준으로 해석. `-c`는 작업 디렉터리 기준.
- 상대 경로 `.usagi` 파일만 허용. Python `import`와는 무관.
- 모듈 변수에 `math.pi = 3`처럼 직접 대입할 수 없음.

## v0.2: 클래스·리스트·예외 처리

```usagi
クラス Box {
    ウララヤハ init(self, number) { self.number=number }
}
プルャ b=Box(5)
プルャ xs=[1,2]
xs[0]=9
xs.append(b.number)
プルップラッ {
    なげる "ヤハ！"
} ウギッ e {
    ウラ e, xs
}
```

리스트: `items[0]=value`, `items.append(value)`, `items.pop()`, `items.insert(index,value)`.

표준 네임스페이스: `math` / `text` / `random` / `clock`.

로컬 패키지: `ハイ "pkg:이름" ウララ 별칭`. CLI는 `usagi pkg init`, `usagi pkg add NAME FILE`, `list`, `verify`, `remove` 사용.

[한국어 전체 v0.2 사용 가이드](docs/V02_FEATURES.md) · [日本語](docs/V02_FEATURES.ja.md)

## v0.3 논리 연산 예제

```usagi
プルャ value = ナイナイ
ハァ イヤハ (value == ナイナイ) ヤハヤハ (ヤハ ウルウル ヤハ) {
    ウラ "조건 성립"
}
```

## 연산자 우선순위 (높음 → 낮음)

1. 함수 호출 `()`, 인덱싱 `[]`, 멤버 접근 `.`
2. 단항 `-`, `!`, `not`, `아님`
3. 곱셈·나눗셈·나머지 `* / %`
4. 덧셈·뺄셈 `+ -`
5. 크기 비교 `< <= > >=`
6. 같음 비교 `== !=`
7. 논리 AND
8. 논리 OR

## 현재 v0.2 미구현

- 일반 파일 I/O, 온라인 패키지 레지스트리, 패키지 의존성 해결, 원격 패키지 설치
- 클래스 상속, 정적 타입 검사, 매크로, 바이트코드 컴파일, LSP, 디버거
- 완전한 다국어 오류 메시지 및 보안 샌드박스

## 언어 품질 관련 메모

- `ハァヤハウラ`는 이야기 속 사탕을 달라는 표현을 입력 요청 함수로 **창작적으로 응용**했습니다.
- `ヤハ`와 `ウーラーヤハヤハ`의 진리값 할당은 구현 편의를 위한 **언어 설계 결정**이지 공식 번역이 아닙니다.
- `ウラ`와 `ウラララ`처럼 앞 글자가 같은 명령은 토큰을 통째로 읽어 정확히 구분합니다.