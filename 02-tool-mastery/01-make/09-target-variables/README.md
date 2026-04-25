# Lab 09: Target-Specific Variables (Scoping)

[← Prev: 08-Metaprogram](../08-metaprogramming/README.md) | [Home](../README.md) | [Next: 10-Large Scale →](../10-recursive-make/README.md)

---

## Objective
Learn how to limit the scope of a variable so it only applies when a specific target is being built. This is essential for mixed-mode builds (e.g., building one tool with optimizations and another with debug symbols).

## Core Concepts

### 1. Global Scoping (The Default)
Variables defined at the top level apply to all rules.

### 2. Target-Specific Scoping
You can assign a variable for only one target and its prerequisites:
```makefile
target: VARIABLE = value
```
Example:
```makefile
debug_tool: CFLAGS = -g
debug_tool: main.o
```
In this case, `CFLAGS` will be `-g` **only** during the execution of the `debug_tool` recipe and its prerequisites.

### 3. Pattern-Specific Variables
You can even apply variables to groups of files:
```makefile
%.o: CFLAGS += -fPIC
```

---

## Guided Exercise
1.  **Observe**: Look at the `Makefile`. We have two apps: `fast_app` and `safe_app`.
2.  **Build Both**: Run `make`.
3.  **Check Output**: Notice that `fast_app` used `-O3` while `safe_app` used `-O0 -Wall`. They both used the same generic pattern rule, but the variables were swapped based on the **target context**.

## Challenges
1.  **Prerequisite Check**: Does a target-specific variable apply to the prerequisites? (Hint: Build `safe_app` and check if the `.o` compilation used the specific flags).
2.  **Overrides**: What happens if you define a global `CFLAGS` and a target-specific `CFLAGS`? Which one wins?

---
[← Prev: 08-Metaprogram](../08-metaprogramming/README.md) | [Home](../README.md) | [Next: 10-Large Scale →](../10-recursive-make/README.md)
