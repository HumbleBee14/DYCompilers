# DYCompilers

A structured workspace for growing from compiler fundamentals to advanced ML compiler development. Each stage groups notes, exercises, and hands-on projects so you can progress quickly without losing track of assets or reusable tooling.

## Learning Phases
- `01-foundations` — math/CS refreshers, formal language theory, automata, data-structures, and first lexer/parser experiments
- `02-basic-compilers` — single-file compilers, expression evaluators, bytecode interpreters, and pipeline anatomy
- `03-intermediate-compilers` — typed languages, IR design, optimisations, register allocation, and simple VMs
- `04-advanced-compilers` — SSA-based optimisers, JITs, multi-pass backends, and language feature research
- `05-ml-compilers` — graph compilers, autodiff, MLIR/TVM pipelines, hardware acceleration, and model lowering
- `docs` — roadmap, study plans, and reference material that span every phase
- `shared` — reusable tooling, scripts, and project templates for consistent scaffolding

## Getting Started
1. Read `docs/ROADMAP.md` for the month-long journey and weekly milestones.
2. Follow `docs/LEARNING_PATH.md` to schedule study blocks and pick companion resources.
3. Start logging theory notes inside `01-foundations/notes` and tackle the exercises before moving onto projects.
4. Use the template in `shared/templates/compiler-project` when spinning up a new compiler project.

## Development Environment (WSL Ubuntu)
Set up the toolchain once on WSL2/Ubuntu to cover C/C++, LLVM, and MLIR experiments.

- **Enable WSL2 + install Ubuntu** – Turn on "Windows Subsystem for Linux" and "Virtual Machine Platform", install Ubuntu from the Microsoft Store, then update packages:
  - `sudo apt update && sudo apt upgrade -y`
- **Compiler toolchain & build essentials** – Install core compilers, build systems, and scripting basics:
  - `sudo apt install -y build-essential cmake ninja-build git python3 python3-pip clang lld lldb`
    - `build-essential` — GCC/G++ and standard headers for native builds.
    - `cmake` — Cross-platform build configuration generator.
    - `ninja-build` — Fast build executor used by modern compiler projects. Works with CMake.
                      → Replaces make in modern projects for faster incremental builds.
    - `git` — Source control for cloning LLVM and managing this workspace.
    - `python3` / `python3-pip` — Scripting glue, test harnesses, and build helpers.
    - `clang` — Alternate C/C++ compiler; good for LLVM-centric work.
    - `lld` — LLVM linker that pairs with Clang for faster links.
    - `lldb` — LLVM debugger used in compiler toolchains.
- **Lexer/parser utilities** – `sudo apt install -y flex bison`
  - `flex` — Generates lexers from regular-expression specs.
  - `bison` — Generates parsers from grammar descriptions.
- **LLVM headers and libraries** – `sudo apt install -y llvm-dev libclang-dev`
  - `llvm-dev` — Development headers/libs to embed LLVM without a source build.
  - `libclang-dev` — Clang C API for tooling and parsing experiments.
- **Sanity check** – Confirm Clang + Ninja toolchain works using the sample project in `shared/samples/toolchain-check`:
  - ```bash
    cmake -S shared/samples/toolchain-check \
      -B shared/samples/toolchain-check/build \
      -G Ninja -DCMAKE_CXX_COMPILER=clang++
    cmake --build shared/samples/toolchain-check/build
    ./shared/samples/toolchain-check/build/hello
    ```
- **Optional: build LLVM/MLIR from source** – Needed when experimenting with custom MLIR dialects:
  - Install extras: `sudo apt install -y python3-venv zlib1g-dev libedit-dev libxml2-dev`
    - `python3-venv` — Isolated environments for MLIR Python tooling.
    - `zlib1g-dev` — Compression dependency required by LLVM.
    - `libedit-dev` — Line-editing library used by LLVM shell tools.
    - `libxml2-dev` — XML support for certain LLVM components.
  - Clone + build:
    - ```bash
      git clone https://github.com/llvm/llvm-project.git
      cd llvm-project
      mkdir build && cd build
      cmake -G Ninja ../llvm \
        -DLLVM_ENABLE_PROJECTS="clang;lld;mlir" \
        -DLLVM_TARGETS_TO_BUILD="X86;NVPTX;AMDGPU" \
        -DCMAKE_BUILD_TYPE=Release \
        -DLLVM_ENABLE_ASSERTIONS=ON
      ninja
      # Optional install step requires sudo:
      # sudo ninja install
      ```

