# UsagiLang v0.3.0-alpha (development)

[🇯🇵 日本語版 README](README.ja.md) | English / 한국어

**An experimental programming language inspired by Usagi’s expressions from *Chiikawa*.**

日本語と한국어 키워드를 모두 지원하는 Python 기반 독립 인터프리터입니다.
This is an **unofficial fan-made programming language**. It is not affiliated with, endorsed by, or an official translation provided by the original creators or rights holders. All programming semantics are original conventions invented for this project. No official character art or audio is included.

## Hello, World!

```usagi
우라 "Hello, World!"
```

```bash
python usagilang.py -c '우라 "Hello, World!"'
# Hello, World!
```

**Features:** Japanese/Korean keywords · variables · mutable lists · classes · exceptions · import · REPL · math/text/random/clock · offline package manager · VS Code extension source · no third-party runtime dependencies.

**Latest tagged release:** `v0.1.0-alpha` · **Development:** `v0.3.0-alpha` · **License:** MIT (original code and documentation only) · **Python:** 3.10+

- [v0.2 개발 기능 안내](docs/V02_FEATURES.md)
- [Language commands](COMMANDS.md)
- [Examples](examples)
- [Changelog](CHANGELOG.md)
- [How to contribute](CONTRIBUTING.md)
- [Publish instructions](PUBLISH.md)

---

## 한국어 사용 설명서

팬 제작 비공식 우사기어 프로그래밍 언어. Python 3.10 이상, 외부 패키지 불필요.
원작 대사의 뜻을 공식적으로 정의한 것이 아니라 **창작 프로그래밍 문법**입니다. 원작 권리자와 무관합니다.

## 바로 실행

아래 명령은 프로젝트 루트에서 실행합니다. `v0.3.0-alpha`는 개발판 기능이므로 공식 배포 버전과 다를 수 있습니다.

```bash
python -m pip install -e .
usagi run examples/v02.usagi
usagi check examples/v02.usagi
usagi repl
```

기존 `python usagilang.py examples/hello.usagi` 실행 방식도 유지됩니다.

```bash
python usagilang.py examples/hello.usagi
python usagilang.py examples/mixed.usagi
python usagilang.py examples/functions.usagi
python usagilang.py examples/lists.usagi
python usagilang.py examples/input.usagi
python usagilang.py -c 'ウラ "야하!"'
```

Windows에서는 환경에 따라 `python` 대신 `py`를 사용하세요.

## 명령어 사전

| 기능 | 일본어 | 한국어 별칭 |
|---|---|---|
| 변수 선언 | `プルャ` | `푸루야` |
| 화면 출력 | `ウラ` | `우라` |
| 입력 | `ハァヤハウラ` | `하아야하우라`, `하이야하우나` |
| 참 | `ヤハ` | `야하` |
| 거짓 | `ウーラーヤハヤハ` | `우라야하야하`, `우나야하야하` |
| 조건 | `ハァ` | `하아` |
| 그 외 | `フゥン` | `후웅` |
| 조건 반복 | `プルルルル` | `푸루루루루`, `푸루루루` |
| 순회 반복 | `ツツウラウラ` | `츠츠우라우라` |
| 함수 선언 | `ウララヤハ` | `우라라야하` |
| 반환 | `ウラララ` | `우라라라` |
| 반복 종료 | `サクッ` | `사쿠` |
| 다음 반복 | `プワッ` | `푸왓` |
| 순회 키워드 | `ウラウラ` | `우라우라` |
| 그리고 | `ウルウル` | `우루우루` |
| 또는 | `ヤハヤハ` | `야하야하` |
| 부정 | `イヤハ` | `이야하` |
| 값 없음 | `ナイナイ` | `나이나이` |
| 모듈 가져오기 | `ハイ` | `하이` |
| 모듈 이름 지정 | `ウララ` | `우라라` |

| 예외 처리 시작 | `プルップラッ` | `푸룻푸랏` |
| 예외 포착 | `ウギッ` | `우깃` |

v0.3부터 위 표기를 권장합니다. 기존 영어 및 한국어 별칭은 호환용으로 유지됩니다. `throw`와 `else` 명령어는 변경하지 않았습니다.

## 문법

- 파일 확장자 `.usagi`, UTF-8 저장. 명령어는 일본어/한국어 혼용 가능.
- 명령문 구분: 줄바꿈 또는 `;`. 블록은 `{ ... }`.
- 변수 선언: `푸루야 x = 10`, 변경: `x = x + 1`.
- 출력: `우라 "안녕", x` (공백으로 연결). 입력: `하이야하우나("질문: ")`.
- 자료형: 정수, 실수, 문자열, 참/거짓, 리스트, 없음.
- 연산: `+ - * / %`, 비교 `== != < <= > >=`, 논리 `ウルウル/ヤハヤハ/イヤハ` (구형 `and/or/not`도 지원).
- 리스트: `[1, 2, 3]`, 접근: `items[0]`; 문자열도 인덱싱 지원.
- 조건: `하아 x > 3 { 우라 "큼" } 후웅 { 우라 "작음" }`.
- 반복: `푸루루루 x < 5 { x = x + 1 }`, `츠츠우라우라 x 우라우라 [1,2,3] { 우라 x }`.
- 함수: `우라라야하 add(a,b) { 우라라라 a+b }` → `add(1,2)`.
- 내장 함수: `str(x)`, `int(x)`, `float(x)`, `len(x)`, `range(n)` / `range(start, stop[, step])`, `input(prompt)`.
- 주석: `# ...` 또는 `// ...`; 세미콜론 선택 가능.
- 출력 시 참/거짓은 각각 `ヤハ`/`ウーラーヤハヤハ`로 표시됨.
- 변수는 함수별 지역 환경과 상위 환경을 지원함. 블록 중괄호 자체는 새 지역 환경을 만들지 않음.

