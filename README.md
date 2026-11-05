# 🐰 UsagiLang v0.1.0-alpha

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

**Features:** Japanese and Korean keyword aliases · variables · lists · if/else · while/for · functions · recursion · input/output · no third-party dependencies.

**Release:** `v0.1.0-alpha` · **License:** MIT (original code and documentation only) · **Python:** 3.10+

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
| 순회 키워드 | `in` | `안에` |
| 그리고 | `and`, `&&` | `그리고` |
| 또는 | `or`, `||` | `또는` |
| 부정 | `not`, `!` | `아님` |
| 값 없음 | `ナシ`, `null` | `없음` |

## 문법

- 파일 확장자 `.usagi`, UTF-8 저장. 명령어는 일본어/한국어 혼용 가능.
- 명령문 구분: 줄바꿈 또는 `;`. 블록은 `{ ... }`.
- 변수 선언: `푸루야 x = 10`, 변경: `x = x + 1`.
- 출력: `우라 "안녕", x` (공백으로 연결). 입력: `하이야하우나("질문: ")`.
- 자료형: 정수, 실수, 문자열, 참/거짓, 리스트, 없음.
- 연산: `+ - * / %`, 비교 `== != < <= > >=`, 논리 `and/or/not` 또는 한국어 별칭.
- 리스트: `[1, 2, 3]`, 접근: `items[0]`; 문자열도 인덱싱 지원.
- 조건: `하아 x > 3 { 우라 "큼" } 후웅 { 우라 "작음" }`.
- 반복: `푸루루루 x < 5 { x = x + 1 }`, `츠츠우라우라 x 안에 [1,2,3] { 우라 x }`.
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

## 테스트

```bash
python -m unittest discover -s tests -v
```

## 안전 및 현재 한계

- Python 코드를 `eval`/`exec`로 실행하지 않는 독립 파서 및 트리 탐색형 인터프리터.
- 반복 실행 횟수는 기본 100,000회 제한 (`--max-steps 5000`).
- 실제 프로젝트 언어 v0.1이며 모듈 import, 파일 I/O, 객체, 대입형 리스트 수정, 패키지 관리 등은 미구현.
- 믿을 수 없는 코드를 시스템 수준으로 격리하는 보안 샌드박스는 아님. 재귀·메모리·출력 크기 제한은 완전하지 않음.