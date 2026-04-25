# ==============================================================================
# Lab 09: Target-Specific Variables
# ==============================================================================

CC     := gcc
# Global CFLAGS
CFLAGS := -O2

all: fast_app safe_app

# 1. Target-Specific assignment
# These only apply when building 'fast_app'
fast_app: CFLAGS := -O3 -march=native
fast_app: main.c
	@echo "Building fast_app with [$(CFLAGS)]"
	$(CC) $(CFLAGS) main.c -o $@

# These only apply when building 'safe_app'
safe_app: CFLAGS := -O0 -g -Wall
safe_app: main.c
	@echo "Building safe_app with [$(CFLAGS)]"
	$(CC) $(CFLAGS) main.c -o $@

clean:
	rm -f fast_app safe_app

.PHONY: all clean
