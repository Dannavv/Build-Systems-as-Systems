# ==============================================================================
# Lab 06: Conditionals
# ==============================================================================

CC     := gcc
APP    := app
SRC    := src/main.c

# Default to release mode
DEBUG ?= 0

# 1. Conditional Logic
ifeq ($(DEBUG), 1)
	MODE   := DEBUG
	CFLAGS := -g -O0 -DDEBUG
else
	MODE   := RELEASE
	CFLAGS := -O3
endif

all: $(APP)

$(APP): $(SRC)
	@echo "Building in [$(MODE)] mode..."
	$(CC) $(CFLAGS) $< -o $@

# 2. Informational target
config:
	@echo "Current Configuration:"
	@echo "  Mode:   $(MODE)"
	@echo "  Flags:  $(CFLAGS)"

clean:
	rm -f $(APP)

.PHONY: all config clean
