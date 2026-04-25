import hashlib
import json
import os
import random
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=repr)


def stable_hash(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


@dataclass
class Artifact:
    name: str
    inputs: Dict[str, Any]
    payload: Dict[str, Any]


class DeterminismLab:
    def __init__(self) -> None:
        self.rng = random.Random()

    def build_nondeterministic(self, source_files: List[str], flags: List[str]) -> Artifact:
        """Build an artifact with hidden nondeterministic inputs.

        This intentionally mixes in time, RNG state, and an unordered manifest.
        The same declared inputs can therefore produce different outputs.
        """

        manifest = {name for name in source_files}
        build_id = f"{time.time_ns()}-{self.rng.randint(1000, 9999)}"
        payload = {
            "mode": "nondeterministic",
            "build_id": build_id,
            "manifest": list(manifest),
            "flags": flags,
        }
        return Artifact(name="demo.bin", inputs={"source_files": source_files, "flags": flags}, payload=payload)

    def build_deterministic(self, source_files: List[str], flags: List[str], build_seed: str) -> Artifact:
        """Build an artifact from explicit inputs only.

        The manifest is canonicalized, and the build id is derived from a stable hash.
        """

        canonical_manifest = sorted(source_files)
        payload = {
            "mode": "deterministic",
            "build_id": stable_hash({"files": canonical_manifest, "flags": sorted(flags), "seed": build_seed})[:16],
            "manifest": canonical_manifest,
            "flags": sorted(flags),
            "seed": build_seed,
        }
        return Artifact(
            name="demo.bin",
            inputs={"source_files": source_files, "flags": flags, "build_seed": build_seed},
            payload=payload,
        )

    def build_order_sensitive_report(self, entries: List[str]) -> Dict[str, Any]:
        """Create a report that becomes unstable if caller order is not canonicalized."""

        # Intentionally use the incoming order as-is to show why canonicalization matters.
        return {
            "entries": entries,
            "fingerprint": stable_hash({"entries": entries}),
        }

    def build_canonical_report(self, entries: List[str]) -> Dict[str, Any]:
        """Create a stable report by sorting entries before hashing."""

        canonical_entries = sorted(entries)
        return {
            "entries": canonical_entries,
            "fingerprint": stable_hash({"entries": canonical_entries}),
        }


def print_artifact(title: str, artifact: Artifact) -> None:
    print(f"\n=== {title} ===")
    print(f"inputs: {artifact.inputs}")
    print(f"payload: {artifact.payload}")


def demo_nondeterminism() -> None:
    print("## Demo 1: Hidden Nondeterminism")
    print("model: the same declared inputs can still produce different outputs if time, RNG, or order leak in")
    lab = DeterminismLab()

    run1 = lab.build_nondeterministic(["main.c", "util.c", "api.c"], ["-O2", "-Wall"])
    time.sleep(0.001)
    run2 = lab.build_nondeterministic(["main.c", "util.c", "api.c"], ["-O2", "-Wall"])

    print_artifact("Run 1", run1)
    print_artifact("Run 2", run2)
    print(f"same_payload: {run1.payload == run2.payload}")
    print("expected: payloads differ because build_id and manifest order are not controlled")


def demo_determinism() -> None:
    print("\n## Demo 2: Fixed Deterministic Build")
    print("model: all variability becomes explicit input, and manifests are canonicalized")
    lab = DeterminismLab()

    run1 = lab.build_deterministic(["main.c", "util.c", "api.c"], ["-Wall", "-O2"], build_seed="release-2026-04-25")
    run2 = lab.build_deterministic(["api.c", "main.c", "util.c"], ["-O2", "-Wall"], build_seed="release-2026-04-25")

    print_artifact("Deterministic Run 1", run1)
    print_artifact("Deterministic Run 2", run2)
    print(f"same_payload: {run1.payload == run2.payload}")
    print("expected: payloads match even if caller order differs, because canonicalization removes noise")


def demo_ordering() -> None:
    print("\n## Demo 3: Ordering Bug And Canonical Fix")
    lab = DeterminismLab()

    unstable = lab.build_order_sensitive_report(["zeta", "alpha", "beta"])
    stable = lab.build_canonical_report(["zeta", "alpha", "beta"])

    print(f"order_sensitive: {unstable}")
    print(f"canonical: {stable}")
    print("expected: canonical report is stable across runs and input order")


def main() -> None:
    print("Lab T3: Determinism vs Nondeterminism")
    print(f"python={os.environ.get('PYTHONHASHSEED', 'default-hash-seed')}")
    demo_nondeterminism()
    demo_determinism()
    demo_ordering()


if __name__ == "__main__":
    main()