### 문법 예제

```usagi
プルャ count = 0
プルルルル count < 3 {
    ウラ "우라! " + str(count)
    count = count + 1
}
```

## 모듈 import

다른 `.usagi` 파일에서 함수와 변수를 가져올 수 있습니다. 모듈은 별도의 변수 공간을 가지며, **한 번 실행한 모듈은 같은 실행 중 다시 실행하지 않습니다.**

```usagi
# examples/imports.usagi
ハイ "modules/math.usagi" ウララ 数学
ウラ 数学.square(4)
우라 数学.pi
```

```bash
python usagilang.py examples/imports.usagi
```

- 문법: `import "경로.usagi" as 이름` / `가져와 "경로.usagi" 별칭 이름` / `インポート "경로.usagi" として 名前`.
- `as`를 생략하면 파일명에서 확장자를 뺀 이름을 사용합니다. 파일명이 변수 이름으로 적합하지 않으면 `as`를 지정하세요.
- 경로는 **import를 작성한 파일을 기준**으로 해석하며, `-c` 모드에서는 현재 작업 폴더를 기준으로 합니다. 상대 경로의 `.usagi` 파일만 지원합니다.
- 함수나 변수는 `모듈.함수()`, `모듈.변수`로 접근합니다. 일반 변수의 `.` 접근 및 모듈 멤버 직접 대입은 아직 지원하지 않습니다.
- 순환 import는 오류로 처리합니다. 모듈 실행도 동일한 `--max-steps` 한도를 공유합니다.
- import는 Python 모듈을 가져오지 않습니다. 로컬 패키지 참조 문법 `import "pkg:이름"`은 지원하지만 일반 파일 I/O는 제공하지 않습니다.

## v0.2 업데이트 🐰

**REPL:** `usagi repl` (여러 줄 입력 지원, `:help` / `:reset` / `:exit`).

**리스트 수정:** `items[0] = 42`, `items.append(3)`, `items.pop()`, `items.insert(0, 1)`.

**표준 라이브러리:** `math.sqrt(16)`, `math.pi`, `text.upper("hi")`, `random.randint(1, 6)`, `clock.now()`.

**클래스·객체:**

```usagi
クラス Counter {
    ウララヤハ init(self, value) { self.value = value }
    ウララヤハ next(self) {
        self.value = self.value + 1
        ウラララ self.value
    }
}
プルャ counter = Counter(4)
ウラ counter.next()
```

**예외 처리 (v0.3):**

```usagi
푸룻푸랏 {
    던지기 "야하!"
} 우깃 err {
    우라 err
}
```

**로컬 패키지 관리:** 원격 저장소에서 자동 설치하지 않고 개발자가 선택한 로컬 `.usagi` 파일만 복사합니다.

```bash
usagi pkg init
usagi pkg add helpers examples/modules/math.usagi
usagi pkg list
usagi pkg verify
usagi pkg remove helpers
```

코드에서는 `ハイ "pkg:helpers" ウララ helpers`로 가져옵니다. 패키지 관리자는 **실험적 로컬 단일 파일 방식**이며 외부 레지스트리·버전 해결·온라인 설치는 지원하지 않습니다.

**VS Code:** [소스 확장](vscode/usagilang) 제공. 구문 강조, 스니펫, 키워드 추천, Run/Check 명령. 아직 Marketplace에는 게시되지 않았습니다.

**오류 표시:** `ヤダ！` 테마, 오류 코드, 코드 줄 위치, 일부 해결 힌트. `--plain-errors`로 테마를 끌 수 있습니다.

자세한 문법과 제한은 [v0.2 안내](docs/V02_FEATURES.md)를 참조하세요.

## 테스트

```bash
python -m unittest discover -s tests -v
```

## 안전 및 현재 한계

- Python 코드를 `eval`/`exec`로 실행하지 않는 독립 파서 및 트리 탐색형 인터프리터.
- 반복 실행 횟수는 기본 100,000회 제한 (`--max-steps 5000`).
- v0.2 개발판은 객체·리스트 대입·로컬 단일 파일 패키지 기능을 지원하지만 일반 파일 I/O, 온라인 패키지 레지스트리, 상속, 정적 타입 검사, LSP, 임의 Python 모듈 가져오기는 지원하지 않습니다.
- 믿을 수 없는 코드를 시스템 수준으로 격리하는 보안 샌드박스는 아님. 재귀·메모리·출력 크기 제한은 완전하지 않음.