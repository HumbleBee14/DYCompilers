#!/usr/bin/env bash
set -euo pipefail

# Shared test wrapper.
# Usage: ./shared/tools/test.sh <project-path>
# Detects common test runners; extend as projects grow.

PROJECT_DIR="${1:-01-foundations/projects/lexer-playground}"

if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "[test] project directory not found: $PROJECT_DIR" >&2
  exit 1
fi

if [[ -f "$PROJECT_DIR/pytest.ini" || -d "$PROJECT_DIR/tests" && -f "$PROJECT_DIR/requirements.txt" ]]; then
  (cd "$PROJECT_DIR" && python -m pytest)
elif [[ -f "$PROJECT_DIR/Cargo.toml" ]]; then
  (cd "$PROJECT_DIR" && cargo test)
elif [[ -f "$PROJECT_DIR/package.json" ]]; then
  (cd "$PROJECT_DIR" && npm test)
else
  echo "[test] no recognised test configuration; add commands here." >&2
fi