Revisit `shared/tools/tooling-checklist.md` as you add linters, formatters, or extra dependencies.

Prefer keeping LLVM/MLIR inside this repository (rather than a one-off clone)? Use the submodule workflow below.

## LLVM/MLIR Submodule Workflow (release/19.x)
- **Add the submodule**
  - ```bash
    mkdir -p external
    git submodule add -b release/19.x https://github.com/llvm/llvm-project.git external/llvm-project
    git submodule update --init --recursive
    ```
  - Tip: fetch tags and `git -C external/llvm-project checkout llvmorg-19.1.0` if you want an exact pin.
- **Build out-of-tree** (keeps sources clean)
  - ```bash
    cmake -S external/llvm-project/llvm \
      -B external/llvm-project/build \
      -G Ninja \
      -DLLVM_ENABLE_PROJECTS="clang;lld;mlir" \
      -DLLVM_TARGETS_TO_BUILD="X86;NVPTX;AMDGPU" \
      -DCMAKE_BUILD_TYPE=Release \
      -DLLVM_ENABLE_ASSERTIONS=ON \
      -DCMAKE_INSTALL_PREFIX="${PWD}/external/llvm-project/build/install"
    cmake --build external/llvm-project/build
    cmake --build external/llvm-project/build --target install
    ```
- **Use from your CMake projects**
  - ```cmake
    set(LLVM_DIR "${CMAKE_SOURCE_DIR}/external/llvm-project/build/install/lib/cmake/llvm")
    set(MLIR_DIR "${CMAKE_SOURCE_DIR}/external/llvm-project/build/install/lib/cmake/mlir")
    find_package(LLVM REQUIRED CONFIG)
    find_package(MLIR REQUIRED CONFIG)
    ```
  - Then link the needed targets, e.g. `LLVMCore`, `LLVMSupport`, `MLIRIR`, `MLIRParser`.
- **After cloning**
  - Run `git submodule update --init --recursive` (add `--depth 1` for shallow clones) before building.

------------------------------

---

# 🔹 What is `CMakeLists.txt`?

* It’s a **recipe file** (written in the CMake language).
* It tells **CMake**:

  * what the project is called,
  * what source files exist,
  * what libraries to link,
  * what compiler flags to use.

Think of it like a **Makefile, but cross-platform and modern**.

Example:

```cmake
cmake_minimum_required(VERSION 3.16)
project(hello LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)  # require C++17
add_executable(hello hello.cpp)
```

This says: “make an executable called `hello` from `hello.cpp`.”

Without it, CMake doesn’t know what to build.

---

# 🔹 Why two CMake commands?

### 1) **Configure step**

```bash
cmake -S . -B build -G Ninja -DCMAKE_CXX_COMPILER=clang++
```

* `-S .` → **source dir** (where `CMakeLists.txt` lives).
* `-B build` → **build dir** (where all temporary files go). Keeps source clean.
* `-G Ninja` → use **Ninja** build system instead of Make.
* `-DCMAKE_CXX_COMPILER=clang++` → tell CMake which compiler to use.

👉 This step **generates build instructions** (like a Ninja “Makefile”) in the `build/` folder.

---

### 2) **Build step**

```bash
cmake --build build
```

* This **runs the actual compilation**, using the generator chosen earlier (Ninja here).
* It builds the target (`hello`) into `build/hello`.

👉 So first CMake = “decide *how* to build.”
👉 Second CMake = “actually build.”

---

# 🔹 Why not just `cmake --build`?

Because CMake needs to **configure once** to know what to build.

* If you skip the first step, there are no build files yet.
* After the first configure, you can just run:

  ```bash
  cmake --build build
  ```

  repeatedly whenever you change code.



-------------
==========================================
---

# 🛠️ Compiler Dev Environment – Package by Package

### 🔹 Core Build Toolchain

* **`build-essential`** → Installs `gcc`, `g++`, `make`, and standard headers.
  → Needed for *basic C/C++ compilation* and linking.

