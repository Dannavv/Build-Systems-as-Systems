# Lab 08: Metaprogramming (The Powerhouse)

[← Prev: 07-Functions](../07-advanced-functions/README.md) | [Home](../README.md) | [Next: 09-Scoping →](../09-target-variables/README.md)

---

## Objective
Learn how to write code that writes code. This is the "God Mode" of Make, allowing you to generate complex rules for multiple components automatically.

## Core Concepts

### 1. `$(call VARIABLE, PARAM1, PARAM2...)`
The `call` function allows you to treat a variable as a function template.
```makefile
define my_template
    @echo "Hello $(1), welcome to $(2)"
endef

greet:
	$(call my_template, User, Make)
```

### 2. `$(eval ...)`
The `eval` function takes a string and **inserts it into the Makefile** as if you had typed it. It is evaluated by the Make parser at runtime.

### 3. Dynamic Rule Generation
By combining `foreach` and `eval`, you can generate rules for dozens of binaries without repeating yourself.
```makefile
define build_app
$(1): $(1).c
	gcc $(1).c -o $(1)
endef

$(foreach app, $(APPS), $(eval $(call build_app, $(app))))
```

---

## Guided Exercise
1.  **Analyze**: Look at the `Makefile`. Notice there is **no explicit rule** for `app_one`, `app_two`, or `app_three`.
2.  **Verify**: Run `make`. Watch how Make dynamically generates and executes rules for all three apps.
3.  **Scale**: Add `app_four` to the `APPS` variable. Run `make` again. It just works!

## Challenges
1.  **Unique Flags**: Modify the `build_app` template so that each app can have its own custom flags (e.g., `app_one_FLAGS := -lm`).
2.  **The Debugger**: Use `$(info ...)` wrapped around your `call` to see exactly what string `eval` is injecting into your Makefile.

---
[← Prev: 07-Functions](../07-advanced-functions/README.md) | [Home](../README.md) | [Next: 09-Scoping →](../09-target-variables/README.md)
