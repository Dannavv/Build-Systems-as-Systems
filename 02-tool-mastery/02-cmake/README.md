# Lab M2: CMake As A Graph Compiler

## Goal
Learn how CMake describes a build graph, how targets propagate usage requirements, and how a single PUBLIC versus PRIVATE decision can change whether downstream code compiles.

This lab treats CMake as a graph compiler: it does not build directly itself, but generates a build system that knows how to build the graph correctly.

## Why This Matters
CMake is not the same kind of tool as Make.

- Make executes rules directly from timestamps and prerequisites.
- CMake describes the graph and generates build files for another tool to execute.

That means CMake is about expressing relationships cleanly so the generated build system can propagate include paths, compile features, and link requirements to the right consumers.

## What You Build
A tiny C++ project with:
- one library target
- one executable target
- one correct CMake configuration
- one buggy CMake configuration

The code prints a build label, a sum, and a product.

## Files
- [src/main.cpp](src/main.cpp): executable entry point
- [src/calculator.cpp](src/calculator.cpp): library implementation
- [include/lab/calculator.hpp](include/lab/calculator.hpp): public library header
- [correct/CMakeLists.txt](correct/CMakeLists.txt): correct target propagation
- [buggy/CMakeLists.txt](buggy/CMakeLists.txt): intentionally broken propagation
- [CMAKE_TOOL_DETAILS.md](CMAKE_TOOL_DETAILS.md): CMake tool details, use cases, and workflow
- [CMAKE_SYNTAX_CORRECT.md](CMAKE_SYNTAX_CORRECT.md): syntax + structure guide for the correct CMake file
- [CMAKE_SYNTAX_BUGGY.md](CMAKE_SYNTAX_BUGGY.md): syntax + structure guide for the buggy CMake file

## Read These Together
- [correct/CMakeLists.txt](correct/CMakeLists.txt) with [CMAKE_SYNTAX_CORRECT.md](CMAKE_SYNTAX_CORRECT.md)
- [buggy/CMakeLists.txt](buggy/CMakeLists.txt) with [CMAKE_SYNTAX_BUGGY.md](CMAKE_SYNTAX_BUGGY.md)
- [README.md](README.md) with [CMAKE_TOOL_DETAILS.md](CMAKE_TOOL_DETAILS.md) for tool-level context and use cases

## Build Graph
Correct graph:

`calculator library -> cmake_lab executable`

The library exports its include directory publicly, so the executable can compile against the library header.

Buggy graph:

`calculator library -> cmake_lab_buggy executable`

The buggy version keeps the include directory PRIVATE, so the executable does not receive the header path and fails to compile.

## Core Idea
The most important concept in this lab is target propagation.

A target can carry usage requirements to its consumers:
- include directories
- compile features
- compile definitions
- link dependencies

If those requirements are marked PUBLIC or INTERFACE, consumers inherit them. If they are PRIVATE, the target uses them internally but consumers do not.

That is the graph abstraction layer in CMake.

## Correct Configuration
Open [correct/CMakeLists.txt](correct/CMakeLists.txt) and read it as a build graph description.

The library target declares:
- its source file
- its public include directory
- its language standard feature requirement

The executable target declares:
- its source file
- that it links against the library

Because the include directory is PUBLIC, the executable gets the library header path automatically through the dependency edge.

## Buggy Configuration
Open [buggy/CMakeLists.txt](buggy/CMakeLists.txt) and compare it with the correct version.

The bug is subtle:
- the library still knows where its headers are
- but the include directory is marked PRIVATE
- so the executable does not inherit the include path

That means `main.cpp` cannot find `lab/calculator.hpp` when the build tries to compile the executable target.

This is a target propagation bug, not a source-code bug.

## How To Run The Correct Build
From [correct](correct):
```bash
cmake -S . -B build
cmake --build build
./build/cmake_lab
```

Expected output:
- the label from the library
- `sum=7`
- `product=12`

## How To See The Bug
From [buggy](buggy):
```bash
cmake -S . -B build
cmake --build build
```

Expected result:
- CMake configures successfully
- the build fails when compiling the executable because the header path is missing

## Algorithm
Think about CMake in three stages:
1. Define targets.
2. Attach usage requirements to targets.
3. Generate a concrete build system that preserves those relationships.

This is why target scope matters so much.

If you attach something PUBLIC, consumers inherit it.
If you attach something PRIVATE, only the target itself sees it.

## Demo Flow
### Correct Project
1. Configure the project.
2. Build the project.
3. Run the executable.

What you should observe:
- the library builds
- the executable compiles successfully
- the executable links and runs

### Buggy Project
1. Configure the project.
2. Build the project.

What you should observe:
- configuration succeeds
- library compilation succeeds
- executable compilation fails because the public header is not visible

## Test Cases And What They Prove
| Test / Check | What It Proves |
| --- | --- |
| Correct configure | CMake can generate a build system from the graph |
| Correct build | PUBLIC include directories propagate to consumers |
| Correct run | The generated graph produces a working executable |
| Buggy configure | The graph can still be syntactically valid even when it is semantically wrong |
| Buggy build failure | PRIVATE include directories do not propagate to consumers |

## Expected Learning Outcomes
After this lab, you should be able to explain:
1. Why CMake is a graph compiler rather than a direct builder.
2. How PUBLIC and PRIVATE change dependency propagation.
3. Why target usage requirements matter more than global include paths.
4. Why a graph can be valid in syntax but wrong in behavior.

## Practical Takeaway
This lab shows the central CMake lesson:

1. Model code as targets.
2. Put dependencies on targets, not on global state.
3. Use PUBLIC when consumers need the requirement.
4. Use PRIVATE when only the target itself needs it.
5. Debug build failures by checking target propagation first.

## Next Step
The next lab can move to Ninja, where the generated graph gets executed as fast as possible with minimal build logic.