* **`clang` / `clang++`** → LLVM’s C/C++ compiler.
  → You’ll often build compilers *with Clang*, and sometimes target LLVM IR.

* **`lld`** → LLVM’s linker (faster than GNU `ld`).
  → Lets you test linking phases with LLVM tools.

* **`lldb`** → LLVM’s debugger.
  → Debug your compiler or generated binaries (alternative to GDB).

* **`cmake`** → Cross-platform build system generator.
  → Almost every modern compiler project (LLVM, MLIR, TVM, etc.) uses it.

* **`ninja-build`** → Fast build executor, works with CMake.
  → Replaces `make` in modern projects for faster incremental builds.

* **`git`** → Version control.
  → To pull LLVM, MLIR, TVM, XLA source repos.

---

### 🔹 Parsing Tools

* **`flex`** → Lexical analyzer generator.
  → Generates C code for *tokenizing source input* into a stream of tokens.

* **`bison`** → Parser generator.
  → Consumes tokens from `flex` and builds *ASTs or parse trees*.

(These are used in “classic” compilers; MLIR/XLA often use hand-written parsers, but learning them is essential for understanding compiler frontends.)

---

### 🔹 LLVM/Clang Development

* **`llvm-dev`** → Headers and libraries for LLVM.
  → Needed if your compiler wants to *emit LLVM IR* or use LLVM’s optimization passes.

* **`libclang-dev`** → Clang’s C API.
  → Useful for tooling (e.g., if you want to parse C/C++ code from your own compiler or tool).

---

### 🔹 Language & Scripting

* **`python3` / `python3-pip`** → Python runtime + package manager.
  → Required for MLIR tutorials (many tools/scripts are in Python) and for TVM.

---

### 🔹 Extra Dev Dependencies (when building LLVM/MLIR from source)

* **`zlib1g-dev`** → Compression library.
  → LLVM uses this for compressed debug info & object files.

* **`libedit-dev`** → Line editing (like GNU readline).
  → Used in LLVM’s interactive tools (e.g., REPL shells).

* **`libxml2-dev`** → XML parsing.
  → LLVM uses it in some analysis/serialization tools.

---

# 🔑 How They Fit Into Compiler Development

* **Frontend (parsing source → AST)** → `flex`, `bison`, `clang-dev`.
* **Middle-end (IR + optimizations)** → `llvm-dev`, `clang`, `lld`, `cmake+ninja`.
* **Backend (codegen, linking)** → `lld`, `gcc/g++`, `clang++`.
* **Testing/debugging** → `lldb`, `git`, `python3`.
* **Infra** → `cmake`, `ninja`, `zlib`, `libedit`, `libxml2`.

---

👉 So in practice:

* If you want to **write your own toy compiler**: you’ll use `flex + bison` → C++ → build with `cmake + ninja`.
* If you want to **target LLVM IR**: you’ll link against `llvm-dev`.
* If you want to **experiment with MLIR**: you’ll build MLIR with `cmake+ninja`, then use Python scripts to test dialects.
* If you want to **debug generated code**: you’ll use `lldb`.

---
============================================================



---

# 📌 LLVM & MLIR – What They Are and Why They Matter

NOTE: LLVM/MLIR are *everywhere* in compilers (classical and ML).

### 🔹 LLVM

* **What it is:**
  A **compiler infrastructure** (libraries + tools) for building compilers.
  Originally stood for *Low-Level Virtual Machine*.
  It defines a **common Intermediate Representation (LLVM IR)** and provides optimization + codegen backends.

* **Where it fits:**

  * **Frontend** (e.g., Clang parses C++ into LLVM IR).
  * **Middle-end** (LLVM does optimizations: inlining, loop unrolling, vectorization).
  * **Backend** (LLVM lowers IR into machine code for x86, ARM, GPU, etc.).

* **Why important:**
  Instead of writing your own optimizer/codegen, you can **reuse LLVM** and just write a frontend for your language.

---

### 🔹 MLIR (Multi-Level Intermediate Representation)

* **What it is:**
  A **framework to define many IRs**, layered at different abstraction levels.
  It was created by Google for ML/AI workloads.
  Think of it as “LLVM for *higher-level* computation graphs.”

