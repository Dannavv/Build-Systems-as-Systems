# Lab 06: Conditionals & Configurations

[← Prev: 05-Workflows](../05-workflows-debug/README.md) | [Home](../README.md) | [Next: 07-Functions →](../07-advanced-functions/README.md)

---

## Objective
Learn how to use conditional logic to handle different build configurations (like Debug vs. Release).

## Core Concepts

### 1. Conditionals (`ifeq` / `ifneq`)
Make can branch its behavior based on variable values.
```makefile
ifeq ($(DEBUG), 1)
    CFLAGS += -g -O0
else
    CFLAGS += -O3
endif
```
- Note: Conditionals are evaluated during the **parsing phase**, not the execution phase.

### 2. Testing Definitions (`ifdef` / `ifndef`)
Checks if a variable is defined (even if it's empty).

### 3. Command Line Control
Conditionals allow users to pass parameters to the build:
`make DEBUG=1`

---

## Guided Exercise
1.  **Build Debug**: Run `make DEBUG=1`. Notice the compiler flags in the output.
2.  **Build Release**: Run `make DEBUG=0` (or just `make`). Notice the flags change to `-O3`.
3.  **Check Config**: Run `make config`. This uses a conditional to print the current mode.

## Challenges
1.  **OS Detection**: Use the `shell` command to detect the OS (e.g., `uname`) and use a conditional to change the `RM` command (e.g., `del` for Windows vs `rm` for Linux).
2.  **Required Variables**: Use `ifeq` combined with `$(error ...)` to stop the build if a required variable (like `VERSION`) is not provided.

---
[← Prev: 05-Workflows](../05-workflows-debug/README.md) | [Home](../README.md) | [Next: 07-Functions →](../07-advanced-functions/README.md)
