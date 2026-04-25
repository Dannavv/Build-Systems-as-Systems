# Lab 07: Advanced Functions

[← Prev: 06-Conditionals](../06-conditionals/README.md) | [Home](../README.md) | [Next: 08-Metaprogram →](../08-metaprogramming/README.md)

---

## Objective
Harness Make's built-in functions to perform complex data processing on file lists and environment data.

## Core Concepts

### 1. `$(filter PATTERN..., TEXT)`
Keeps only the words in `TEXT` that match any of the `PATTERN` words.
```makefile
SOURCES := main.c utils.c test.c
STAGING := $(filter %.c, $(SOURCES))
```

### 2. `$(foreach VAR, LIST, TEXT)`
Iterates over a list and performs a transformation.
```makefile
DIRS := src include tests
EXISTS := $(foreach dir, $(DIRS), $(wildcard $(dir)/*))
```

### 3. `$(shell COMMAND)`
Executes a shell command and returns its output. This is how you bridge Make with the OS.
```makefile
GIT_HASH := $(shell git rev-parse --short HEAD)
```

### 4. `$(sort LIST)`
Sorts the words in `LIST` alphabetically and **removes duplicates**.

---

## Guided Exercise
1.  **Analyze**: Look at the `Makefile` and how it filters out "test" files from the production build.
2.  **Verify**: Run `make info`. See how it uses `shell` to get the current date and git status.
3.  **Process**: Run `make`. It will only build the non-test files.

## Challenges
1.  **Inverse Filter**: Use `$(filter-out ...)` to create a list of ONLY test files.
2.  **Safe Shell**: What happens to the `shell` command if the command fails? Try using `$(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")`.

---
[← Prev: 06-Conditionals](../06-conditionals/README.md) | [Home](../README.md) | [Next: 08-Metaprogram →](../08-metaprogramming/README.md)
