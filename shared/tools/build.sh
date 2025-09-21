#!/usr/bin/env bash
set -euo pipefail

# Shared build wrapper.
# Usage: ./shared/tools/build.sh <project-path>
# If no project path is supplied, defaults to lexer playground during Week 1.

PROJECT_DIR="${1:-01-foundations/projects/lexer-playground}"

if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "[build] project directory not found: $PROJECT_DIR" >&2
  exit 1
fi

if [[ -f "$PROJECT_DIR/Makefile" ]]; then
  (cd "$PROJECT_DIR" && make all)
elif [[ -f "$PROJECT_DIR/Cargo.toml" ]]; then
  (cd "$PROJECT_DIR" && cargo build)
elif [[ -f "$PROJECT_DIR/package.json" ]]; then
  (cd "$PROJECT_DIR" && npm run build)
else
  echo "[build] no recognised build configuration; add commands here." >&2
fi
