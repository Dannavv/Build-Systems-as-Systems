# Lab 05: Workflows & Debugging

[← Prev: 04-Auto-Deps](../04-auto-deps/README.md) | [Home](../README.md) | [Next: 06-Conditionals →](../06-conditionals/README.md)

---

## Objective
Create professional developer workflows and learn how to debug complex Makefiles.

## Core Concepts

### 1. UX Targets
A good Makefile should provide high-level targets for daily work:
- `make check`: Run linters/tests.
- `make install`: Deploy the binary.
- `make info`: Show version and configuration.

### 2. Debugging Techniques
- `make -n`: Dry run.
- `make -p`: Print the entire internal database (rules and variables).
- `make -d`: Detailed debug output (why Make decided to run a rule).
- `$(info ...)`: Print a message during the Makefile parsing phase.

### 3. Silencing Recipes
Using `@` before a command prevents Make from echoing the command string to the terminal.
```makefile
clean:
	@echo "Cleaning..."
	@rm -rf build/
```

---

## Guided Exercise
1.  **Info**: Run `make show`. This uses the `$(info)` function to print variables.
2.  **Dry Run**: Run `make run -n`.
3.  **Internal Database**: Run `make -p > database.txt` and search for your targets in the generated file.

## Challenges
1.  **Variable Origin**: Run `make -p` and look for the variable `CC`. Where did it come from?
2.  **Verbosity**: Add a variable `V=1`. Change your recipes to only be silent if `V` is NOT set.

---
[← Prev: 04-Auto-Deps](../04-auto-deps/README.md) | [Home](../README.md) | [Next: 06-Conditionals →](../06-conditionals/README.md)
