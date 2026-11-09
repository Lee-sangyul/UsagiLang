# UsagiLang v0.3.0-alpha（開発版）

[English / 한국어](README.md) | **日本語**

**『ちいかわ』のうさぎの表現から着想を得た、実験的なプログラミング言語です。**

UsagiLang は、日本語と韓国語のキーワードをどちらも使える、Python 製の独立したインタープリターです。外部パッケージは必要ありません。

> **非公式のファン制作プロジェクトです。**
> UsagiLang は原作者・権利者とは関係がなく、公認・監修・推奨されたものではありません。
> 原作のせりふを公式に翻訳したり、その意味を定義したりするものではありません。
> 各キーワードに割り当てたプログラミング上の意味は、このプロジェクト独自の創作・設計です。公式のキャラクター画像や音声は同梱していません。

## ✨ Hello, World!

```usagi
ウラ "Hello, World!"
```

```bash
python usagilang.py -c 'ウラ "Hello, World!"'
# Hello, World!
```

**主な機能：** 日本語・韓国語のキーワード別名、変数、リスト、条件分岐（if/else）、反復処理（while/for）、関数、再帰、モジュール読み込み、クラス、例外処理、REPL、標準ライブラリ、ローカルパッケージ管理、入出力。

| 項目 | 内容 |
|---|---|
| 最新リリース | `v0.1.0-alpha` |
| 開発中 | `v0.3.0-alpha` |
| 動作環境 | Python 3.10 以上 |
| 外部依存 | なし |
| ライセンス | MIT（独自に作成したコード・ドキュメントのみ） |
| ソースコード | [GitHub リポジトリ](https://github.com/Lee-sangyul/UsagiLang) |

## 🚀 はじめかた

1. Python 3.10 以降をインストールします。
2. このリポジトリを取得し、プロジェクトのディレクトリに移動します。

```bash
git clone https://github.com/Lee-sangyul/UsagiLang.git
cd UsagiLang
```

3. サンプルを実行します。

```bash
python usagilang.py examples/hello.usagi
python usagilang.py examples/mixed.usagi
python usagilang.py examples/functions.usagi
python usagilang.py examples/lists.usagi
python usagilang.py examples/input.usagi
```

`-c` を指定すると、ファイルを作成せずにコードを直接実行できます。

```bash
python usagilang.py -c 'ウラ "ヤハ！"'
```

Windows では環境によって `python` の代わりに `py` を使用してください。コマンドの引用符の扱いはシェルにより異なる場合があります。

## v0.3 の始め方

```bash
python -m pip install -e .
usagi run examples/v02.usagi
usagi check examples/v02.usagi
usagi repl
```

REPL は複数行入力に対応し、`:help` / `:reset` / `:exit` が使えます。
古い起動方法 `python usagilang.py examples/hello.usagi` もそのまま利用できます。

## 📖 コマンド一覧

日本語と韓国語の表記は同じ機能を持ち、1つのファイル内で混在させられます。
英語が分かる方にも使いやすいよう、各コマンドに英語名と短い英語の説明を追加しました。

| 機能 | 日本語キーワード | 韓国語の別名 | English | Short description (EN) |
|---|---|---|---|---|
| 変数宣言 | `プルャ` | `푸루야` | Variable declaration | Declare a new variable. |
| 出力 | `ウラ` | `우라` | Output | Print one or more values. |
| 入力 | `ハァヤハウラ` | `하아야하우라`, `하이야하우나` | Input | Read a line of user input. |
| 真（true） | `ヤハ` | `야하` | True | Boolean true value. |
| 偽（false） | `ウーラーヤハヤハ` | `우라야하야하`, `우나야하야하` | False | Boolean false value. |
| 条件分岐 | `ハァ` | `하아` | If | Run code when a condition is true. |
| else | `フゥン` | `후웅` | Else | Run code when the if condition is false. |
| while ループ | `プルルルル` | `푸루루루루`, `푸루루루` | While | Repeat while a condition is true. |
| for ループ | `ツツウラウラ` | `츠츠우라우라` | For | Iterate over items in a sequence. |
| 関数宣言 | `ウララヤハ` | `우라라야하` | Function | Define a function. |
| return | `ウラララ` | `우라라라` | Return | Return a value from a function. |
| break | `サクッ` | `사쿠` | Break | Exit the current loop. |
| continue | `プワッ` | `푸왓` | Continue | Skip to the next loop iteration. |
| for の in | `ウラウラ` | `우라우라` | In | Specify a sequence to iterate over. |
| 論理 AND | `ウルウル` | `우루우루` | Logical AND | True when both conditions are true. |
| 論理 OR | `ヤハヤハ` | `야하야하` | Logical OR | True when at least one condition is true. |
| 論理 NOT | `イヤハ` | `이야하` | Logical NOT | Reverse a boolean condition. |
| 値なし | `ナイナイ` | `나이나이` | None | Represent the absence of a value. |
| モジュールの読み込み | `ハイ` | `하이` | Import | Load a local UsagiLang module. |
| 別名指定 | `ウララ` | `우라라` | Alias | Give an imported module a name. |
| クラス宣言 | `class`, `クラス` | `클래스` | Class | Define a class. |
| try | `プルップラッ` | `푸룻푸랏` | Try | Start a block that may raise an error. |
| catch | `ウギッ` | `우깃` | Catch | Handle a raised language error. |
| throw | `throw`, `なげる` | `던지기` | Throw | Raise a language error. |

※ **English / Short description (EN)** はコマンドの意味を説明するためのものです。英語名がすべて新しい構文として使えるという意味ではありません。

**v0.3 で追加した表記が推奨構文です。** `in`、`and`、`or`、`not`、`ナシ`、`import`、`as`、`try`、`catch` などの旧表記と韓国語・日本語の既存別名も引き続き利用できます。`フゥン`（else）と `throw` / `なげる` は変更していません。値なしを出力すると `ナイナイ` と表示されます。

※ キーワードの役割は原作中の発言の公式な意味を表すものではありません。詳細な仕様は [COMMANDS.md](COMMANDS.md)（韓国語）を参照してください。

## 📝 基本文法

- ファイルの拡張子は `.usagi`、文字コードは UTF-8 です。
- 文は改行または `;` で区切り、ブロックは `{ ... }` で囲みます。
- 変数宣言：`プルャ x = 10`
- 変数の再代入：`x = x + 1`
- 出力：`ウラ "こんにちは", x`（複数の値は空白で区切って表示）
- 入力：`ハァヤハウラ("名前: ")`
- 型：整数、浮動小数点数、文字列、真偽値、リスト、値なし
- 算術演算：`+ - * / %`
- 比較演算：`== != < <= > >=`
- 論理演算：`ウルウル / ヤハヤハ / イヤハ`（旧 `and / or / not` も互換対応）
- リスト：`[1, 2, 3]`、要素の参照：`items[0]`
- 文字列もインデックスで参照できます。
- コメント：`# ...` または `// ...`
- 真偽値を出力すると、真は `ヤハ`、偽は `ウーラーヤハヤハ` と表示されます。
- 関数にはローカル環境と親環境があります。波括弧のブロック自体は新しいローカル環境を作りません。

### 1. 変数と出力

```usagi
プルャ name = "うさぎ"
ウラ "こんにちは、", name
```

### 2. 条件分岐（if / else）

```usagi
プルャ x = 5
ハァ x > 3 {
    ウラ "3より大きい"
} フゥン {
    ウラ "3以下"
}
```

### 3. 繰り返し（while）

```usagi
プルャ count = 0
プルルルル count < 3 {
    ウラ "ウラ！ " + str(count)
    count = count + 1
}
```

### 4. 反復処理（for）

```usagi
ツツウラウラ n ウラウラ range(1, 6) {
    ハァ n == 2 { プワッ }
    ハァ n == 5 { サクッ }
    ウラ n
}
```

### 5. 関数と戻り値

```usagi
ウララヤハ add(a, b) {
    ウラララ a + b
}
ウラ add(4, 5)
```

### 6. 日本語と韓国語の混在

```usagi
푸루야 message = "야하!"
ウラ message
```

## 🔧 組み込み関数

- `str(x)`、`int(x)`、`float(x)`、`len(x)`
- `range(n)`、`range(start, stop[, step])`
- `input(prompt)`

## 📦 モジュールの import

別の `.usagi` ファイルにある変数や関数を、名前空間を通して使えます。

```usagi
# examples/imports.usagi
ハイ "modules/math.usagi" ウララ 数学
ウラ 数学.square(4)
우라 数学.pi
```

```bash
python usagilang.py examples/imports.usagi
```

- 推奨構文：`ハイ "file.usagi" ウララ 名前` / `하이 "file.usagi" 우라라 이름`。旧構文 `import "file.usagi" as name` も引き続き動作します。
- `as` を省略すると、拡張子を除いたファイル名がモジュール名になります。名前が識別子として使えない場合は別名を指定してください。
- パスは読み込み元の `.usagi` ファイルからの相対パスです。 `-c` の場合はカレントディレクトリから探します。絶対パスや `.usagi` 以外のファイルは対象外です。
- `module.function()` や `module.variable` の形でアクセスします。モジュールの変数と呼び出し元の変数は分離されます。
- 同じファイルは1回の実行中に1回だけ評価され、循環 import はエラーになります。`--max-steps` は読み込み先にも適用されます。
- Python モジュールの読み込み、汎用ファイル入出力、Python パッケージの読み込み、一般的なファイル I/O、モジュールのメンバーへの直接代入は未対応です。

## v0.2 で追加された機能（v0.3 でも利用可能）

**リストの変更**：`items[0] = 10`、`items.append(3)`、`items.pop()`、`items.insert(0, 7)`。

**標準ライブラリ**：`math.sqrt(16)`、`math.pi`、`text.upper("hi")`、`random.randint(1, 6)`、`clock.now()`。

**クラス・オブジェクト**：

```usagi
クラス Counter {
    ウララヤハ init(self, value) { self.value = value }
    ウララヤハ next(self) {
        self.value = self.value + 1
        ウラララ self.value
    }
}
プルャ c = Counter(4)
ウラ c.next()
```

**例外処理**：

```usagi
プルップラッ {
    なげる "ヤハ！"
} ウギッ error {
    ウラ error
}
```

**ローカルパッケージ管理**：ネットワークからコードを自動取得せず、選択した `.usagi` ファイルのみプロジェクト内へコピーします。

```bash
usagi pkg init
usagi pkg add helpers examples/modules/math.usagi
usagi pkg list
usagi pkg verify
usagi pkg remove helpers
```

`ハイ "pkg:helpers" ウララ helpers` で読み込めます（旧 `import ... as ...` も利用可能）。オンラインレジストリや依存関係の自動解決はありません。

**VS Code：** [ソースコードのみの拡張機能](vscode/usagilang)。構文強調、スニペット、キーワード補完、実行／構文チェックを提供します。Marketplace 未公開です。

**エラー表示：** `ヤダ！` テーマ、エラーコード、発生行、場合によっては対処のヒントを表示します。`--plain-errors` でテーマを無効化できます。

新構文の詳細：[v0.3 機能ガイド（日本語）](docs/V03_FEATURES.ja.md)。旧機能の詳細：[v0.2 機能ガイド（日本語）](docs/V02_FEATURES.ja.md)。

## 🧪 テスト

```bash
python -m unittest discover -s tests -v
```

## ⚠️ 安全性と現在の制限

- Python の `eval` / `exec` でユーザーのコードを実行する方式ではなく、独自のパーサーと構文木をたどるインタープリターを使用します。
- 実行ステップ数はデフォルトで 100,000 に制限されます。例：`--max-steps 5000`
- 汎用ファイル入出力、オンラインパッケージレジストリ、クラス継承、静的型検査、LSP などは未実装です。
- **信頼できないコードを OS レベルで隔離するセキュリティサンドボックスではありません。** 再帰の深さ、メモリ使用量、出力サイズの制限は完全ではありません。
- `v0.3.0-alpha` は開発中の実験的なバージョンのため、仕様や動作は今後変更される可能性があります。

## 🤝 関連ドキュメント・貢献

- [コマンド仕様（韓国語）](COMMANDS.md)
- [サンプルコード](examples)
- [変更履歴](CHANGELOG.md)
- [貢献ガイド](CONTRIBUTING.md)
- [公開手順](PUBLISH.md)

バグ報告、改善提案、翻訳への協力は、リポジトリの Issue や Pull Request から歓迎します。

---

**UsagiLang は『ちいかわ』の非公式ファンプロジェクトです。原作のキャラクターや作品に関する権利を主張するものではありません。**
