# TracePass (LLVM New Pass Manager Plugin)

This is a tiny **out-of-tree LLVM pass plugin** that instruments LLVM IR:
it injects a `printf("LOG: Entering function: <name>")` call at the start of
every defined function in a module.

## What You’re Building

- You are *not* writing a full compiler frontend.
- You are writing a **middle-end pass** that:
  - reads LLVM IR as an object graph (`Module → Function → BasicBlock → Instruction`)
  - mutates that IR by inserting new instructions (instrumentation)

## Files

- `LLVM/TracePass/CMakeLists.txt`
  - Finds LLVM via `find_package(LLVM CONFIG)`
  - Uses LLVM’s helper macro `add_llvm_pass_plugin(...)` to build `TracePass.so`
- `LLVM/TracePass/TracePass.cpp`
  - Defines a `Module` pass (`PassInfoMixin`) for the **new pass manager**
  - Declares `printf` in the module (`getOrInsertFunction`)
  - For each function body, inserts a `printf` call at the first valid insertion point
- `LLVM/TracePass/tests/test.c`
  - A small C program to demonstrate the instrumentation

## How The Pass Works (Conceptually)

1) LLVM parses/loads bitcode into a `Module`
2) The pass iterates:
   - each `Function` in the module
   - skips declarations (no body)
3) For each function:
   - finds the entry block
   - inserts a call to `printf` before the first non-PHI/debug instruction

The “insertion” is done via `IRBuilder`, which is like a cursor that emits new IR instructions at the current insertion point.

## Build

```bash
cd LLVM/TracePass
mkdir -p build && cd build
cmake -G Ninja -DLLVM_DIR="$(llvm-config --cmakedir)" ..
cmake --build .
```

Output: `LLVM/TracePass/build/TracePass.so`

## Run (Build + Test Loop)

```bash
cd LLVM/TracePass/build
LLVM_BINDIR="$(llvm-config --bindir)"

# 1) C → bitcode
clang-18 -O0 -emit-llvm -c ../tests/test.c -o test.bc

# 2) Run the pass (no output file needed if you only want to observe)
"$LLVM_BINDIR/opt" -load-pass-plugin=./TracePass.so -passes="trace-pass" test.bc -o inst.bc

# 3) Verify injection in IR
"$LLVM_BINDIR/llvm-dis" inst.bc -o - | rg "call.*@printf|LOG: Entering function"

# 4) Lower to object and link (avoid PIE relocation warnings)
"$LLVM_BINDIR/llc" inst.bc -filetype=obj -relocation-model=pic -o inst.o
clang-18 inst.o -no-pie -o test_exe

# 5) Run
./test_exe
```

