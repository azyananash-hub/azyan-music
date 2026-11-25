"""Uji Intelligent Skill Router: 8 kueri nyata dengan skill yang seharusnya paling relevan."""
import json
import os
import unittest

from _helpers import LIBRARY_ROOT, load_module

router = load_module("route_skill", "scripts/route_skill.py")
with open(os.path.join(LIBRARY_ROOT, "SKILL_REGISTRY.json"), encoding="utf-8") as fh:
    REG = json.load(fh)["skills"]

CASES = {
    "hitung arus hubung singkat bus 11 kV dari MVA sumber": "short-circuit-calculator",
    "load flow tegangan bus dan rugi daya saluran": "load-flow-pandapower",
    "baca register holding Modbus TCP dari PLC": "modbus-tcp-client",
    "range dan approach cooling tower": "cooling-tower-performance",
    "efisiensi boiler metode gas buang Siegert": "boiler-efficiency-indirect",
    "recovery dan rejection membran RO neraca massa": "ro-mass-balance",
    "Sharpe ratio dan max drawdown portofolio dari return harian": "portfolio-metrics-quantstats",
    "jadwal review kartu kosakata JLPT dengan FSRS": "fsrs-scheduler",
}


class RouterTests(unittest.TestCase):
    def test_top1_accuracy(self):
        hits = 0
        for query, expected in CASES.items():
            top = router.route(query, REG, top=1)
            if top and top[0]["name"] == expected:
                hits += 1
        self.assertEqual(hits, len(CASES), f"{hits}/{len(CASES)} benar")

    def test_empty_query_rejected(self):
        with self.assertRaises(ValueError):
            router.route("dan atau yang", REG)


if __name__ == "__main__":
    unittest.main()
