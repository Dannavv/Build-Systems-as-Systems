# Lab 03: Pattern Rules & Wildcards

[← Prev: 02-Variables](../02-variables-functions/README.md) | [Home](../README.md) | [Next: 04-Auto-Deps →](../04-auto-deps/README.md)

---

## Objective
Learn how to write generic rules that apply to many files, allowing your build system to scale.

## Core Concepts

### 1. Source Discovery: `wildcard`
Automatically find all source files:
```makefile
SOURCES := $(wildcard src/*.c)
```

### 2. Pattern Rules: `%`
A template rule that matches file patterns:
```makefile
build/%.o: src/%.c
	$(CC) -c $< -o $@
```
- `%` matches the "stem" (e.g., if target is `build/main.o`, the stem is `main`).
- This replaces the need to write separate rules for every `.c` file.

---

## Guided Exercise
1.  **Build**: Run `make`.
2.  **Scale**: Run `touch src/extra.c` and run `make`. It should automatically detect and compile the new file.
3.  **Debug**: Run `make -d` to see how Make matches patterns.

## Challenges
1.  **Implicit Rules**: What happens if you remove the pattern rule from the Makefile?
2.  **Naming**: Change the pattern to `obj/%.o`. What else must you change?

---
[← Prev: 02-Variables](../02-variables-functions/README.md) | [Home](../README.md) | [Next: 04-Auto-Deps →](../04-auto-deps/README.md)
