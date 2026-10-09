"""Reproducible validation checks for the final FCFF model."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import tesla_fcff as model  # noqa: E402


class TeslaFcffValidationTests(unittest.TestCase):
    def setUp(self):
        self.projection = model.build_projection()
        self.value = model.dcf_value(self.projection)

    def test_known_answer_base_case(self):
        """Fixed-answer reconciliation catches unintended base-case drift."""
        self.assertAlmostEqual(self.value["enterprise_value"], 39_158.52, places=2)
        self.assertAlmostEqual(self.value["equity_value"], 74_841.52, places=2)
        self.assertAlmostEqual(self.value["per_share_value"], 21.21, places=2)

    def test_three_statement_articulation_and_bridge(self):
        for row in self.projection:
            self.assertAlmostEqual(row["gap"], 0.0, places=2)
        self.assertAlmostEqual(
            self.value["equity_value"],
            self.value["enterprise_value"] + self.value["non_operating_cash"] - self.value["debt_and_finance_leases"],
            places=2,
        )
        self.assertAlmostEqual(
            self.value["per_share_value"] * model.ASSUMPTIONS["diluted_shares"],
            self.value["equity_value"],
            places=2,
        )

    def test_dcf_monotonicity(self):
        grid = model.sensitivity(self.projection)
        center = model.ASSUMPTIONS["wacc"]
        self.assertGreater(grid[(center - 0.010, 0.030)], grid[(center, 0.030)])
        self.assertGreater(grid[(center, 0.040)], grid[(center, 0.030)])

    def test_highest_risk_terminal_value_failure_fails_loudly(self):
        """A perpetuity-growth model must reject a growth rate at/above WACC."""
        invalid = deepcopy(model.ASSUMPTIONS)
        invalid["terminal_growth"] = invalid["wacc"]
        with self.assertRaisesRegex(ValueError, "WACC must exceed terminal growth"):
            model.dcf_value(self.projection, invalid)

    def test_locked_changed_input_run(self):
        changed = deepcopy(model.ASSUMPTIONS)
        changed["automotive_growth"][1] = 0.06
        changed_projection = model.build_projection(changed)
        changed_value = model.dcf_value(changed_projection, changed)
        self.assertGreater(changed_projection[1]["fcff"], self.projection[1]["fcff"])
        self.assertGreater(changed_value["per_share_value"], self.value["per_share_value"])

    def test_operating_cash_reserve_bridge_sensitivity(self):
        reserve_case = deepcopy(model.ASSUMPTIONS)
        reserve_case["operating_cash_reserve"] = 10_000.0
        reserve_value = model.dcf_value(self.projection, reserve_case)
        self.assertAlmostEqual(reserve_value["non_operating_cash"], 34_059.0, places=2)
        self.assertAlmostEqual(
            self.value["per_share_value"] - reserve_value["per_share_value"],
            10_000.0 / model.ASSUMPTIONS["diluted_shares"],
            places=2,
        )


if __name__ == "__main__":
    unittest.main()
