import io
import unittest

from _helpers import TRADE_STATS, load_module

ts = load_module("trade_stats", TRADE_STATS)


class TradeStatsTests(unittest.TestCase):
    def test_basic_metrics(self):
        s = ts.compute_stats([100, -50, 200, -100])
        self.assertEqual(s["total_trades"], 4)
        self.assertEqual(s["win_rate_pct"], 50.0)
        self.assertEqual(s["expectancy"], 37.5)
        self.assertEqual(s["profit_factor"], 2.0)  # 300 / 150
        self.assertEqual(s["net_pnl"], 150.0)

    def test_expectancy_times_n_equals_net(self):
        s = ts.compute_stats([10, -3, 7.5, -2.25, 4])
        self.assertAlmostEqual(s["expectancy"] * s["total_trades"], s["net_pnl"], places=3)

    def test_no_losses_profit_factor_none(self):
        self.assertIsNone(ts.compute_stats([1, 2, 3])["profit_factor"])

    def test_max_drawdown_with_starting_equity(self):
        # 10000 -> 9500 -> 9700 -> 8900: DD terbesar 1100 dari puncak 10000 = 11%
        s = ts.compute_stats([-500, 200, -800], starting_equity=10000)
        self.assertEqual(s["max_drawdown_abs"], 1100.0)
        self.assertEqual(s["max_drawdown_pct"], 11.0)

    def test_max_drawdown_without_starting_equity_has_no_pct(self):
        s = ts.compute_stats([-500, 200, -800])
        self.assertIsNone(s["max_drawdown_pct"])
        self.assertIn("note", s)

    def test_small_sample_warning(self):
        self.assertIn("warning", ts.compute_stats([1, -1]))

    def test_empty_and_non_finite_rejected(self):
        with self.assertRaises(ValueError):
            ts.compute_stats([])
        with self.assertRaises(ValueError):
            ts.compute_stats([1.0, float("inf")])

    def test_load_pnls_bad_value(self):
        with self.assertRaises(ValueError):
            ts.load_pnls(io.StringIO("pnl\n12\nabc\n"))

    def test_load_pnls_ok(self):
        self.assertEqual(ts.load_pnls(io.StringIO("pnl\n1.5\n-2\n")), [1.5, -2.0])


if __name__ == "__main__":
    unittest.main()
