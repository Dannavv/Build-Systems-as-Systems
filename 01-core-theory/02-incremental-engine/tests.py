import unittest

from main import build_buggy_engine, build_fixed_engine, build_sample_engine


class IncrementalEngineTests(unittest.TestCase):
    def test_initial_run_recomputes_all_nodes(self) -> None:
        engine = build_sample_engine()
        out = engine.run(["report"])

        self.assertEqual(out["report"]["final_price"], 104.5)
        recomputed = [name for name, state in engine.last_trace if state == "recomputed"]
        self.assertEqual(
            set(recomputed),
            {"base_price", "tax_rate", "discount", "price_after_discount", "final_price", "report"},
        )

    def test_second_run_reuses_cache(self) -> None:
        engine = build_sample_engine()
        engine.run(["report"])
        engine.run(["report"])

        recomputed = [name for name, state in engine.last_trace if state == "recomputed"]
        self.assertEqual(recomputed, [])

    def test_change_input_recomputes_affected_subgraph_only(self) -> None:
        engine = build_sample_engine()
        engine.run(["report"])

        engine.set_input("tax_rate", 0.20)
        out = engine.run(["report"])

        self.assertEqual(out["report"]["final_price"], 114.0)
        recomputed = [name for name, state in engine.last_trace if state == "recomputed"]
        self.assertEqual(set(recomputed), {"tax_rate", "final_price", "report"})

    def test_missing_edge_causes_stale_result_until_fixed(self) -> None:
        buggy = build_buggy_engine()
        first = buggy.run(["package_label"])["package_label"]
        buggy.set_input("region", "eu-west-1")
        second = buggy.run(["package_label"])["package_label"]

        self.assertEqual(first, "abc123-us-east-1")
        self.assertEqual(second, "abc123-us-east-1")

        fixed = build_fixed_engine()
        fixed.run(["package_label"])
        fixed.set_input("region", "eu-west-1")
        corrected = fixed.run(["package_label"])["package_label"]
        self.assertEqual(corrected, "abc123-eu-west-1")


if __name__ == "__main__":
    unittest.main()
