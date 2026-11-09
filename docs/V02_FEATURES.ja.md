# UsagiLang v0.2.0-alpha 機能ガイド（旧仕様）

> **旧バージョンの資料です。** このページは v0.2 の構文を記録しています。v0.3 では `ハイ`（import）、`ウラウラ`（in）、`プルップラッ`（try）、`ウギッ`（catch）などを推奨します。詳しくは [v0.3 日本語ガイド](V03_FEATURES.ja.md) を参照してください。旧構文は引き続き利用可能です。

`v0.2.0-alpha` は開発中のバージョンです。公開済みの `v0.1.0-alpha` タグとは異なります。

## CLI / REPL

```bash
python -m pip install -e .
usagi run examples/v02.usagi
usagi check examples/v02.usagi
usagi repl
```

`check` は構文解析のみを実行し、コードは実行しません。REPL は複数行入力、`:help`、`:reset`、`:exit` に対応しています。

## リストの変更

```usagi
プルャ xs=[1,2]
xs[0]=9
xs.append(3)
ウラ xs.pop()
ウラ xs
```

`items.insert(index, value)`、`append(items, value)`、`pop(items[, index])` も使えます。文字列は変更できません。

## 標準ライブラリ

- 数値：`abs`、`round`、`sum`、`min`、`max`
- 数学：`math.sqrt`、`math.floor`、`math.ceil`、`math.pow`、`math.pi`
- 文字列：`text.upper`、`text.lower`、`text.split`、`text.join`
- 乱数：`random.randint`、`random.choice`
- 時間：`clock.now`（Unix 時刻の秒数）

## クラスとオブジェクト

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

`init(self, ...)` は省略可能な初期化メソッドです。`self` はメソッド呼び出し時に渡されます。継承・静的メソッド・アクセス制御には未対応です。

## 例外処理

```usagi
ためす {
    なげる "ヤハ！"
} つかまえる e {
    ウラ e
}
```

`try/catch/throw` と `시도/잡기/던지기` も同じ構文です。捕捉するのは UsagiLang の実行エラーであり、すべての Python 例外ではありません。

## エラー表示

`🐰 ヤダ！ [E100] path:line:column` 形式のエラーと、該当コードの位置、一部の修正ヒントを表示します。`--plain-errors` でテーマを無効化できます。

## オフライン・パッケージ管理（実験的）

```bash
usagi pkg init
usagi pkg add mymath examples/modules/math.usagi
usagi pkg list
usagi pkg verify
usagi pkg remove mymath
```

`pkg add` はプロジェクト内で選択した `.usagi` ファイルだけを `.usagi/packages/` にコピーし、`usagi-packages.json` に登録します。オンラインからの取得、レジストリ、依存関係の解決、バージョン管理は未対応です。

```usagi
import "pkg:mymath" as mymath
ウラ mymath.square(6)
```

## VS Code

`vscode/usagilang` に拡張機能の開発用ソースがあります。構文強調、スニペット、キーワード補完、実行と構文チェックのコマンドを提供します。Marketplace には公開されていません。

## テストと注意

```bash
python -m unittest discover -s tests -v
python usagilang.py examples/v02.usagi
```

本処理系は**安全なサンドボックスではありません**。信頼できないコードを実行しないでください。Python の任意モジュールの import や一般的なファイル I/O は実装していません。

これは原作者・権利者とは無関係の非公式ファン制作プロジェクトです。プログラミング上の意味は独自に考案したものです。
