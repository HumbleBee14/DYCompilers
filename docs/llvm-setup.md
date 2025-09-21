# LLVM / MLIR Setup (WSL Ubuntu)

Use this guide to pick the quickest path for obtaining LLVM + MLIR when working on this repository.

> **TL;DR** — Use a prebuilt archive if you have one. Otherwise, do the minimal submodule build (MLIR + X86). Upgrade to full source builds only when you need Clang or GPU backends.

## 1. Prerequisites

```bash
sudo apt update
sudo apt install -y build-essential cmake ninja-build git python3 python3-pip \
  clang lld lldb flex bison zlib1g-dev libedit-dev libxml2-dev
```

Work inside the Linux file system (e.g. `~/dev/...`), not `/mnt/c/...`, for faster builds.

---

## Option 1 — Fastest: Use a Prebuilt Archive

If you already have a vetted LLVM + MLIR archive (example shown for 19.1.x):

```bash
export LLVM_INSTALL_DIR=~/tools/llvm19
mkdir -p "$LLVM_INSTALL_DIR"
tar -C "$LLVM_INSTALL_DIR" -xJvf ~/Downloads/llvm_mlir_rel_v19_1_6_x86_linux.tar.xz --strip-components=1
export PATH="$LLVM_INSTALL_DIR/bin:$PATH"
export LLVM_DIR="$LLVM_INSTALL_DIR/lib/cmake/llvm"
export MLIR_DIR="$LLVM_INSTALL_DIR/lib/cmake/mlir"
mlir-opt --version
llvm-config --version
```

Add the `export` lines to your shell profile (`~/.bashrc`, etc.) so they persist.

Point CMake at `$LLVM_DIR` / `$MLIR_DIR` or pass them on the command line when building.

> Windows users can extract the archive to a path without spaces (e.g. `C:\llvm19`) and set environment variables via “Edit the system environment variables”.

---

## Option 2 — Fast & Reproducible: LLVM Submodule (Minimal Build)

1. Track LLVM release 19.x inside this repository:
   ```bash
   mkdir -p external
   git submodule add -b release/19.x https://github.com/llvm/llvm-project.git external/llvm-project
   git -C external/llvm-project fetch --tags
   git -C external/llvm-project checkout llvmorg-19.1.0
   git add external/llvm-project
   git commit -m "Add LLVM submodule pinned to 19.1.0"
   ```
   After cloning the repo, run `git submodule update --init --recursive` (add `--depth 1` for a shallow fetch).

2. Configure a minimal build (MLIR tools, X86 target only):
   ```bash
   cmake -S external/llvm-project/llvm \
     -B external/llvm-project/build-min \
     -G Ninja \
     -DLLVM_ENABLE_PROJECTS="mlir" \
     -DLLVM_TARGETS_TO_BUILD="X86" \
     -DCMAKE_BUILD_TYPE=Release \
     -DLLVM_ENABLE_ASSERTIONS=ON \
     -DLLVM_USE_LINKER=lld \
     -DLLVM_BUILD_TOOLS=ON \
     -DLLVM_BUILD_TESTS=OFF -DLLVM_INCLUDE_TESTS=OFF -DLLVM_INCLUDE_BENCHMARKS=OFF \
     -DCMAKE_INSTALL_PREFIX="${PWD}/external/llvm-project/build-min/install"
   ```

3. Build and install:
   ```bash
   cmake --build external/llvm-project/build-min -j"$(nproc)"
   cmake --build external/llvm-project/build-min --target install
   ```

4. Verify tool availability:
   ```bash
   external/llvm-project/build-min/install/bin/mlir-opt --version
   external/llvm-project/build-min/install/bin/llvm-config --version
   ```

5. Point project CMake files at the install directory:
   ```cmake
   set(LLVM_DIR "${CMAKE_SOURCE_DIR}/external/llvm-project/build-min/install/lib/cmake/llvm")
   set(MLIR_DIR "${CMAKE_SOURCE_DIR}/external/llvm-project/build-min/install/lib/cmake/mlir")
   find_package(LLVM REQUIRED CONFIG)
   find_package(MLIR REQUIRED CONFIG)
   ```

Add GPU backends later by reconfiguring with `-DLLVM_TARGETS_TO_BUILD="X86;NVPTX"` (NVIDIA) or `"X86;AMDGPU"` (AMD).

