# ==============================================================================
# Lab 07: Advanced Functions
# ==============================================================================

# 1. Shell integration
DATE     := $(shell date +%Y-%m-%d)
# We use ?= to allow overrides if git isn't available
GIT_VER  ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo "v1.0.0")

# 2. List manipulation
ALL_FILES := main.c util.c test_suite.c mock_db.c
# Filter out anything starting with test_ or mock_
PROD_SRCS := $(filter-out test_% mock_%, $(ALL_FILES))
# Filter in only things ending in .c
STRICT_C  := $(filter %.c, $(ALL_FILES))

all:
	@echo "Date: $(DATE)"
	@echo "Git:  $(GIT_VER)"
	@echo "Production Sources: $(PROD_SRCS)"

info:
	@echo "All Files:    $(ALL_FILES)"
	@echo "Filtered (.c): $(STRICT_C)"
	@echo "Sorted Unique: $(sort $(ALL_FILES) main.c)"

.PHONY: all info
