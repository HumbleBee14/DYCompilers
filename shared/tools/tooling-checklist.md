# Tooling Checklist

Track environment setup tasks and shared utilities. Mark items complete as you verify them.

## Language Toolchains
- [ ] Install Rust (rustup) and add `cargo fmt`, `cargo clippy`.
- [ ] Install latest LLVM/Clang toolchain.
- [ ] Ensure Python 3.11+ with `pipx`/`venv` for scripts.

## Editors & Extensions
- [ ] Configure VS Code/Neovim/JetBrains with syntax + formatter integrations.
- [ ] Install tree-sitter grammar support for experiment languages.
- [ ] Set up debugger integrations (lldb/gdb).

## Formatting & Linting
- [ ] Define formatting rules (`.clang-format`, `rustfmt.toml`, etc.).
- [ ] Add lint command wrappers in `shared/tools` (e.g., `lint.sh`).
- [ ] Document how to run linters per language.

## Build & Test Automation
- [ ] Create `build.sh` / `build.ps1` cross-platform wrappers.
- [ ] Create `test.sh` / `test.ps1` to run project suites.
- [ ] Document coverage/reporting expectations.

## Utilities
- [ ] DFA/CFG visualisation scripts (Graphviz or similar).
- [ ] Benchmark harness template (time & memory measurement).
- [ ] Log formatting helper for CLIs.

Update this checklist as tooling matures. Completed utilities should include usage docs and, where relevant, example outputs.
