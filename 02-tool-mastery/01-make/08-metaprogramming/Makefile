# ==============================================================================
# Lab 08: Metaprogramming
# ==============================================================================

APPS := client server worker

all: $(APPS)

# 1. Define a template (the 'function')
# $(1) will be the app name
define GENERATE_RULE
$(1): src/$(1).c
	@echo "Dynamic build for [$(1)]"
	gcc src/$(1).c -o $(1)
endef

# 2. Use eval and foreach to instantiate the template for every app
# This loop 'types' the rules into the Makefile for us!
$(foreach app,$(APPS),$(eval $(call GENERATE_RULE,$(app))))

# 3. View the generated code (for debugging)
show-generated:
	$(foreach app,$(APPS),$(info $(call GENERATE_RULE,$(app))))

clean:
	rm -f $(APPS)

.PHONY: all clean show-generated
