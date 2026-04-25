# ==============================================================================
# Lab 01: Foundation Makefile
# ==============================================================================

# Variables (Standard practices)
CC     := gcc
CFLAGS := -std=c11 -Wall -Wextra -Wpedantic -O2

# 1. The Default Target
# By convention, 'all' is the first target and is run when you just type 'make'.
all: app

# 2. Linking
# 'app' depends on 'main.o'. If 'main.o' changes, we must relink 'app'.
app: main.o
	@echo "Linking binary: $@"
	$(CC) main.o -o app

# 3. Compiling
# 'main.o' depends on the source file. If the source changes, we recompile.
main.o: src/main.c
	@echo "Compiling source: $<"
	$(CC) $(CFLAGS) -c src/main.c -o main.o

# 4. Utility Targets
# 'run' is a convenience target. It depends on 'app', ensuring it's built first.
run: app
	@echo "Executing app..."
	./app

# 'clean' removes build artifacts.
clean:
	@echo "Cleaning up..."
	rm -f app main.o

# 5. Phony Targets
# We declare 'all', 'run', and 'clean' as .PHONY because they aren't real files.
# This prevents issues if someone creates a file named 'clean' in this folder.
.PHONY: all run clean
