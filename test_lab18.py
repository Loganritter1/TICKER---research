import unittest

from edgar_buffett import buffett_checks
from memo_validation import unsupported_numbers


class Lab18Tests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"Fiscal year end": "2022-08-28", "Revenue": 226954.0, "Net income": 5844.0, "Operating cash flow": 7392.0, "Capital spending": 3891.0, "Equity": 20642.0, "ROE": 28.3, "Owner earnings": 3501.0},
            {"Fiscal year end": "2023-09-03", "Revenue": 242290.0, "Net income": 6292.0, "Operating cash flow": 11068.0, "Capital spending": 4323.0, "Equity": 25058.0, "ROE": 25.1, "Owner earnings": 6745.0},
            {"Fiscal year end": "2024-09-01", "Revenue": 254453.0, "Net income": 7367.0, "Operating cash flow": 11339.0, "Capital spending": 4710.0, "Equity": 23622.0, "ROE": 31.2, "Owner earnings": 6629.0},
            {"Fiscal year end": "2025-08-31", "Revenue": 275235.0, "Net income": 8099.0, "Operating cash flow": 13335.0, "Capital spending": 5498.0, "Equity": 29164.0, "ROE": 27.8, "Owner earnings": 7837.0},
            {"Fiscal year end": "2026-08-30", "Revenue": 303154.0, "Net income": 9226.0, "Operating cash flow": 15817.0, "Capital spending": 6435.0, "Equity": 35803.0, "ROE": 25.8, "Owner earnings": 9382.0},
        ]
        for row in self.rows:
            row["Tags"] = {metric: "test-tag" for metric in (*["Revenue", "Net income", "Operating cash flow", "Capital spending", "Equity"], "ROE", "Owner earnings")}

    def test_cost_known_answer_checks_pass(self):
        self.assertEqual(set(buffett_checks(self.rows).values()), {"pass"})

    def test_missing_owner_earnings_is_not_known(self):
        self.rows[0]["Owner earnings"] = "not found"
        checks = buffett_checks(self.rows)
        self.assertEqual(checks["Owner earnings positive every year"], "not known")
        self.assertEqual(checks["Owner earnings grew, first year to last"], "not known")

    def test_hand_typed_number_is_flagged(self):
        report = {"cik": "0000909832", "rows": self.rows}
        self.assertEqual(unsupported_numbers("ROE was 40.0%.", report), ["40.0%"]) 
        self.assertEqual(unsupported_numbers("ROE was 28.3%.", report), [])

    def test_10_k_label_is_not_treated_as_a_number(self):
        report = {"cik": "0000909832", "rows": self.rows}
        self.assertEqual(unsupported_numbers("The 10-K supports this view.", report), [])


if __name__ == "__main__":
    unittest.main()
