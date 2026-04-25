CC ?= gcc
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -O2
APP := app

all: $(APP)

$(APP): src/main.c
	$(CC) $(CFLAGS) $< -o $@

run: $(APP)
	./$(APP)

check:
	@printf 'check: static checks placeholder\n'

package: $(APP)
	@printf 'package: creating release artifact placeholder\n'

show:
	@printf 'Use `make -n` for dry-run, `make -B` to force rebuild, `make -j` for parallel jobs.\n'

clean:
	rm -f $(APP)

.PHONY: all run check package show clean
