# The content of the Master Battle Plan

---
NOTE: We are doing a crash course in LLVM compiler engineer for new grad! You have to help the user by providing a detailed Master Battle Plan that includes projects, learning objectives, and a schedule to achieve the goal in 24 hours.name: LLVM Engineer in 24 Hours
description: A detailed Master Battle Plan to become an LLVM Compiler Engineer in 24 hours.
Goal: Teach the user how to become an LLVM Compiler Engineer in 24 hours through targeted projects and learning objectives.
---

# LLVM Engineer in 24 Hours: Master Battle Plan

**Goal:** Go from "Java Developer" to "LLVM Compiler Engineer Candidate" in 24 hours.
**Target Role:** Compiler Engineer at Cerebras (Systems + ML).
**Strategy:** Build two specific projects that prove you understand the full compiler stack (Middle-end & Backend) and can optimize for AI hardware.

---

## 1. The Architecture & Roadmap
You are building pieces of the pipeline highlighted below.

| Phase | Project Name | What You Learn | Interview Buzzwords |
| :--- | :--- | :--- | :--- |
| **Middle-End** | **`TracePass`** | How to read/modify IR, C++ Casting, IRBuilder. | *Pass Manager, BasicBlock, SSA, Dominators, Instrumentation.* |
| **Backend** | **`RISCV-AI`** | How to map math to hardware, TableGen, ML Kernels. | *Instruction Selection, DAG Matching, TableGen, Fused-Multiply-Add.* |

---

## 2. Project 1: The Middle-End (The "TracePass")
**Objective:** Create a compiler pass that automatically injects `printf("Entering function...")` at the start of every C function.

### Core Concepts to Master
* **The Module:** The container for all code (like a Java "File").
* **The Function:** A list of Basic Blocks.
* **The Basic Block:** A list of Instructions that run linearly.
* **`IRBuilder`:** The cursor object used to insert new instructions.

### Execution Steps
1.  **Setup:** Install LLVM (via `apt` or `brew`) and set up `CMakeLists.txt`.
2.  **Coding:**
    * Get the `printf` function reference using `M.getOrInsertFunction()`.
    * Iterate: `for (auto &F : M)`.
    * Set Builder: `Builder.SetInsertPoint(&F.getEntryBlock().front())`.
    * Create Global String: `Builder.CreateGlobalStringPtr(...)`.
    * Inject Call: `Builder.CreateCall(...)`.
3.  **Validation:** Run on `test.c` and see the logs print when you execute the binary.

---

## 3. Project 2: The Backend (The "AI Accelerator")
**Objective:** Modify the real RISC-V backend to support a fictional AI instruction (`AI_MAC`) and prove the compiler uses it automatically for Matrix Multiplication.

### Core Concepts to Master
* **TableGen (`.td`):** The language used to describe hardware.
* **Instruction Selection (ISel):** Pattern matching IR graphs to Machine Instructions.
* **Hardware/Software Co-design:** Designing instructions that fit software needs (ML).

### Execution Steps
1.  **Setup:** Download LLVM Source (`git clone`) and build `llc` (the backend compiler).
2.  **TableGen Hacking (`RISCVInstrInfo.td`):**
    * **Define Hardware:** Create the `AI_MAC` instruction definition (Input: 3 registers, Output: 1 register).
    * **Define Logic:** Write the **Pattern Match**:
      ```tablegen
      def : Pat<(add (mul GPR:$a, GPR:$b), GPR:$c),
                (AI_MAC GPR:$a, GPR:$b, GPR:$c)>;
      ```
3.  **Validation (The "ML Demo"):**
    * Write `matmul.c` (Standard Matrix Multiplication loops).
    * Compile using your custom backend.
    * **Success Criteria:** Open the assembly (`.s`) file. If you see `ai_mac` inside the inner loop, you win.

---

## 4. Interview Cheat Sheet
Use these exact translations from your Java brain to Compiler terms.

| If you want to say... | Say this instead (Compiler Terminology) |
| :--- | :--- |
| "I used `instanceof` to check if it was a Load instruction." | "I used **`dyn_cast<LoadInst>`** to safely check the instruction type." |
| "I looped through the code." | "I **iterated over the Basic Blocks** in the Control Flow Graph." |
| "I inserted a new line of code." | "I **instrumented the IR** by inserting call instructions using the **IRBuilder**." |
| "I told it to replace a+b*c with my special instruction." | "I wrote a **DAG Pattern Match** in **TableGen** to handle **Instruction Selection** for a fused operation." |
| "It works for matrix math." | "I verified the backend by compiling a **GEMM kernel** and checking that the loops were optimized to use the **custom ISA extension**." |

---

## 5. The 24-Hour Schedule

* **Hour 0-2 (Project 1 Setup):** Get `CMakeLists.txt` working. Run "Hello World" pass.
* **Hour 2-5 (Project 1 Logic):** Implement `TracePass.cpp`. Debug the C++ errors.
* **Hour 5-6 (Break/Build):** Start the **LLVM Source Build** (for Project 2). Go eat/sleep.
* **Hour 7-10 (Project 2 Backend):** Modify `RISCVInstrInfo.td`. Add `AI_MAC`. Rebuild `llc`.
* **Hour 10-12 (Project 2 ML Demo):** Write `matmul.c`. Compile it. Debug why the pattern isn't matching.
* **Hour 12+ (Practice):** Read the Cheat Sheet. Rehearse your story.
