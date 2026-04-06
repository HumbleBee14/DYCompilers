cmake_minimum_required(VERSION 3.20)
project(toyc-ch1 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Point to our local LLVM 19.1.0 build (not system LLVM)
set(LLVM_DIR "/home/humblebee/DYCompilers/external/llvm-project/build/install/lib/cmake/llvm")
set(MLIR_DIR "/home/humblebee/DYCompilers/external/llvm-project/build/install/lib/cmake/mlir")

# Prevent CMake from finding system LLVM
set(CMAKE_FIND_USE_SYSTEM_ENVIRONMENT_PATH OFF)

find_package(LLVM REQUIRED CONFIG NO_DEFAULT_PATH PATHS ${LLVM_DIR})
find_package(MLIR REQUIRED CONFIG NO_DEFAULT_PATH PATHS ${MLIR_DIR})

message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")
message(STATUS "Using MLIRConfig.cmake in: ${MLIR_DIR}")

include_directories(${LLVM_INCLUDE_DIRS})
include_directories(${MLIR_INCLUDE_DIRS})

# Match LLVM's build flags (LLVM is built with -fno-rtti)
if(NOT LLVM_ENABLE_RTTI)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-rtti")
endif()

add_executable(toyc-ch1
  toyc.cpp
  parser/AST.cpp
)

target_include_directories(toyc-ch1 PRIVATE include/)

# Link LLVM and MLIR libraries
target_link_libraries(toyc-ch1 PRIVATE
  LLVMSupport
  MLIRSupport
)
