# Changelog

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