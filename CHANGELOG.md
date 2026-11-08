# Changelog

## [Unreleased]

### Added
- Local `.usagi` file imports via `import` / `インポート` / `가져와` and optional namespace aliases (`as` / `として` / `별칭`).
- Module member access with `module.name`, caching, file-relative paths, separate environments, and cyclic import detection.
- Import examples and regression tests; Korean and Japanese documentation updates.
- v0.2.0-alpha (development): stateful multiline REPL; `run`, `check`, `repl` and `pkg` CLI subcommands; pip-installable `usagi` entry point.
- Mutable lists (`items[0] = value`, `append`, `pop`, `insert`) and math/text/random/clock standard namespaces.
- Class declarations, instance fields, bound methods and optional `init(self, ...)` initializers.
- `try` / `catch` / `throw` (Japanese and Korean aliases), themed diagnostics and source locations.
- Offline local-file package manager with `usagi-packages.json` and `import "pkg:name"` support.
- VS Code syntax extension source (highlighting, snippets, keyword completion, Run/Check commands).
- Feature tests, runnable `examples/v02.usagi`, Korean/Japanese guides.


## [0.1.0-alpha] - 2026-11-05

First experimental release.

### Added
- Standalone Python lexer, parser and tree-walking interpreter.
- Japanese and Korean aliases for language keywords, including mixed-script files.
- Print, input, variables, conditionals, loops, lists, indexing, user functions, recursion and built-ins.
- Six sample `.usagi` programs and 19 standard-library unit tests.
- CLI file execution, `-c` inline execution, and `--max-steps` guard.
- Language reference, README, MIT license, and GitHub Actions test workflow.

### Known limitations
- No modules/import, class system, REPL or package manager yet.
- Not a security sandbox for untrusted code; memory/output/recursion bounds are incomplete.
- Original fictional expressions are inspirations; their programming meanings are invented by this project.