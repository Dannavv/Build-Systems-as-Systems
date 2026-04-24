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
    """A graph node in the incremental computation engine.

    Source nodes read their value from `inputs`. Derived nodes compute their
    value from dependency values provided during evaluation.
    """

    name: str
    deps: List[str]
    compute: Callable[[Dict[str, Any]], Any]
    is_source: bool = False


@dataclass
class TraceEntry:
    """One node evaluation record captured during a run."""

    name: str
    state: str
    signature: str
    deps: List[str]


class IncrementalEngine:
    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}
        self.inputs: Dict[str, Any] = {}
        self.value_cache: Dict[str, Any] = {}
        self.signature_cache: Dict[str, str] = {}
        self.last_trace: List[TraceEntry] = []

    def add_source(self, name: str, initial_value: Any) -> None:
        """Register an input node whose value can change between runs."""

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
        """Register a derived node with explicit dependency edges."""

        if name in self.nodes:
            raise ValueError(f"Node '{name}' already exists")

        self.nodes[name] = Node(name=name, deps=deps, compute=compute, is_source=False)

    def set_input(self, name: str, value: Any) -> None:
        """Change a source value and let the next run invalidate dependents."""

        if name not in self.nodes or not self.nodes[name].is_source:
            raise ValueError(f"Input '{name}' is not a declared source node")
        self.inputs[name] = value

    def run(self, targets: List[str]) -> Dict[str, Any]:
        """Evaluate one or more targets and update the trace/cache state.

        The engine always walks dependencies first. Each node is then compared
        against its previous signature to decide whether the cached value can be
        reused or whether the node must be recomputed.
        """

        self.last_trace = []
        outputs: Dict[str, Any] = {}
        visiting: Set[str] = set()

        for target in targets:
            value, _ = self._build_node(target, visiting)
            outputs[target] = value

        return outputs

    def _build_node(self, name: str, visiting: Set[str]) -> Tuple[Any, str]:
        """Recursively evaluate one node and return its value plus signature."""

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

        signature_payload = self._signature_payload(node, dep_signatures)

        signature = stable_hash(signature_payload)

        if self.signature_cache.get(name) == signature and name in self.value_cache:
            self.last_trace.append(TraceEntry(name=name, state="cached", signature=signature, deps=list(node.deps)))
            visiting.remove(name)
            return self.value_cache[name], signature

        if node.is_source:
            value = self.inputs[name]
        else:
            value = node.compute(dep_values)

        self.value_cache[name] = value
        self.signature_cache[name] = signature
        self.last_trace.append(TraceEntry(name=name, state="recomputed", signature=signature, deps=list(node.deps)))
        visiting.remove(name)
        return value, signature

    def _signature_payload(self, node: Node, dep_signatures: Dict[str, str]) -> Dict[str, Any]:
        """Build the data that determines whether a node is stale.

        Source nodes depend on their own value.
        Derived nodes depend on the signatures of their direct dependencies.
        """

        if node.is_source:
            return {
                "name": node.name,
                "kind": "source",
                "value": self.inputs[node.name],
            }

        return {
            "name": node.name,
            "kind": "derived",
            "deps": dep_signatures,
        }


def build_sample_engine() -> IncrementalEngine:
    """A clean dependency graph for incremental computation."""

    engine = IncrementalEngine()
    engine.add_source("base_price", 100)
    engine.add_source("tax_rate", 0.10)
    engine.add_source("discount", 5)

    engine.add_node(
        "price_after_discount",
        ["base_price", "discount"],
        lambda d: d["base_price"] - d["discount"],
    )
    engine.add_node(
        "final_price",
        ["price_after_discount", "tax_rate"],
        lambda d: round(d["price_after_discount"] * (1 + d["tax_rate"]), 2),
    )
    engine.add_node(
        "report",
        ["final_price"],
        lambda d: {"final_price": d["final_price"], "currency": "USD"},
    )
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

    recomputed = [entry.name for entry in engine.last_trace if entry.state == "recomputed"]
    cached = [entry.name for entry in engine.last_trace if entry.state == "cached"]

    print(f"\n=== {title} ===")
    print(f"output: {outputs[target]}")
    print(f"recomputed: {recomputed}")
    print(f"cached: {cached}")
    print("trace:")
    for entry in engine.last_trace:
        deps_text = ", ".join(entry.deps) if entry.deps else "<none>"
        print(f"  - {entry.name}: {entry.state}, deps=[{deps_text}], signature={entry.signature[:12]}...")
    print(f"elapsed_ms: {elapsed_ms:.3f}")
    return elapsed_ms


def demo_incrementality() -> None:
    print("\n## Demo 1: Correct Incremental Graph")
    print("model: source nodes feed derived nodes; signatures decide cache reuse")
    engine = build_sample_engine()

    t1 = print_run(engine, "Run 1 (cold)", "report")
    t2 = print_run(engine, "Run 2 (warm, no changes)", "report")

    engine.set_input("tax_rate", 0.20)
    t3 = print_run(engine, "Run 3 (changed tax_rate)", "report")

    print("\nsummary:")
    print(f"run1_ms={t1:.3f}, run2_ms={t2:.3f}, run3_ms={t3:.3f}")
    print("expected: run2 reuses cache heavily; run3 recomputes only the affected subgraph")


def demo_missing_edge_failure() -> None:
    print("\n## Demo 2: Missing Dependency Edge Failure")
    print("failure model: a node can look fresh if the graph omits a real dependency")

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
