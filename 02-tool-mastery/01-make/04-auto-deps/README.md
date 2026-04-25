# Lab 04: Automatic Dependencies

[← Prev: 03-Patterns](../03-pattern-rules/README.md) | [Home](../README.md) | [Next: 05-Workflows →](../05-workflows-debug/README.md)

---

## Objective
Solve the "Header Problem": Ensuring that changing a `.h` file triggers a recompile of any `.c` file that includes it, without manually listing dependencies.

## Core Concepts

### 1. The Header Problem
By default, Make only knows about what you list in the prerequisites. If `main.c` includes `config.h`, but the Makefile only lists `main.o: main.c`, then changing `config.h` will **not** trigger a rebuild.

### 2. Compiler Generation (`-MMD`)
Modern compilers (GCC/Clang) can generate dependency rules for you while they compile.
- `-MMD`: Generate a `.d` file with the dependencies.
- `-MP`: Add a phony target for each dependency to prevent errors if a header is deleted.

### 3. Including `.d` Files
The `include` directive tells Make to read other fragments into the Makefile.
```makefile
-include $(DEPS)
```
The `-` prefix tells Make to ignore errors if the files don't exist yet (which happens on the first build).

---

## Guided Exercise
1.  **Inspect**: Look at the `CPPFLAGS` and the `-include` line in the `Makefile`.
2.  **Build**: Run `make`. Check the `build/` directory for `.d` files.
3.  **Test**: Open `src/util.h` and change a value. Run `make`. It should rebuild the relevant files!
4.  **Compare**: Delete the `-include` line and repeat the test. What happens?

## Challenges
1.  **Dependency Content**: Open a `.d` file. What does the syntax look like? Does it look like a Make rule?
2.  **Phony Headers**: Why do we use `-MP`? (Try deleting a header file and running `make` without `-MP`).

---
[← Prev: 03-Patterns](../03-pattern-rules/README.md) | [Home](../README.md) | [Next: 05-Workflows →](../05-workflows-debug/README.md)
