# Lab 10: Recursive Make & Orchestration

[← Prev: 09-Scoping](../09-target-variables/README.md) | [Home](../README.md)

---

## Objective
Learn how to manage large projects by delegating build tasks to sub-directories.

## Core Concepts

### 1. Recursive Make
This involves calling `make` from within a `Makefile`.
```makefile
subsystem:
	$(MAKE) -C subdir
```
- `-C subdir`: Tells Make to change directory to `subdir` before looking for a Makefile.
- `$(MAKE)`: **Crucial.** Always use the variable `$(MAKE)`, never the literal command `make`. This ensures flags (like `-j`) are passed down correctly.

### 2. Passing Variables (`export`)
By default, variables are not shared with sub-makes. Use `export` to make them available.
```makefile
export CC CFLAGS
```

### 3. The "Recursive Make Considered Harmful" Debate
While easy to use, recursive make can lead to incorrect dependency tracking across directories. In very advanced systems, people use "Non-recursive Make" (including all sub-Makefiles into one), but Recursive Make remains the standard for most Linux projects.

---

## Guided Exercise
1.  **Structure**: Notice we have a `core/` and a `ui/` directory, each with its own `Makefile`.
2.  **Orchestrate**: Run `make` in the root. Watch how it "descends" into each directory and runs their respective builds.
3.  **Parallelism**: Run `make -j4`. Notice how the parallel flag is passed down to the sub-makes automatically.

## Challenges
1.  **Top-Down Flags**: Change a variable in the root Makefile and `export` it. Check if the sub-directories respect the change.
2.  **Clean Up**: Add a `clean` target to the root that calls `make clean` in all sub-directories.

---
[← Prev: 09-Scoping](../09-target-variables/README.md) | [Home](../README.md)
