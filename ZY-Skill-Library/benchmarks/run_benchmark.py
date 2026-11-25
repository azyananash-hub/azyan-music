"""Benchmark tugas representatif dengan label sintetis yang dihitung manual.

Yang DIUKUR: akurasi keluaran skill terhadap label, akurasi router, dan waktu eksekusi fungsi.
Yang TIDAK DIUKUR (NOT TESTED): A/B dengan vs tanpa skill, kualitas tulisan/desain AI,
jumlah file yang dibaca, dan konsumsi token. Runtime sesi ini tidak mengontrol kondisi itu.
Usage: python benchmarks/run_benchmark.py [--write]
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def timed(fn):
    t0 = time.perf_counter()
    out = fn()
    return out, (time.perf_counter() - t0) * 1000


def check(label, got, expected, tol):
    return {"case": label, "expected": expected, "got": got, "pass": abs(got - expected) <= tol}


def run():
    rows, timings = [], {}
    # B. Industrial utility (data sintetis, label dihitung manual)
    be = load("skills/industrial-utility/boiler-efficiency-indirect/scripts/boiler_efficiency.py", "be")
    ct = load("skills/industrial-utility/cooling-tower-performance/scripts/cooling_tower.py", "ct")
    ro = load("skills/industrial-utility/ro-mass-balance/scripts/ro_mass_balance.py", "ro")
    # Boiler: flue = 0.38*(200-25)/9 = 7.3889; eff = 100 - 7.3889 - 0.5 = 92.1111
    r, t = timed(lambda: be.efficiency({"dry_flue_gas": be.flue_gas_loss_pct(200, 25, 9), "radiation": 0.5}))
    timings["B-boiler"] = t
    rows.append(check("B-boiler efisiensi % (T_flue 200, ambien 25, CO2 9, rad 0.5)", r["efficiency_pct"], 92.1111, 0.01))
    # Cooling tower: range 12, approach 4, efektivitas 75 %, evaporasi 10 m3/h
    r, t = timed(lambda: ct.analyse(40, 28, 24, 500))
    timings["B-cooling"] = t
    rows.append(check("B-cooling range C", r["range_c"], 12.0, 0.001))
    rows.append(check("B-cooling efektivitas %", r["effectiveness_pct"], 75.0, 0.01))
    rows.append(check("B-cooling evaporasi m3/h", r["evaporation_m3_h_estimate"], 10.0, 0.01))
    # RO: Qf 20, Cf 2000, Qp 12, Cp 40 -> recovery 60 %, rejection 98 %, Cc 4940
    r, t = timed(lambda: ro.mass_balance(20, 2000, 12, 40))
    timings["B-ro"] = t
    rows.append(check("B-RO recovery %", r["recovery_pct"], 60.0, 0.001))
    rows.append(check("B-RO rejection %", r["rejection_pct"], 98.0, 0.001))
    rows.append(check("B-RO Cc mg/L", r["c_concentrate"], 4940.0, 0.01))
    # C. Creative: tautan render ClipACanvas vertikal dari HTML canvas sintetis
    rl = load("skills/clipacanvas/render-link-builder/scripts/build_render_link.py", "rl")
    html = "<!doctype html><html><body><canvas id='c'></canvas><script>const x=1;</script></body></html>"
    r, t = timed(lambda: rl.build_link(html, orientation="vertical"))
    timings["C-render-link"] = t
    q = urllib.parse.parse_qs(urllib.parse.urlparse(r["url"]).query)
    rows.append({"case": "C-link parameter vertikal", "expected": "1080x1920 fps60 dur4 auto=true",
                 "got": f"{q['width'][0]}x{q['height'][0]} fps{q['fps'][0]} dur{q['duration'][0]} auto={q['auto'][0]}",
                 "pass": (q["width"], q["height"], q["fps"], q["duration"], q["auto"]) == (["1080"], ["1920"], ["60"], ["4"], ["true"])})
    rows.append({"case": "C-link kode ter-decode memuat <canvas", "expected": True,
                 "got": "<canvas" in q["code"][0], "pass": "<canvas" in q["code"][0]})
    # E. Keuangan (data sintetis berlabel)
    ts = load("skills/quantitative-trading/trade-statistics/scripts/trade_stats.py", "ts")
    ps = load("skills/quantitative-trading/position-size-calculator/scripts/position_size.py", "ps")
    # PnL [50,-20,30,-10,40,-60]: expectancy 5, win 50 %, PF 120/90 = 1.3333, net 30
    # Equity 1000 -> 1050 -> 1030 -> 1060 -> 1050 -> 1090 -> 1030: DD terbesar 60
    r, t = timed(lambda: ts.compute_stats([50, -20, 30, -10, 40, -60], starting_equity=1000))
    timings["E-trades"] = t
    rows.append(check("E-trades expectancy", r["expectancy"], 5.0, 0.001))
    rows.append(check("E-trades win rate %", r["win_rate_pct"], 50.0, 0.001))
    rows.append(check("E-trades profit factor", r["profit_factor"], 1.3333, 0.001))
    rows.append(check("E-trades max DD absolut", r["max_drawdown_abs"], 60.0, 0.001))
    # Ukuran posisi: equity 5000, risiko 0.5 % = 25; jarak stop 10; nilai 100 -> 0.025 lot
    r, t = timed(lambda: ps.position_size(5000, 0.5, 2000, 1990, 100))
    timings["E-position"] = t
    rows.append(check("E-position units", r["units"], 0.025, 0.00001))
    return rows, timings


def routing():
    rt = load("scripts/route_skill.py", "rt")
    with open(os.path.join(ROOT, "SKILL_REGISTRY.json"), encoding="utf-8") as fh:
        reg = json.load(fh)["skills"]
    with open(os.path.join(ROOT, "benchmarks", "router_labels.json"), encoding="utf-8") as fh:
        cases = json.load(fh)["cases"]
    ok, details = 0, []
    t0 = time.perf_counter()
    for c in cases:
        top = rt.route(c["query"], reg, 3)
        got = top[0]["name"] if top else None
        ok += got == c["expected"]
        details.append({"query": c["query"], "expected": c["expected"], "got": got})
    ms = (time.perf_counter() - t0) * 1000
    return {"cases": len(cases), "correct_top1": ok, "time_ms": round(ms, 2)}, details


def main():
    rows, timings = run()
    rr, _ = routing()
    npass = sum(r["pass"] for r in rows)
    lines = ["# Hasil benchmark (label sintetis, dihitung manual)", "",
             "Sumber: `benchmarks/run_benchmark.py`. Hanya yang terukur; lainnya NOT TESTED.", "",
             f"- Perhitungan skill: **{npass}/{len(rows)}** lulus",
             f"- Ketepatan router (top-1, kueri berlabel): **{rr['correct_top1']}/{rr['cases']}** dalam {rr['time_ms']} ms",
             "", "| Kasus | Harapan | Keluaran | Lulus |", "|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['case']} | {r['expected']} | {r['got']} | {'ya' if r['pass'] else 'TIDAK'} |")
    lines += ["", "Waktu eksekusi fungsi (ms): " + ", ".join(f"{k} {v:.2f}" for k, v in timings.items()), "",
              "## NOT TESTED",
              "- A. AmiraVerse (desain Flutter): perlu runtime AI dengan dan tanpa skill; tidak ada proyek Flutter di repository ini.",
              "- D. DEAMIRA (ide ke spesifikasi): perlu runtime AI dengan dan tanpa skill.",
              "- C. Kualitas motion graphics: link dibuat dan diuji parameternya; render di server ClipACanvas tidak diuji.",
              "- Perbandingan dengan vs tanpa skill (A/B), jumlah file yang dibaca, dan konsumsi token: tidak tersedia di runtime ini."]
    text = "\n".join(lines) + "\n"
    print(text)
    if "--write" in sys.argv:
        with open(os.path.join(ROOT, "benchmarks", "RESULTS.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    return 0 if npass == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
