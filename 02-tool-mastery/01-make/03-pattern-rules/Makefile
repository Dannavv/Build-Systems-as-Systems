CC ?= gcc
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -O2
SRC_DIR := src
BUILD_DIR := build
SOURCES := $(wildcard $(SRC_DIR)/*.c)
OBJECTS := $(patsubst $(SRC_DIR)/%.c,$(BUILD_DIR)/%.o,$(SOURCES))
APP := app

all: $(APP)

$(APP): $(OBJECTS)
	$(CC) $(OBJECTS) -o $@

# One pattern rule compiles every C file into its matching object file.
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR):
	mkdir -p $@

run: $(APP)
	./$(APP)

clean:
	rm -rf $(BUILD_DIR) $(APP)

.PHONY: all run clean
