# Changelog

## [Unreleased]

### Added
- Local `.usagi` file imports via `import` / `インポート` / `가져와` and optional namespace aliases (`as` / `として` / `별칭`).
- Module member access with `module.name`, caching, file-relative paths, separate environments, and cyclic import detection.
- Import examples and regression tests; Korean and Japanese documentation updates.

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
- No class system, REPL or package manager yet. (Modules/imports are supported on the development branch.)
- Not a security sandbox for untrusted code; memory/output/recursion bounds are incomplete.
- Original fictional expressions are inspirations; their programming meanings are invented by this project.