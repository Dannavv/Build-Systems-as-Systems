# Make Mastery Track

> [!NOTE]
> This is a progressive lab sequence designed to transition you from basic build scripts to mastering deterministic state transformation.

## What is Make?
At its core, `make` is a **DAG (Directed Acyclic Graph) execution engine**. It manages transformations based on file timestamps, ensuring that only what is necessary is rebuilt.

### The Mental Model
1. **Nodes**: Files (Targets and Prerequisites).
2. **Edges**: Dependencies (Relationships between files).
3. **Operations**: Recipes (Shell commands to transform prerequisites into targets).

---

## Curriculum Overview

### Phase 1: The Essentials
| Lab | Focus | Navigation |
| :--- | :--- | :--- |
| **01-Foundation** | Rule Anatomy & DAG | [Start Lab →](01-foundation/README.md) |
| **02-Variables** | Dry Principles & Functions | [Go to Lab →](02-variables-functions/README.md) |
| **03-Patterns** | Generic Rules (`%`) | [Go to Lab →](03-pattern-rules/README.md) |
| **04-Auto-Deps** | Compiler Integration | [Go to Lab →](04-auto-deps/README.md) |
| **05-Workflows** | UX & Debugging | [Go to Lab →](05-workflows-debug/README.md) |

### Phase 2: Advanced Mastery
| Lab | Focus | Navigation |
| :--- | :--- | :--- |
| **06-Conditionals** | Logic & Configs | [Go to Lab →](06-conditionals/README.md) |
| **07-Functions** | Data Processing | [Go to Lab →](07-advanced-functions/README.md) |
| **08-Metaprogram** | Dynamic Rule Generation | [Go to Lab →](08-metaprogramming/README.md) |
| **09-Scoping** | Target-Specific Vars | [Go to Lab →](09-target-variables/README.md) |
| **10-Large Scale** | Recursive Orchestration | [Go to Lab →](10-recursive-make/README.md) |

---

## Global Command Workflow
- `make`: Executes the first target (usually `all`).
- `make -j<N>`: Parallel execution.
- `make -n`: Dry run (show commands without executing).
- `make -B`: Force a full rebuild.

---
[Home](README.md) | [Next: 01-Foundation](01-foundation/README.md)
