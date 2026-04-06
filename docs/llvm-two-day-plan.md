# LLVM Crash Plan (2 Days)

Goal: go from Java-heavy background with light C++ to a demo-ready LLVM story in 48 hours, touching both middle-end (IR instrumentation) and backend (instruction selection with a custom AI MAC). Code footprint is tiny; most time is wiring and verifying.

## Prereqs (Day 0, 30–60 min)
- Install: `sudo apt update && sudo apt install -y build-essential clang lld llvm-dev cmake ninja-build`
- C++ reboot targets: `auto`, references/pointers vs Java refs, ranges-for, RAII, `dyn_cast/isa/cast`, headers vs translation units.

## Day 1 – Middle-End Pass (TracePass)
**Objective:** Out-of-tree pass that injects `printf` at function entry; proves IR navigation + IRBuilder use.

1) IR warmup (45m)
- Generate/read IR: `clang -S -emit-llvm -O0 sample.c -o sample.ll`
- Identify Module → Function → BasicBlock → Instruction; SSA `%` names; terminators.

2) Project scaffolding (15m)
- Files: `TracePass/CMakeLists.txt`, `TracePass/TracePass.cpp` (new pass manager plugin).
- Key CMake pieces: `find_package(LLVM REQUIRED CONFIG)`, `include(AddLLVM)`, `add_llvm_pass_plugin(...)`.

3) Implement pass (1.5–2h)
- `run(Module&)`: `getOrInsertFunction("printf")`; skip declarations; get entry block; `IRBuilder` insert `CreateGlobalStringPtr` and `CreateCall`.
- Return `PreservedAnalyses::none()` since IR is modified.

4) Build + test loop (1h)
```bash
mkdir -p TracePass/build && cd TracePass/build
cmake .. && cmake --build .
cat > ../test.c <<'EOF'
#include <stdio.h>
void helper(){ int x=10; }
int main(){ helper(); return 0; }
EOF
clang -O0 -emit-llvm -c ../test.c -o test.bc
opt -load-pass-plugin=./TracePass.so -passes="trace-pass" test.bc -o inst.bc
llvm-dis inst.bc -o - | grep printf   # see injected call
clang inst.bc -o test && ./test       # run to see logs
```

5) Interview crib (30m)
- Concepts: BasicBlock, terminator, SSA, why new pass manager, `IRBuilder` cursor model, `dyn_cast` vs `dynamic_cast`.
- Mapping to Java: object graph iteration; `dyn_cast` ≈ `instanceof` + cast; `auto` ≈ `var`.

## Day 2 – Backend Taste + ML Angle (RISC-V AI_MAC)
**Objective:** Add fused multiply-add instruction to RISC-V backend via TableGen and prove instruction selection on C code (including a tiny ML kernel).

1) Source build (start early, 2–3h wall clock)
```bash
git clone --depth 1 https://github.com/llvm/llvm-project.git
cd llvm-project
mkdir build && cd build
cmake -G Ninja -DLLVM_ENABLE_PROJECTS="clang" -DLLVM_TARGETS_TO_BUILD="RISCV" -DCMAKE_BUILD_TYPE=Release ../llvm
ninja llc llvm-mc
```

2) Add custom instruction (1h editing + rebuild)
- Edit `llvm/lib/Target/RISCV/RISCVInstrInfo.td`:
  - Define `AI_MAC` as R-type (outs GPR:$rd, ins GPR:$rs1,$rs2,$rs3).
  - Add pattern: `Pat<(add (mul GPR:$a, GPR:$b), GPR:$c), (AI_MAC GPR:$a, GPR:$b, GPR:$c)>`.
- Rebuild: `ninja llc llvm-mc`.

3) Assembler acceptance (15m)
```bash
echo "ai_mac a0, a1, a2, a3" | ./bin/llvm-mc -triple=riscv32 -show-encoding
```

4) Instruction selection check (45m)
```bash
cat > math.c <<'EOF'
int ml_kernel(int a,int b,int c){ return a + b * c; }
EOF
./bin/clang -O3 --target=riscv32 -emit-llvm -c math.c -o math.bc
./bin/llc -march=riscv32 math.bc -o math.s
grep ai_mac math.s   # expect fused op instead of mul+add
```

5) ML demo (45m)
- Use naive GEMM:
```bash
cat > matmul.c <<'EOF'
#define N 16
void ml_inference_layer(int A[N][N], int B[N][N], int C[N][N]) {
  for (int i=0;i<N;i++)
    for (int j=0;j<N;j++) {
      int sum=0;
      for (int k=0;k<N;k++) sum += A[i][k]*B[k][j];
      C[i][j]=sum;
    }
}
EOF
./bin/clang -O3 --target=riscv32 -emit-llvm -c matmul.c -o matmul.bc
./bin/llc -march=riscv32 matmul.bc -o matmul.s
grep ai_mac matmul.s || true
```
- If missing, try `-O2` or adjust pattern for commuted operands; use `llc -debug` if needed.

6) Story framing (30m)
- Middle-end: IR instrumentation with `IRBuilder`, pass plugin, SSA awareness.
- Backend: TableGen instruction def + DAG pattern for ISel; hardware/software co-design assumption (3-input ALU).
- ML link: fused MAC reduces instruction count in GEMM inner loop; mention next-step loop tiling/cost modeling.

## Optional polish (if time)
- Extend TracePass to log arg count (`F.arg_size()`).
- Add a short note mapping CFG/BasicBlocks to your pass in your notes.

## Deliverables checklist
- `TracePass.so` (or `.dylib`) built and demonstrated on `test.c`.
- `AI_MAC` present in `math.s` (and ideally `matmul.s`) via your modified RISC-V backend.
- Talking points prepared for interview: new pass manager, IRBuilder, TableGen patterns, ISel fusion for ML kernels.
