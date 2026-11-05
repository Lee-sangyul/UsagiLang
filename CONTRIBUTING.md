# Contributing to UsagiLang

Thanks for helping improve UsagiLang! 🐰

## Getting started

1. Install Python 3.10 or newer (no external libraries required).
2. Run `python -m unittest discover -s tests -v`.
3. Add a new `.usagi` example or a unit test for each behavior change.
4. Open an issue for breaking syntax proposals before implementing them.
5. Open a pull request with a concise change summary and test results.

## Language design rules

- Preserve backward compatibility with `.usagi` v0.1 samples when practical.
- Japanese spellings are canonical; Korean aliases must produce equivalent tokens.
- Do not claim that keywords have official translations in the source franchise.
- Avoid copyrighted artwork, screenshots, audio, character logos, or other unlicensed assets in contributions.
- Do not add unsafe Python `eval` or `exec` as a shortcut to interpreter implementation.

## Testing

```bash
python -m unittest discover -s tests -v
python usagilang.py examples/hello.usagi
```