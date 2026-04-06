#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/PassManager.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {

struct TracePass : public PassInfoMixin<TracePass> {
  PreservedAnalyses run(Module &module, ModuleAnalysisManager &) {
    LLVMContext &context = module.getContext();
    IRBuilder<> builder(context);

    // Declare (or fetch) `int printf(const char*, ...)` in the module.
    Type *i32 = Type::getInt32Ty(context);
    Type *i8 = Type::getInt8Ty(context);
    Type *i8Ptr = PointerType::getUnqual(i8);
    FunctionType *printfType = FunctionType::get(i32, {i8Ptr}, /*isVarArg=*/true);
    FunctionCallee printfFunc = module.getOrInsertFunction("printf", printfType);

    for (Function &function : module) {
      if (function.isDeclaration())
        continue;

      BasicBlock &entry = function.getEntryBlock();
      Instruction *insertBefore = &*entry.getFirstInsertionPt();
      builder.SetInsertPoint(insertBefore);

      std::string msg = "LOG: Entering function: " + function.getName().str() + "\n";
      GlobalVariable *globalStr = builder.CreateGlobalString(msg, "tracepass.msg", 0, &module);
      Value *zero = builder.getInt32(0);
      Value *formatStr = builder.CreateInBoundsGEP(globalStr->getValueType(), globalStr, {zero, zero});
      builder.CreateCall(printfFunc, {formatStr});
    }

    return PreservedAnalyses::none();
  }
};

} // namespace

extern "C" LLVM_ATTRIBUTE_WEAK PassPluginLibraryInfo llvmGetPassPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "TracePass", LLVM_VERSION_STRING,
          [](PassBuilder &pb) {
            pb.registerPipelineParsingCallback(
                [](StringRef name, ModulePassManager &mpm,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (name == "trace-pass") {
                    mpm.addPass(TracePass());
                    return true;
                  }
                  return false;
                });
          }};
}