---

## Option 3 — Slowest: Full Source Build (Clang + Multiple Backends)

When you need Clang, LLD, and GPU targets together, use the fuller build. Expect multi-hour compilation.

```bash
cmake -S external/llvm-project/llvm \
  -B external/llvm-project/build \
  -G Ninja \
  -DLLVM_ENABLE_PROJECTS="clang;lld;mlir" \
  -DLLVM_TARGETS_TO_BUILD="X86;NVPTX;AMDGPU" \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_ASSERTIONS=ON \
  -DLLVM_USE_LINKER=lld \
  -DCMAKE_INSTALL_PREFIX="${PWD}/external/llvm-project/build/install"
cmake --build external/llvm-project/build -j"$(nproc)"
cmake --build external/llvm-project/build --target install
```

This yields `clang`, `lld`, `mlir-opt`, `mlir-translate`, `llc`, etc., with CPU + GPU support.

---

## 3. Target Selection Guide

| Learning Stage | Recommended Targets |
| --- | --- |
| Front-end + IR fundamentals | `X86` |
| Advanced optimisation experiments | `X86` |
| ML/AI on CPU | `X86` |
| ML/AI on NVIDIA GPU | `X86;NVPTX` |
| ML/AI on AMD GPU | `X86;AMDGPU` |

Start with `X86` only to keep builds fast; add GPU backends when you actively need them.

---

## 4. Toolchain Quick Reference

| Tool | Purpose |
| --- | --- |
| `mlir-opt` | Run MLIR passes (dialect conversions, optimisations). |
| `mlir-translate` | Convert between MLIR and LLVM IR text. |
| `opt` | Run LLVM IR optimisation passes on `.ll` files. |
| `llc` | Lower LLVM IR to object/assembly for a target. |
| `clang` / `lld` | Compile and link executables or libraries. |

Example CPU pipeline:

```bash
mlir-opt in.mlir -convert-linalg-to-loops -convert-scf-to-cf \
  -convert-memref-to-llvm -convert-arith-to-llvm -convert-func-to-llvm \
  -reconcile-unrealized-casts > out_llvm_dialect.mlir
mlir-translate out_llvm_dialect.mlir -mlir-to-llvmir > out.ll
llc -filetype=obj out.ll -o out.o
clang out.o -o out.bin
```

---

## 5. Helpful Configure Flags

- `-DLLVM_ENABLE_PROJECTS="mlir;clang;lld"` — choose which LLVM subprojects to build.
- `-DLLVM_TARGETS_TO_BUILD="X86;NVPTX"` — select codegen backends (start with `X86`).
- `-DLLVM_ENABLE_ASSERTIONS=ON` — better diagnostics during development.
- `-DLLVM_USE_LINKER=lld` — faster links compared to GNU ld.
- `-DCMAKE_INSTALL_PREFIX=...` — install destination for headers/libs/tools.
- `-DLLVM_BUILD_TOOLS=ON` — ensure utilities like `mlir-opt` are produced.

Optional speedups: install `ccache` and add `-DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache` to the CMake configure step.

---

## 6. Build This Repository Against LLVM/MLIR

```bash
cmake -S . -B build -G Ninja -DCMAKE_CXX_COMPILER=clang++ \
  -DLLVM_DIR="<path>/lib/cmake/llvm" \
  -DMLIR_DIR="<path>/lib/cmake/mlir"
cmake --build build
```

- Option 1: `<path>` = `$LLVM_INSTALL_DIR`
- Option 2: `<path>` = `external/llvm-project/build-min/install`
- Option 3: `<path>` = `external/llvm-project/build/install`

Persist environment variables or pass these paths via `cmake -D` flags.

---

## 7. Troubleshooting Tips

- Ensure builds happen on the Linux file system and use `ninja -j"$(nproc)"` for parallelism.
- If tools are missing, check `LLVM_BUILD_TOOLS=ON` and rerun the install target.
- Link errors usually mean `LLVM_DIR` / `MLIR_DIR` paths or the chosen compiler need adjustment.
- Add GPU backends by reconfiguring with the desired targets and rebuilding.
- Submodule clones can be shallow: `git submodule update --init --recursive --depth 1`.

You now have fast, reproducible, and full build options laid out. Start small; scale when your projects demand it.
