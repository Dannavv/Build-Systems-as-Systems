# Lab 02: Variables and Functions

[← Prev: 01-Foundation](../01-foundation/README.md) | [Home](../README.md) | [Next: 03-Patterns →](../03-pattern-rules/README.md)

---

## Objective
Learn how to use variables and string manipulation functions to make your Makefiles DRY (Don't Repeat Yourself).

## Core Concepts

### 1. Variable Assignment Types
- `VAR = value` (Lazy): Evaluated every time it's used.
- `VAR := value` (Immediate): Evaluated once at the start. **Recommended.**
- `VAR ?= value` (Conditional): Assign only if not already set (allows command-line overrides).

### 2. Automatic Variables (The Magic)
Make provides special variables based on the rule context:
- `$@`: The name of the **target**.
- `$<`: The **first prerequisite**.
- `$^`: **All** prerequisites.
- `$*`: The "stem" matched by a pattern rule (learned in Lab 03).

### 3. String Manipulation: `patsubst`
Transforms a list of strings based on a pattern:
```makefile
OBJECTS := $(patsubst %.c, build/%.o, $(SOURCES))
```

### 4. Order-Only Prerequisites
```makefile
target: normal_prereqs | order_only_prereqs
```
The target depends on the existence of `order_only_prereqs`, but their timestamps won't trigger a rebuild. Perfect for creating directories.

---

## Guided Exercise
1.  **Debug**: Run `make print-vars` to see expanded state.
2.  **Build**: Run `make`. Observe `$@` and `$<` in action.
3.  **Override**: Run `CC=clang make -B`.

## Challenges
1.  **The `all` Prerequisite**: Add a fake file to `SOURCES`. What does `print-vars` show?
2.  **Order-Only**: Delete the `build` directory and run `make`. How does the directory get created?

---
[← Prev: 01-Foundation](../01-foundation/README.md) | [Home](../README.md) | [Next: 03-Patterns →](../03-pattern-rules/README.md)
