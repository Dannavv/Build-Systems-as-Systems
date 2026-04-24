# Lab T1: Build Your Own Mini-Make

## What This Lab Teaches
This lab shows how a build system decides:
1. What must be built first.
2. What can be skipped.
3. What must be rebuilt after a source change.

You will run a small Python build engine that behaves like a simplified `make`.

## What Is Happening In This Lab
The build graph is:

`hello.c -> hello.o -> hello.exe`

The script builds this graph in dependency order:
1. Check/build `hello.c` (source file).
2. Build `hello.o` from `hello.c` when needed.
3. Build `hello.exe` from `hello.o` when needed.

The decision is based on file modification times (`mtime`):
1. If a target does not exist, build it.
2. If any dependency is newer than the target, rebuild it.
3. Otherwise, skip it as up to date.

## How To Run
```bash
python3 main.py
```

## Expected Output Flow
The script demonstrates three build passes:
1. **First build**: builds everything (`hello.o`, then `hello.exe`).
2. **Second build**: should report targets as up to date.
3. **Third build**: after source modification, should rebuild the affected targets.

## Files In This Lab
- `main.py`: Mini build engine and demo runner.
- `hello.c`: C source file used by the demo.
- `hello.o`: Compiled object file.
- `hello.exe`: Final executable.

## Important Note
`main.py` rewrites `hello.c` at startup. This is intentional for demonstration, but it means manual edits to `hello.c` are overwritten on each run.

## How The Engine Works
The engine is intentionally small, but it follows the same core ideas as real build tools.

### 1. Rules Are Stored As A Build Graph
When `add_rule(target, deps, cmd)` is called, the engine saves this structure:

- key: target name (example: `hello.o`)
- value: dependency list + shell command

Conceptually, each rule is a node in a directed graph:

- `hello.o` depends on `hello.c`
- `hello.exe` depends on `hello.o`

This graph is acyclic in this lab, so a recursive traversal can safely terminate.

### 2. Build Starts From The Requested Final Target
Calling `build("hello.exe")` means:

1. Start at final artifact (`hello.exe`).
2. Recursively visit its dependencies before touching the target itself.
3. Return upward once each dependency is handled.

This is a depth-first traversal with post-order behavior (children first, parent after).

### 3. Leaf Handling: Source Files Without Rules
If a dependency is not present in `self.rules`, the engine treats it as a source/leaf node:

1. If the file exists (example: `hello.c`), it is considered satisfied.
2. If the file does not exist, the build fails immediately with an error.

This matches classic make behavior: no rule + missing file => cannot continue.

### 4. Freshness Check Uses Modification Time
After all dependencies for a target are processed, the engine decides whether the target is stale.

It computes:

- `target_mtime` via `get_mtime(target)`
- each dependency `mtime` via `get_mtime(dep)`

Decision logic:

1. If target is missing (`mtime == 0`), build is required.
2. If any dependency has newer `mtime` than target, rebuild is required.
3. Otherwise, target is up to date and command is skipped.

This is the incrementality rule that avoids unnecessary recompilation.

### 5. Command Execution Is Conditional And Strict
Only when `needs_build` is true, the engine runs the rule command:

`subprocess.run(rule['cmd'], shell=True, check=True)`

Important effects:

1. `shell=True` executes the command through the system shell.
2. `check=True` raises an exception on non-zero exit status.
3. A failed compile/link step stops the build immediately.

### 6. Why The Order Is Correct
For this lab graph:

1. `build("hello.exe")` calls `build("hello.o")`
2. `build("hello.o")` calls `build("hello.c")`
3. `hello.c` is leaf/exists => return
4. evaluate/build `hello.o`
5. return to `hello.exe`, evaluate/build `hello.exe`

So the guaranteed execution order is always:

`hello.c` check -> `hello.o` check/build -> `hello.exe` check/build

### 7. Why The Demo Has Three Passes
`main.py` demonstrates the incremental algorithm explicitly:

1. **First pass**: outputs are missing, so both targets build.
2. **Second pass**: mtimes show outputs are fresh, so both are skipped.
3. **Third pass**: source file is modified after a short sleep, so mtimes force rebuild.

The sleep is important because many filesystems have coarse timestamp granularity; without delay, changes may not appear as newer.

### 7.1 Run Trace Table (What Happens Per Pass)
Use this table to map each pass to engine decisions:

| Pass | Trigger Condition | `hello.c` (leaf) | `hello.o` decision | `hello.exe` decision | Expected Command Execution |
| --- | --- | --- | --- | --- | --- |
| 1. First build | Outputs do not exist yet | Exists and is accepted as source | Missing target, must build | Missing target, must build | `gcc -c hello.c -o hello.o` then `gcc hello.o -o hello.exe` |
| 2. Second build | No files changed since pass 1 | Exists and unchanged | Target newer than or equal to deps, skip | Target newer than or equal to deps, skip | No commands run |
| 3. Third build | `hello.c` modified after delay | Exists with newer mtime | Dependency newer than target, rebuild | Dependency (`hello.o`) newer than target, rebuild | `gcc -c hello.c -o hello.o` then `gcc hello.o -o hello.exe` |

Reading the table from left to right mirrors the engine flow:
1. Determine trigger condition.
2. Confirm leaf/source status.
3. Evaluate staleness for each generated target.
4. Run only the commands required by staleness.

### 8. Current Limitations (Intentional For Learning)
This lab engine keeps the model simple on purpose. It does not yet include:

1. cycle detection
2. parallel builds
3. pattern rules / wildcard rules
4. header dependency scanning
5. command caching or content hashing

Even without these features, the lab captures the foundational build-system algorithm used in practice.

## Prerequisites
- Python 3
- GCC available in your shell (`gcc --version`)
