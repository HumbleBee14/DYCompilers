# C++ Refresher for LLVM/Compiler Work

Focus: modern C++ features and idioms you’ll touch constantly in LLVM passes, analyses, and backends.

## Compilation Units, Headers, Namespaces
- **Headers vs sources:** Declarations in `.h/.hpp`, definitions in `.cpp`. Avoid ODR violations by keeping one definition of symbols.
- **Include guards / `#pragma once`:** Prevent multiple inclusion.
- **Namespaces:** Prevent symbol collisions; LLVM uses `namespace llvm { ... }`.

Example:
```cpp
// foo.h
#pragma once
namespace demo { int add(int a, int b); }
// foo.cpp
#include "foo.h"
namespace demo { int add(int a, int b) { return a + b; } }
```

## auto Type Deduction
- Use `auto` to avoid verbose types and to stay correct with iterator-heavy APIs.
- Works with pointers/references; add `&` when you need a reference.
```cpp
auto x = 42;              // int
const auto &ref = x;      // const int&
for (auto &v : vec) { v++; }
```

## References and Pointers
- **Reference (`T&`)**: non-null alias; cannot reseat.
- **Pointer (`T*`)**: can be null; use `->` and `*`.
- Prefer references when you know the object exists; use pointers for optional/ownership-aware flows.
```cpp
void bump(int &v) { v++; }   // must have an int
void maybeUse(int *p) { if (p) *p += 1; }
```

## Const Correctness
- Mark data and member functions `const` to express immutability; unlocks use with const containers/algos.
```cpp
int getVal() const { return Val; }
void foo(const std::vector<int> &v) { /* read-only */ }
```

## RAII (Resource Acquisition Is Initialization)
- Acquire resources in constructors, release in destructors. Ensures cleanup on all code paths.
```cpp
struct FileHandle {
  FileHandle(FILE *f) : F(f) {}
  ~FileHandle() { if (F) fclose(F); }
  FILE *F;
};
```

## Smart Pointers
- `std::unique_ptr<T>`: sole ownership; moves only. Common in AST/IR builders.
- `std::shared_ptr<T>`: shared ownership; avoid unless required.
- `std::weak_ptr<T>`: non-owning handle to a `shared_ptr`.
```cpp
auto node = std::make_unique<MyNode>(...);
takeOwnership(std::move(node));  // transfers ownership
```

## Move Semantics
- Support efficient transfers; implement move ctor/assign when holding resources.
```cpp
struct Buf {
  Buf(size_t n): data(new int[n]), n(n) {}
  ~Buf(){ delete[] data; }
  Buf(Buf&& o) noexcept : data(o.data), n(o.n) { o.data=nullptr; o.n=0; }
  Buf& operator=(Buf&& o) noexcept {
    if (this!=&o){ delete[] data; data=o.data; n=o.n; o.data=nullptr; o.n=0; }
    return *this;
  }
  int *data; size_t n;
};
```

## Value Categories: lvalues/rvalues
- rvalues are temporaries; enable moves.
- Use `std::move` when you’re done using an object and want to transfer resources.

## Lambdas
- Used for callbacks, `llvm::make_range` transforms, small predicates.
```cpp
auto isEven = [](int x){ return x % 2 == 0; };
```

## Range-Based For and Iterators
- LLVM containers support iteration; prefer `auto &` to avoid copies.
```cpp
for (auto &BB : F) { /* BasicBlock */ }
for (auto &I : BB) { /* Instruction */ }
```

## Casting in LLVM (RTTI Off by Default)
- LLVM disables `dynamic_cast`; use:
  - `isa<T>(ptr)`: check type.
  - `cast<T>(ptr)`: assert + cast.
  - `dyn_cast<T>(ptr)`: safe cast, returns nullptr.
```cpp
if (auto *BO = llvm::dyn_cast<llvm::BinaryOperator>(Inst)) {
  /* use BO */
}
```

## Enums and `enum class`
- Prefer `enum class` for scoped, type-safe enums.
```cpp
enum class Kind { Add, Sub };
Kind k = Kind::Add;
```

## Struct vs Class, Access Specifiers
- `struct` defaults to public, `class` to private. Use minimal public API.

## Operator Overloads (light touch)
- LLVM uses them for things like `raw_ostream <<`. Implement when it improves clarity.

## Error Handling
- Exceptions often disabled in LLVM builds. Prefer:
  - Return `Error`/`Expected<T>` (LLVM style).
  - `Optional<T>` (or `std::optional` in non-LLVM code).
  - Status enums or bool + out param.
```cpp
llvm::Expected<int> parse(...) {
  if (fail) return llvm::createStringError(...);
  return value;
}
```

## Templates (Only as Needed)
- Common for utilities and container helpers; avoid over-templating. Use `auto` + `decltype` sparingly.

## Standard Containers You’ll See
- `std::vector`, `SmallVector` (LLVM): stack-optimized.
- `DenseMap`, `DenseSet` (LLVM): perf-oriented maps/sets.
- `SmallPtrSet`: small, pointer-keyed set.
```cpp
llvm::DenseMap<const llvm::Value*, int> Index;
llvm::SmallVector<llvm::Instruction*, 8> Worklist;
```

## String Handling
- `std::string` vs `llvm::StringRef` (non-owning view).
```cpp
void foo(llvm::StringRef name); // no copy; caller owns storage
```

## Memory and Alignment Awareness
- Backends care about layout; use `alignof`, `std::aligned_alloc` when relevant.

## Build System Notes
- CMake targets: `add_library`, `add_executable`, `add_llvm_pass_plugin`.
- Set C++ standard: `set(CMAKE_CXX_STANDARD 17)` or as required.

## Logging/Streams (LLVM Style)
- Use `llvm::errs()`, `llvm::outs()`; supports `<<`.
```cpp
llvm::errs() << "Visiting: " << F.getName() << "\n";
```

## Common LLVM Types to Recognize
- `Module`, `Function`, `BasicBlock`, `Instruction`, `Value`, `Type`, `IRBuilder`.
- `ArrayRef<T>`: lightweight view of a contiguous range.
- `Optional<T>` (or `std::optional`), `Expected<T>`, `Twine` (string concat helper).

## Threading and Concurrency
- When present, prefer RAII locks (`std::lock_guard<std::mutex>`). LLVM often opts for single-threaded passes unless specified.

## Style Tips in LLVM Context
- Prefer pre-increment (`++it`) for iterators.
- Avoid raw `new/delete`; use RAII/smart pointers or value types.
- Keep functions short; pass by reference where possible; use `const` aggressively.

