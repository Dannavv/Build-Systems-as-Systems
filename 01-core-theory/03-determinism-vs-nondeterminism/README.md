# Lab T3: Determinism vs Nondeterminism

## Goal
Break reproducibility on purpose, then fix it.

This lab shows why build and pipeline systems must treat randomness, time, environment, and ordering as explicit design concerns instead of hidden behavior.

## Why This Matters
If a system is not deterministic, then:
- the same inputs can produce different outputs
- cache keys become unreliable
- debugging becomes expensive
- CI becomes hard to trust
- distributed builds become unsafe

This is a core systems idea, not just a build-system detail.

## What You Build
A small Python lab that demonstrates:
1. Hidden nondeterminism from time and RNG
2. Unstable output from unordered data
3. Deterministic output from explicit inputs and canonicalization
4. Tests that prove the fix

## Files
- `main.py`: demo code for bad and fixed pipelines
- `tests.py`: correctness and reproducibility tests

## Problem Model
A pipeline is only deterministic when all of its real inputs are explicit.

That means the pipeline must control:
- source content
- build flags
- seed values
- ordering of collections
- environment-dependent values

If any of those leak in from the runtime implicitly, the output can change even when the declared inputs look the same.

## Algorithm
### Nondeterministic version
The bad pipeline deliberately mixes in hidden state:
1. Reads source files and flags.
2. Uses `time.time_ns()` as a hidden changing input.
3. Uses RNG to add another hidden changing input.
4. Converts an unordered set into a list without canonical sorting.
5. Produces a payload that may differ across runs.

### Deterministic version
The fixed pipeline removes hidden state:
1. Takes source files, flags, and a build seed as explicit inputs.
2. Sorts files and flags into a canonical order.
3. Derives the build id from a stable hash.
4. Produces the same payload whenever the inputs are the same.

### Ordering lesson
Even if a pipeline has no randomness, order can still break reproducibility.

If two equivalent input lists are presented in a different order, the result should only differ if order is intentionally meaningful. If order should not matter, canonicalize it first.

## Demo Design
### Demo 1: Hidden Nondeterminism
This demo builds the same nominal artifact twice with the same declared inputs.

What it shows:
- the hidden build id changes
- the manifest order can vary
- identical-looking requests can produce different payloads

### Demo 2: Fixed Deterministic Build
This demo runs the same build twice, but with inputs reordered.

What it shows:
- the canonical manifest stays the same
- the build id stays the same
- the payload stays the same

### Demo 3: Ordering Bug And Canonical Fix
This demo compares two report builders:
- one preserves caller order
- one sorts entries before hashing

The canonical version is stable across run order and input order.

## Run The Demo
```bash
python3 main.py
```

Expected behavior:
1. Demo 1 prints different payloads for the nondeterministic build.
2. Demo 2 prints identical payloads for the deterministic build.
3. Demo 3 shows the difference between order-sensitive and canonical output.

## Run Tests
```bash
python3 tests.py
```

## Test Cases And What They Prove
| Test | What It Checks | Why It Matters |
| --- | --- | --- |
| `test_nondeterministic_pipeline_changes_between_runs` | Same nominal inputs produce different payloads in the bad pipeline | Confirms hidden state breaks reproducibility |
| `test_deterministic_pipeline_stable_for_same_inputs` | Reordered inputs still produce the same output in the fixed pipeline | Confirms canonicalization and explicit seeds work |
| `test_canonical_report_ignores_input_order` | Canonical report is stable across entry order | Confirms sorting removes order noise |
| `test_order_sensitive_report_reflects_input_order` | Unsorted report changes when order changes | Confirms why canonicalization is needed |

## Expected Learning Outcomes
After this lab, you should be able to explain:
1. Why hidden state breaks reproducibility.
2. Why build ids should come from explicit inputs, not runtime noise.
3. Why canonicalization matters for sets, lists, and manifests.
4. Why deterministic systems are easier to cache, debug, and distribute.

## Meta-Evaluation Checklist
This lab includes all required dimensions:

1. Correctness test
- `tests.py` proves both the failure and the fixed behavior.

2. Performance metric
- The demo is small, but it establishes the baseline for comparing stable and unstable runs.

3. Reproducibility check
- The deterministic pipeline returns the same payload for equivalent inputs.

4. Failure scenario
- The nondeterministic pipeline uses time, RNG, and ordering noise.
- The deterministic pipeline removes those sources of variation.

## Practical Takeaway
Determinism is not just about "being careful". It is a design rule:

1. Make all real inputs explicit.
2. Canonicalize any input whose order should not matter.
3. Never mix hidden runtime state into outputs.
4. Use tests to prove repeatability.
5. Use stable outputs as the foundation for caching and distribution.

## Next Step
After this lab, the natural follow-up is to connect determinism back to build systems and cache keys. That leads into the next layers of the curriculum: tool mastery and reproducibility engineering.
