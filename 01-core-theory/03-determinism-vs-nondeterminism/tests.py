import unittest

from main import DeterminismLab


class DeterminismLabTests(unittest.TestCase):
    def test_nondeterministic_pipeline_changes_between_runs(self) -> None:
        lab = DeterminismLab()
        first = lab.build_nondeterministic(["main.c", "util.c", "api.c"], ["-O2", "-Wall"])
        second = lab.build_nondeterministic(["main.c", "util.c", "api.c"], ["-O2", "-Wall"])

        self.assertNotEqual(first.payload, second.payload)

    def test_deterministic_pipeline_stable_for_same_inputs(self) -> None:
        lab = DeterminismLab()
        first = lab.build_deterministic(["main.c", "util.c", "api.c"], ["-Wall", "-O2"], build_seed="release-2026-04-25")
        second = lab.build_deterministic(["api.c", "main.c", "util.c"], ["-O2", "-Wall"], build_seed="release-2026-04-25")

        self.assertEqual(first.payload, second.payload)

    def test_canonical_report_ignores_input_order(self) -> None:
        lab = DeterminismLab()
        first = lab.build_canonical_report(["zeta", "alpha", "beta"])
        second = lab.build_canonical_report(["beta", "zeta", "alpha"])

        self.assertEqual(first, second)

    def test_order_sensitive_report_reflects_input_order(self) -> None:
        lab = DeterminismLab()
        first = lab.build_order_sensitive_report(["zeta", "alpha", "beta"])
        second = lab.build_order_sensitive_report(["beta", "zeta", "alpha"])

        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
