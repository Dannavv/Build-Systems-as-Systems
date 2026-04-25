# Lab T2: Incremental Computation Engine

## Goal
Move from file timestamp rebuilds in Lab T1 to node-level incremental computation with caching.

This lab models a graph of pure transformations and recomputes only the affected nodes when inputs change.

## Why This Matters
This is the same core idea behind:
- Bazel action caching
- ML pipeline invalidation
- reactive UI and dataflow systems

If you understand this lab deeply, you understand the core shape of modern build and compute orchestration.

## What You Build
A Python engine that supports:
1. Source nodes for mutable inputs
2. Derived nodes computed from dependencies
3. Deterministic node signatures
4. Value and signature caches
5. Selective recomputation

The key question is not just whether a value exists in cache. The real question is:

> Which nodes are still valid, and which ones must be recomputed?

## Files
- `main.py`: Engine implementation and demos
- `tests.py`: Correctness and failure tests

## Engine Model
Each node has:
- `name`
- `deps`
- `compute(dep_values)`
- `is_source`

The runtime keeps:
- `value_cache[node]`: last computed value
- `signature_cache[node]`: last dependency or input signature
- `last_trace`: ordered list of trace entries containing:
  - `name`
  - `state` (`recomputed` or `cached`)
  - `signature`
  - `deps`

Signature rules:
- Source nodes hash their own current value.
- Derived nodes hash the signatures of their direct dependencies.
- If a node's signature matches the cached one, the cached value is reused.

This is the essential incremental-computation model:
1. The graph is explicit.
2. Invalidations flow through dependencies.
3. Reuse is allowed only when dependency signatures are unchanged.
4. Hidden inputs are bugs.

## Algorithm
When evaluating node `N`:
1. Recursively evaluate all dependencies first.
2. Build a deterministic signature for `N`.
3. Compare that signature against the cached signature for `N`.
4. If the signature matches and a cached value exists, reuse the cached value.
5. Otherwise recompute `N`, update the caches, and record the node as `recomputed`.

### Pseudocode
```text
run(target):
  evaluate all dependencies first

  signature = hash(current node state + dependency signatures)

  if signature matches previous signature and cached value exists:
    reuse cached value
    record cached in trace
  else:
    compute new value
    store value and signature in cache
    record recomputed in trace
```

### Why This Works
A derived node only depends on:
1. Its direct dependencies.
2. The current values of source nodes through those dependencies.

If none of those dependency signatures change, the node's output cannot change either.

## Demo Design
The demo in `main.py` has two scenarios.

### Demo 1: Correct Incremental Graph
Graph:

`base_price`, `tax_rate`, and `discount` -> `price_after_discount` -> `final_price` -> `report`

What each run demonstrates:

| Run | What Changes | What Should Recompute | Why |
| --- | --- | --- | --- |
| Cold run | Nothing is cached yet | All nodes | No signature has been stored before |
| Warm run | No inputs change | No nodes | All signatures match the cache |
| Changed-input run | `tax_rate` changes | `tax_rate`, `final_price`, `report` | Only the affected path becomes stale |

### Demo 2: Missing Dependency Edge Failure
This scenario intentionally shows a bug.

Buggy graph:

`binary_hash` -> `package_label`

But the compute function also reads `region` from outside the declared dependency list.

That means the engine cannot see that `region` matters, so it can reuse a stale value.

Fixed graph:

`binary_hash`, `region` -> `package_label`

Now the dependency is explicit, so changing `region` correctly forces recomputation.

## Run The Demo
```bash
python3 main.py
```

Expected behavior:
1. Run 1 prints a cold trace with all nodes recomputed.
2. Run 2 prints a warm trace with all nodes cached.
3. Run 3 changes `tax_rate` and recomputes only the affected subgraph.
4. The buggy scenario shows stale output after `region` changes.
5. The fixed scenario shows correct invalidation after `region` changes.

## Run Tests
```bash
python3 tests.py
```

### Test Cases And What They Prove
The tests are not just "does it run" checks. Each one proves a specific property.

| Test | What It Checks | Why It Matters |
| --- | --- | --- |
| `test_initial_run_recomputes_all_nodes` | Cold run recomputes every node | Confirms the cache starts empty and traversal is complete |
| `test_second_run_reuses_cache` | Second run reuses cache for every node | Confirms stable signatures prevent unnecessary recomputation |
| `test_change_input_recomputes_affected_subgraph_only` | Changing `tax_rate` recomputes only the affected path | Confirms invalidation is local, not global |
| `test_missing_edge_causes_stale_result_until_fixed` | Hidden dependency produces stale output; explicit edge fixes it | Confirms the graph must describe all real inputs |

### What The Tests Reveal About The Algorithm
1. The engine does not recompute by target name alone.
2. It recomputes only when a node's signature changes.
3. Cache reuse is safe only when every dependency is declared.
4. A missing edge can produce a correct-looking but stale result.

## Expected Learning Outcomes
After this lab, you should be able to explain:
1. Why unchanged subgraphs should not be recomputed.
2. How dependency signatures drive invalidation.
3. Why hidden dependencies break correctness.
4. Why explicit graph edges are required for deterministic systems.


## Practical Takeaway
If you can explain this lab, you understand the basic shape of build systems, reactive systems, and incremental pipelines:

1. Model the work as a graph.
2. Make dependencies explicit.
3. Attach a stable identity to each node state.
4. Recompute only what changed.
5. Use traces and tests to prove the invalidation logic is correct.

## Next Step
Proceed to Lab T3: Determinism vs Nondeterminism.
Add random or time-based behavior to break reproducibility, then remove non-determinism and restore stable outputs.
