# 🐰 UsagiLang v0.2.0-alpha 개발 기능

이 문서는 개발 중인 `v0.2` 기능에 대한 안내입니다. 기존 `v0.1.0-alpha` 공개 태그와 구별해 주세요.

## 1. CLI와 REPL

```bash
python -m pip install -e .
usagi run examples/v02.usagi
usagi check examples/v02.usagi
usagi repl
usagi run -c 'ウラ "ヤハ！"'
usagi run examples/v02.usagi --max-steps 5000
usagi run examples/v02.usagi --plain-errors
```

`check`는 구문 분석만 수행하고 코드를 실행하지 않습니다. REPL의 `:help`, `:reset`, `:exit`는 환경 도움말·초기화·종료이며, 중괄호가 닫힐 때까지 여러 줄을 입력할 수 있습니다.

## 2. 리스트 수정

```usagi
プルャ xs=[1,2]
xs[0]=3
xs.append(4)
xs.insert(1,9)
ウラ xs
ウラ xs.pop()
```

`append(xs, value)`와 `pop(xs[, index])` 내장 함수도 있습니다. 인덱스 범위를 벗어나면 오류가 발생합니다. 문자열은 수정할 수 없습니다.

## 3. 표준 라이브러리

| 분류 | 기능 |
|---|---|
| 숫자 | `abs`, `round`, `sum`, `min`, `max` |
| 수학 | `math.sqrt`, `math.floor`, `math.ceil`, `math.pow`, `math.pi` |
| 문자열 | `text.upper`, `text.lower`, `text.split`, `text.join` |
| 랜덤 | `random.randint`, `random.choice` |
| 시간 | `clock.now` (Unix timestamp 초 단위) |

`math`, `text`, `random`, `clock`는 자동으로 사용 가능한 표준 네임스페이스입니다. 파일 I/O, 네트워크, 임의 Python 라이브러리 가져오기는 제공하지 않습니다.

## 4. 클래스와 객체

```usagi
クラス Counter {
    ウララヤハ init(self, start) { self.n=start }
    ウララヤハ next(self) {
        self.n=self.n+1
        ウラララ self.n
    }
}
プルャ c=Counter(2)
ウラ c.next()
```

`init(self, ...)`는 선택적인 초기화 메서드입니다. 인스턴스 필드는 `self.n = ...`처럼 추가·수정하고, 메서드는 호출할 때 `self`를 자동으로 전달합니다. 클래스 상속, 정적 메서드, 비공개 멤버 검사는 아직 지원하지 않습니다.

## 5. 예외 처리

```usagi
ためす {
    なげる "예외 예제"
} つかまえる error {
    ウラ error
}
```

일본어·한국어·영어 별칭:

| 기능 | 일본어 | 한국어 | 영어 |
|---|---|---|---|
| 클래스 | `クラス` | `클래스` | `class` |
| 예외 시도 | `ためす` | `시도` | `try` |
| 예외 처리 | `つかまえる` | `잡기` | `catch` |
| 예외 발생 | `なげる` | `던지기` | `throw` |

`catch`는 UsagiLang 실행 오류를 문자열로 받으며, 모든 Python 예외를 무조건 포착하는 기능은 아닙니다.

## 6. 오류 메시지

기본적으로 `🐰 ヤダ！ [E100] 파일명:줄:열` 형식으로 표시하며, 소스 줄과 위치 및 일부 해결 힌트를 보여 줍니다. 파일·패키지 오류나 재귀 한계는 별도 코드로 표시합니다. `--plain-errors`는 우사기 테마를 숨깁니다.

## 7. 로컬 패키지 관리자 (실험적)

```bash
usagi pkg init
usagi pkg add mymath examples/modules/math.usagi
usagi pkg list
usagi pkg verify
usagi pkg remove mymath
```

`pkg init`은 프로젝트 루트에 `usagi-packages.json`을 생성합니다. `pkg add`는 **현재 프로젝트 내부의 선택한 `.usagi` 파일**을 `.usagi/packages/`로 복사하고 매니페스트에 등록합니다. 다른 프로젝트·외부 서버에서 다운로드하지 않습니다.

```usagi
import "pkg:mymath" as mymath
ウラ mymath.square(6)
```

현재 단일 파일 로컬 설치만 지원합니다. 버전 잠금, 무결성 서명, 패키지 간 의존성 처리, 원격 레지스트리, 자동 업데이트는 없습니다. **신뢰할 수 없는 코드를 설치하거나 실행하지 마세요.**

## 8. VS Code 지원

`vscode/usagilang`에 개발용 확장 소스를 제공합니다. `.usagi` 구문 강조, 괄호 쌍, 스니펫, 키워드 완성, Run/Check 명령을 지원합니다. 아직 Marketplace에 공개되지 않았고, 디버거·LSP·정적 타입 자동완성은 없습니다.

## 9. 테스트 및 제한

```bash
python -m unittest discover -s tests -v
python usagilang.py examples/v02.usagi
```

이 인터프리터는 **보안 샌드박스가 아닙니다**. 재귀·메모리·출력 크기의 완전한 제한, 신뢰할 수 없는 파일의 안전 실행, 온라인 의존성 설치, Python 패키지 import 등은 지원하지 않습니다.

원작 표현은 영감을 준 요소이며, 명령어의 기능은 프로젝트가 창작한 것입니다. 원작 권리자와 무관한 비공식 팬 프로젝트입니다.
