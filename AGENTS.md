# AGENTS.md — postal-helper

Guidelines for AI coding agents working in this repository.

## Project Overview

A single-file Python CLI tool that queries Taiwan postal/zip codes (3+2 and 5+3
format) via the `zip5.5432.tw` public API. Zero third-party dependencies — uses
only Python standard library modules.

- **Language**: Python 3.10+
- **Entry point**: `postal_helper.py`
- **External API**: `https://zip5.5432.tw/zip5json.py?adrs=<address>`

## Build / Run / Test Commands

### Running the tool

```bash
# Single query
python3 postal_helper.py "台北市信義區市府路1號"

# JSON output
python3 postal_helper.py --json "台北市信義區市府路1號"

# Interactive mode (no arguments)
python3 postal_helper.py
```

### Linting

No linter configuration exists yet. A `.ruff_cache/` directory (ruff 0.15.0) is
present, indicating ruff has been used. To lint:

```bash
pip install ruff              # install if not available
ruff check postal_helper.py   # lint
ruff check --fix postal_helper.py  # auto-fix
ruff format postal_helper.py  # format
```

### Type checking

```bash
pip install mypy    # install if not available
mypy postal_helper.py
```

### Testing

No test framework or tests exist yet. If tests are added, use `pytest`:

```bash
pip install pytest

# Run all tests
pytest

# Run a single test file
pytest tests/test_postal_helper.py

# Run a single test function
pytest tests/test_postal_helper.py::test_query_zipcode
```

Note: Since the tool calls an external API, tests that exercise `query_zipcode`
will make real network requests unless mocked (use `unittest.mock.patch` on
`urllib.request.urlopen`).

## Code Style Guidelines

### General

- Python 3.10+ — use modern syntax (f-strings, `|` union types where needed).
- Single-file architecture for now; extract modules only when complexity demands.
- Keep the project zero-dependency (stdlib only) unless there is a strong reason.
- Use UTF-8 encoding throughout.

### Formatting

- **Indentation**: 4 spaces (no tabs).
- **Max line length**: 88 characters (ruff/black default).
- **Trailing commas**: Use in multi-line function arguments, lists, and dicts.
- **Blank lines**: Two blank lines between top-level definitions; one blank line
  within functions for logical separation.
- **Quotes**: Double quotes for strings.

### Imports

- Group imports in this order, separated by a blank line:
  1. Standard library (`import argparse`, `import json`, etc.)
  2. Third-party packages (none currently)
  3. Local modules (none currently)
- Sort alphabetically within each group.
- Use `import module` style; avoid `from module import *`.
- For `urllib`, import submodules explicitly (`urllib.error`, `urllib.parse`,
  `urllib.request`) rather than relying on implicit submodule availability.

### Naming Conventions

- **Functions / variables**: `snake_case` — e.g., `query_zipcode`, `display_result`.
- **Constants**: `UPPER_SNAKE_CASE` — e.g., `API_URL`.
- **Classes**: `PascalCase` (none exist yet).
- **Private helpers**: Prefix with `_` if not part of the public interface.

### Type Annotations

- All function signatures must include type annotations for parameters and
  return values.
- Use built-in generic types (`dict`, `list`, `str`, `int`) rather than
  `typing.Dict`, `typing.List`, etc. (Python 3.10+).
- Prefer specific types over `Any` when possible.

### Docstrings

- Every public function must have a docstring.
- Use triple double-quotes (`"""`).
- Single-line docstrings for simple functions; multi-line (summary + details)
  for complex ones.
- Module-level docstring at the top of each file describing its purpose.

### Error Handling

- Catch specific exceptions, not bare `except`.
- Network errors (`urllib.error.URLError`) and parse errors
  (`json.JSONDecodeError`) should be caught and reported to stderr with
  `print(..., file=sys.stderr)`.
- Use `sys.exit(1)` for fatal errors in CLI context.
- In interactive mode, catch `KeyboardInterrupt` and `EOFError` for graceful
  exit.

### CLI Design

- Use `argparse` for argument parsing.
- Support both single-shot (address as positional arg) and interactive modes.
- `--json` / `-j` flag outputs raw JSON for programmatic consumption.
- User-facing output goes to stdout; errors go to stderr.

### API Usage

- API endpoint: `https://zip5.5432.tw/zip5json.py`
- Pass address via `adrs` query parameter (URL-encoded).
- Set `User-Agent` and `Accept` headers on requests.
- Respect rate limits: 2-3 second delay between queries, max 2000/day.
- API returns JSON with keys: `adrs`, `zipcode`, `new_adrs`, `zipcode6`,
  `new_adrs6`, `dataver`, `dataver6`, among others.
- Empty `zipcode6` means no 3+3 data is available; fall back to `zipcode` (3+2).

### File Organization

```
postal-helper/
  postal_helper.py    # Main application (single-file)
  AGENTS.md           # This file
```

When adding tests, place them in `tests/` following pytest conventions
(`test_*.py` files).

### Commit Messages

- Write concise messages focusing on "why" over "what".
- Use imperative mood (e.g., "Add JSON output flag", "Fix URL encoding").
- Keep the subject line under 72 characters.
