#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PY="${PYTHON:-"$ROOT/.venv/bin/python"}"
if [[ ! -x "$PY" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    PY="$(command -v python3)"
  else
    echo "ERROR: Python interpreter not found." >&2
    echo "Expected: $ROOT/.venv/bin/python" >&2
    echo "Hint: create a venv at .venv or set PYTHON=/path/to/python" >&2
    exit 1
  fi
fi

echo "==> Python: $("$PY" -c 'import sys; print(sys.executable)')"
echo "==> Project root: $ROOT"

echo ""
echo "==> 1/3 Running pytest"
(cd "$ROOT" && "$PY" -m pytest -q)

echo ""
echo "==> 2/3 Verifying type stubs"
(cd "$ROOT" && "$PY" verify_type_stubs.py)

echo ""
echo "==> 3/3 Running Rust tests"
(cd "$ROOT/rust" && cargo test -q)

echo ""
echo "Quality gate passed."
