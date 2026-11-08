# UsagiLang VS Code extension (development source)

This folder contains **source code**, not a published Marketplace extension.

Features:
- `.usagi` file association, syntax coloring, brackets, and snippets.
- Keyword suggestions for Japanese, Korean, and English aliases.
- Commands: **UsagiLang: Run Current File** and **UsagiLang: Check Current File**.
- The path to the executable can be configured using `usagilang.cliPath`.

## Setup

1. From the repository root, install the command-line tool with `python -m pip install -e .`.
2. Open the `vscode/usagilang` folder in VS Code.
3. Press F5 to launch an Extension Development Host.
4. Open any .usagi file in the Development Host and run the commands from the Command Palette.

To distribute, build a VSIX with an extension packager; this source repository alone is **not** an installable marketplace release.

The VS Code extension does not run untrusted UsagiLang programs in a sandbox.
