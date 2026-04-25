# ==============================================================================
# Lab 10: Recursive Orchestration (Root)
# ==============================================================================

SUBDIRS := core ui

# 1. Export variables to sub-makes
export CC     := gcc
export CFLAGS := -Wall -O2

all: $(SUBDIRS)

# 2. The recursive pattern
$(SUBDIRS):
	@echo "--- Entering subdirectory [$@] ---"
	$(MAKE) -C $@

clean:
	$(foreach dir,$(SUBDIRS),$(MAKE) -C $(dir) clean;)

.PHONY: all $(SUBDIRS) clean