* **Where it fits:**

  * Above LLVM: handles **tensor ops, loops, high-level algebra**.
  * Provides **dialects** (custom IRs for domains). Examples:

    * `linalg` dialect → matrix ops
    * `mhlo` (XLA’s HLO) dialect → TensorFlow ops
    * `gpu` dialect → GPU kernels
  * Eventually lowers to LLVM IR (or SPIR-V, CUDA, ROCm, etc.) for execution.

* **Why important:**
  ML models are big graphs (matmul, conv, ReLU). MLIR lets you represent + transform these at **multiple levels** before lowering to hardware instructions.

---

### 🔹 Relationship Between LLVM & MLIR

* **LLVM IR** = low-level, close to assembly, machine-focused.
* **MLIR** = higher-level, graph/tensor focused, but can lower into LLVM IR.
* In ML compilers:

  ```
  TensorFlow/PyTorch graph → MLIR dialects → Lower → LLVM IR → CPU/GPU code
  ```

---

# 📚 Quick Notes for You

* **LLVM IR** = *Universal low-level IR*, used by most modern compilers (C/C++, Rust, Swift, Julia, etc.).
* **MLIR** = *Meta-IR framework*, for building domain-specific IRs (esp. ML/AI), then lowering to LLVM IR.
* **Together**: MLIR handles high-level ML optimizations, LLVM does low-level optimizations + codegen.
* **Yes, ML/AI compilers (XLA, IREE, TVM, etc.) all use LLVM and/or MLIR**.

---

👉 In short, you can think of it like this analogy:

* LLVM IR = **assembly-like Esperanto** (common machine language).
* MLIR = **translation layers** above it, for different domains (ML, quantum, GPU).

---


=============================================================

---

# 🖼️ ML Compiler Pipeline (with LLVM + MLIR)

```
    ┌────────────────────────────────┐
    │   Python ML Framework (User)   │
    │   (PyTorch / TensorFlow code)  │
    └───────────────┬────────────────┘
                    │
                    ▼
      ┌────────────────────────────┐
      │  Framework Frontend IR     │
      │  (TorchScript IR / TF Graph│
      │   / ONNX format, etc.)     │
      └─────────────┬──────────────┘
                    │
                    │  (optional MLIR integration)
                    ▼
      ┌────────────────────────────┐
      │     MLIR Dialects          │
      │ (Torch dialect, MHLO,      │
      │  Linalg, GPU, Affine, etc.)│
      └─────────────┬──────────────┘
                    │  lowering
                    ▼
      ┌────────────────────────────┐
      │        LLVM IR             │
      │  (universal low-level IR)  │
      │  Optimizations + Codegen   │
      └────────────┬───────────────┘
                   │  target backend
                   ▼
      ┌────────────────────────────┐
      │  Machine Code / GPU Code   │
      │ (x86, ARM, CUDA, SPIR-V,   │
      │  ROCm, TPU, etc.)          │
      └────────────────────────────┘
```

---

# 📌 Key Notes for Your Understanding

* **Frontend IRs (TorchScript IR, TF Graph, ONNX)**
  → Generated by the ML frameworks themselves.
  → These are the “starting IRs” you get from Python ML code.

* **MLIR Dialects (optional but very useful)**
  → MLIR is a *framework* to define multiple IRs at different levels.
  → You can skip MLIR and go straight to LLVM IR (older compilers like XLA did this),
  but you lose semantic richness (e.g., “this op is a conv2d”).

* **LLVM IR (mandatory in most flows)**
  → The universal low-level IR.
  → Handles classic compiler optimizations and lowering to real hardware instructions.

* **Final Machine Code**
  → Runs on CPU/GPU/TPU/etc.

---



👉 So the path is basically:

* **User writes Python model → Framework captures it in a graph IR → (maybe lowered into MLIR dialects) → eventually lowered into LLVM IR → machine code.**

---


=============================================================


## Contributing Projects
- Place each new compiler under the phase that matches its scope and create a fresh folder using the template.
- Keep project documentation (design notes, decisions, benchmarks) inside its nested `docs/` directory.
- Share reusable components (lexers, IR utilities, testing harnesses) in `shared/tools` so future projects can reuse them.

Move forward phase by phase; once you are comfortable compiling traditional languages, the ML compiler track will feel natural.
