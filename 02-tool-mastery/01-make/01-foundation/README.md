# Lab 01: The Foundation

[← Back to Home](../README.md) | [Next: 02-Variables →](../02-variables-functions/README.md)

---

## Objective
Understand the basic structure of a Make rule and how Make decides when to run a command.

## Core Concepts

### 1. The Rule Anatomy
A rule consists of three parts:
```makefile
target: prerequisites
	recipe
```
- **Target**: Usually a file to be generated (or a label like `clean`).
- **Prerequisites**: Files that the target depends on.
- **Recipe**: Shell commands to create the target. **Must start with a TAB.**

### 2. The Execution Logic
When you run `make target`:
1. Look for a rule for `target`.
2. Check if `target` exists on disk.
3. Check if all `prerequisites` exist. If they have rules, run them first (recursion).
4. **The Decision**: If `target` is missing OR any `prerequisite` is newer than `target`, execute the recipe.

### 3. Phony Targets
Targets that don't represent real files (like `clean` or `run`) should be marked as `.PHONY`.
```makefile
.PHONY: clean
clean:
	rm -f app main.o
```
This ensures `make clean` works even if a file named `clean` exists in the directory.

---

## Guided Exercise
1. **Explore**: Look at the `Makefile` and `src/main.c`.
2. **Build**: Run `make`.
3. **Idempotency**: Run `make` again. It should say `up to date`.
4. **Change**: Run `touch src/main.c` and run `make`. It rebuilds.
5. **Clean**: Run `make clean`.

## Challenges
1.  **Default Target**: Why does `make` run `all` by default?
2.  **Dry Run**: Use `make -n` to see what would happen.
3.  **Break Phony**: Remove `.PHONY` from the Makefile, run `touch clean`, and try `make clean`. What happens?

---
[← Back to Home](../README.md) | [Next: 02-Variables →](../02-variables-functions/README.md)
