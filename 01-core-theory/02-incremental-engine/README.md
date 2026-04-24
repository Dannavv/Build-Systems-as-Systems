# Lab T2: Incremental Computation Engine

## Goal
Move from file timestamp rebuilds (Lab T1) to node-level incremental computation with caching.

This lab models a graph of pure transformations and recomputes only the affected nodes when inputs change.

## Why This Matters
This is the same core idea behind:
- Bazel action caching
- ML pipeline invalidation
- reactive UI/dataflow systems

If you understand this lab deeply, you understand the heart of modern build and compute orchestration.

## What You Build
A Python engine that supports:
1. Source nodes (mutable inputs)
2. Derived nodes (computed from dependencies)
3. Deterministic node signatures
4. Value and signature cache
5. Selective recomputation

## Files
- `main.py`: Engine implementation + demos
- `tests.py`: Correctness and failure tests

## Engine Model
Each node has:
- `name`
- `deps`
- `compute(dep_values)`
- `is_source`

The runtime keeps:
- `value_cache[node]`: last computed value
- `signature_cache[node]`: last dependency/input signature
- `last_trace`: ordered list of `("node", "recomputed|cached")`

## Algorithm (Per Node)
When evaluating node `N`:
1. Recursively evaluate all dependencies first.
2. Build a deterministic signature for `N`.
3. Compare against previous signature.
4. If unchanged and cached value exists, reuse cache.
5. Otherwise recompute `N`, then update caches.

Cycle detection is included via a `visiting` set.

## How To Run
```bash
python3 main.py
```

You will see two demos:
1. Correct incremental graph: cold run, warm run, changed-input run.
2. Missing-edge failure: stale output due to hidden dependency, then fixed graph.

## Run Tests
```bash
python3 tests.py
```

## Expected Learning Outcomes
After this lab, you should be able to explain:
1. Why unchanged subgraphs should not be recomputed.
2. How dependency signatures drive invalidation.
3. Why hidden dependencies break correctness.
4. Why explicit graph edges are required for deterministic systems.

## Meta-Evaluation Checklist
This lab includes all required dimensions:

1. Correctness test
- `tests.py` validates full recompute on cold run and selective recompute after change.

2. Performance metric
- `main.py` prints elapsed milliseconds for cold/warm/changed runs.

3. Reproducibility check
- Same inputs produce the same output and cache behavior.

4. Failure scenario
- Buggy graph intentionally omits an edge (`region`), producing stale output.
- Fixed graph declares the edge and recomputes correctly.

## Next Step
Proceed to Lab T3: Determinism vs Nondeterminism.
Add random or time-based behavior to break reproducibility, then remove non-determinism and restore stable outputs.
