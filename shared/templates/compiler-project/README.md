# Compiler Project Template

Use this template to bootstrap new compiler experiments. Copy the directory (or use `git worktree`/`degit`) and rename folders/files accordingly.

## Layout
- `docs/` — specs, architecture notes, changelog, benchmarks.
- `src/` — source code (organise by module/stage).
- `tests/` — unit, integration, fuzz, or property tests.
- `tools/` — scripts for building, linting, benchmarking, generating IR dumps, etc.

## Getting Started
1. Duplicate the folder into the target phase directory: `cp -r shared/templates/compiler-project 02-basic-compilers/projects/new-project`.
2. Update placeholders in documentation, rename packages/namespaces, and initialise version control if needed.
3. Register project-specific tooling (Makefile, Cargo manifest, etc.).
4. Write an initial design brief in `docs/architecture.md` before coding.

Keep the template up to date as your workflow evolves so new projects stay consistent.
