import hashlib
import json
import time
from dataclasses import dataclass
from time import perf_counter
from typing import Any, Callable, Dict, List, Set, Tuple


def stable_hash(value: Any) -> str:
    """Create a deterministic hash for nested Python values."""

    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=repr)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass
class Node:
    name: str
    deps: List[str]
    compute: Callable[[Dict[str, Any]], Any]
    is_source: bool = False


class IncrementalEngine:
    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}
        self.inputs: Dict[str, Any] = {}
        self.value_cache: Dict[str, Any] = {}
        self.signature_cache: Dict[str, str] = {}
        self.last_trace: List[Tuple[str, str]] = []

    def add_source(self, name: str, initial_value: Any) -> None:
        if name in self.nodes:
            raise ValueError(f"Node '{name}' already exists")

        self.inputs[name] = initial_value
        self.nodes[name] = Node(
            name=name,
            deps=[],
            compute=lambda _: self.inputs[name],
            is_source=True,
        )

    def add_node(self, name: str, deps: List[str], compute: Callable[[Dict[str, Any]], Any]) -> None:
        if name in self.nodes:
            raise ValueError(f"Node '{name}' already exists")

        self.nodes[name] = Node(name=name, deps=deps, compute=compute, is_source=False)

    def set_input(self, name: str, value: Any) -> None:
        if name not in self.nodes or not self.nodes[name].is_source:
            raise ValueError(f"Input '{name}' is not a declared source node")
        self.inputs[name] = value

    def run(self, targets: List[str]) -> Dict[str, Any]:
        self.last_trace = []
        outputs: Dict[str, Any] = {}
        visiting: Set[str] = set()

        for target in targets:
            value, _ = self._build_node(target, visiting)
            outputs[target] = value

        return outputs

    def _build_node(self, name: str, visiting: Set[str]) -> Tuple[Any, str]:
        if name not in self.nodes:
            raise ValueError(f"Unknown node '{name}'")

        if name in visiting:
            cycle = " -> ".join(list(visiting) + [name])
            raise ValueError(f"Cycle detected: {cycle}")

        visiting.add(name)
        node = self.nodes[name]

        dep_values: Dict[str, Any] = {}
        dep_signatures: Dict[str, str] = {}

        for dep in node.deps:
            dep_value, dep_sig = self._build_node(dep, visiting)
            dep_values[dep] = dep_value
            dep_signatures[dep] = dep_sig

        if node.is_source:
            signature_payload = {
                "name": node.name,
                "kind": "source",
                "value": self.inputs[node.name],
            }
        else:
            signature_payload = {
                "name": node.name,
                "kind": "derived",
                "deps": dep_signatures,
            }

        signature = stable_hash(signature_payload)

        if self.signature_cache.get(name) == signature and name in self.value_cache:
            self.last_trace.append((name, "cached"))
            visiting.remove(name)
            return self.value_cache[name], signature

        if node.is_source:
            value = self.inputs[name]
        else:
            value = node.compute(dep_values)

        self.value_cache[name] = value
        self.signature_cache[name] = signature
        self.last_trace.append((name, "recomputed"))
        visiting.remove(name)
        return value, signature


def build_sample_engine() -> IncrementalEngine:
    """A clean dependency graph for incremental computation."""

    engine = IncrementalEngine()
    engine.add_source("base_price", 100)
    engine.add_source("tax_rate", 0.10)
    engine.add_source("discount", 5)

    engine.add_node("price_after_discount", ["base_price", "discount"], lambda d: d["base_price"] - d["discount"])
    engine.add_node("final_price", ["price_after_discount", "tax_rate"], lambda d: round(d["price_after_discount"] * (1 + d["tax_rate"]), 2))
    engine.add_node("report", ["final_price"], lambda d: {"final_price": d["final_price"], "currency": "USD"})
    return engine


def build_buggy_engine() -> IncrementalEngine:
    """
    Intentional hidden-dependency bug:
    package_label reads 'region' from outside declared dependencies.
    """

    engine = IncrementalEngine()
    engine.add_source("binary_hash", "abc123")
    engine.add_source("region", "us-east-1")

    # BUG: missing dependency on 'region'
    engine.add_node(
        "package_label",
        ["binary_hash"],
        lambda d: f"{d['binary_hash']}-{engine.inputs['region']}",
    )
    return engine


def build_fixed_engine() -> IncrementalEngine:
    """Correct version where region is an explicit dependency."""

    engine = IncrementalEngine()
    engine.add_source("binary_hash", "abc123")
    engine.add_source("region", "us-east-1")

    engine.add_node(
        "package_label",
        ["binary_hash", "region"],
        lambda d: f"{d['binary_hash']}-{d['region']}",
    )
    return engine


def print_run(engine: IncrementalEngine, title: str, target: str) -> float:
    start = perf_counter()
    outputs = engine.run([target])
    elapsed_ms = (perf_counter() - start) * 1000

    recomputed = [name for name, state in engine.last_trace if state == "recomputed"]
    cached = [name for name, state in engine.last_trace if state == "cached"]

    print(f"\n=== {title} ===")
    print(f"output: {outputs[target]}")
    print(f"recomputed: {recomputed}")
    print(f"cached: {cached}")
    print(f"elapsed_ms: {elapsed_ms:.3f}")
    return elapsed_ms


def demo_incrementality() -> None:
    print("\n## Demo 1: Correct Incremental Graph")
    engine = build_sample_engine()

    t1 = print_run(engine, "Run 1 (cold)", "report")
    t2 = print_run(engine, "Run 2 (warm, no changes)", "report")

    engine.set_input("tax_rate", 0.20)
    t3 = print_run(engine, "Run 3 (changed tax_rate)", "report")

    print("\nsummary:")
    print(f"run1_ms={t1:.3f}, run2_ms={t2:.3f}, run3_ms={t3:.3f}")
    print("expected: run2 reuses cache heavily; run3 recomputes only affected path")


def demo_missing_edge_failure() -> None:
    print("\n## Demo 2: Missing Dependency Edge Failure")

    buggy = build_buggy_engine()
    print_run(buggy, "Buggy Run 1", "package_label")
    buggy.set_input("region", "eu-west-1")
    print_run(buggy, "Buggy Run 2 (region changed)", "package_label")
    print("note: output may stay stale because 'region' was not declared as dependency")

    fixed = build_fixed_engine()
    print_run(fixed, "Fixed Run 1", "package_label")
    fixed.set_input("region", "eu-west-1")
    print_run(fixed, "Fixed Run 2 (region changed)", "package_label")
    print("note: fixed graph updates correctly because 'region' is explicit")


if __name__ == "__main__":
    demo_incrementality()
    time.sleep(0.05)
    demo_missing_edge_failure()
