# ==============================================================================
# Lab 02: Variables & Functions
# ==============================================================================

# ?= Only sets the variable if it's not already defined (e.g. by an env var)
CC     ?= gcc
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -O2

# := Evaluates the value immediately (Immediate Expansion)
BUILD_DIR := build
SRC_DIR   := src
SOURCES   := main.c util.c

# patsubst transforms a list of strings. 
# Here: main.c util.c -> build/main.o build/util.o
OBJECTS   := $(patsubst %.c,$(BUILD_DIR)/%.o,$(SOURCES))
APP       := app

all: $(APP)

# $@ is an automatic variable representing the target (app)
$(APP): $(OBJECTS)
	@echo "Linking with $(CC): $@"
	$(CC) $(OBJECTS) -o $@

# | starts order-only prerequisites. 
# $(BUILD_DIR) must exist, but changing the directory's timestamp won't trigger a recompile.
$(BUILD_DIR)/main.o: $(SRC_DIR)/main.c $(SRC_DIR)/util.h | $(BUILD_DIR)
	@echo "Compiling main: $<"
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/util.o: $(SRC_DIR)/util.c $(SRC_DIR)/util.h | $(BUILD_DIR)
	@echo "Compiling util: $<"
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR):
	mkdir -p $@

# A debug target to inspect state
print-vars:
	@printf 'SOURCES = %s\n' "$(SOURCES)"
	@printf 'OBJECTS = %s\n' "$(OBJECTS)"

run: $(APP)
	./$(APP)

clean:
	rm -rf $(BUILD_DIR) $(APP)

.PHONY: all print-vars run clean
