"""Load flow (AC power flow) sederhana berbasis pandapower (BSD-3-Clause).

Input JSON (satuan: kV, MW, Mvar, km, ohm/km):
{
  "base_kv": 20,
  "ext_grid": {"bus": 0, "vm_pu": 1.0},
  "buses": [{"index": 0, "vn_kv": 20}, {"index": 1, "vn_kv": 20}],
  "lines": [{"from": 0, "to": 1, "length_km": 2.0, "r_ohm_per_km": 0.3, "x_ohm_per_km": 0.35, "c_nf_per_km": 0, "max_i_ka": 0.3}],
  "loads": [{"bus": 1, "p_mw": 2.0, "q_mvar": 0.8}]
}

Output: tegangan per bus (pu), aliran daya slack, rugi daya, dan pemeriksaan keseimbangan daya.
Hanya untuk studi awal/pendidikan. Keputusan operasi harus berdasarkan studi lengkap.
"""

from __future__ import annotations

import argparse
import json
import sys

import pandapower as pp


def build_network(spec: dict) -> pp.pandapowerNet:
    net = pp.create_empty_network(sn_mva=float(spec.get("sn_mva", 10.0)))
    idx_map = {}
    for b in spec["buses"]:
        idx_map[b["index"]] = pp.create_bus(net, vn_kv=float(b["vn_kv"]), index=int(b["index"]))
    eg = spec["ext_grid"]
    pp.create_ext_grid(net, bus=idx_map[eg["bus"]], vm_pu=float(eg.get("vm_pu", 1.0)))
    for ln in spec.get("lines", []):
        pp.create_line_from_parameters(
            net,
            from_bus=idx_map[ln["from"]],
            to_bus=idx_map[ln["to"]],
            length_km=float(ln["length_km"]),
            r_ohm_per_km=float(ln["r_ohm_per_km"]),
            x_ohm_per_km=float(ln["x_ohm_per_km"]),
            c_nf_per_km=float(ln.get("c_nf_per_km", 0.0)),
            max_i_ka=float(ln.get("max_i_ka", 1.0)),
        )
    for ld in spec.get("loads", []):
        pp.create_load(net, bus=idx_map[ld["bus"]], p_mw=float(ld["p_mw"]), q_mvar=float(ld.get("q_mvar", 0.0)))
    return net


def solve(spec: dict) -> dict:
    net = build_network(spec)
    pp.runpp(net, algorithm="nr", max_iteration=50)
    total_load_p = float(net.load.p_mw.sum())
    total_load_q = float(net.load.q_mvar.sum())
    slack_p = float(net.res_ext_grid.p_mw.sum())
    slack_q = float(net.res_ext_grid.q_mvar.sum())
    losses_p = float(net.res_line.pl_mw.sum())
    balance_error = slack_p - (total_load_p + losses_p)
    return {
        "converged": bool(net.converged),
        "bus_vm_pu": {int(i): round(float(v), 5) for i, v in net.res_bus.vm_pu.items()},
        "slack_p_mw": round(slack_p, 5),
        "slack_q_mvar": round(slack_q, 5),
        "load_p_mw": round(total_load_p, 5),
        "load_q_mvar": round(total_load_q, 5),
        "line_losses_p_mw": round(losses_p, 6),
        "power_balance_error_mw": round(balance_error, 6),
        "line_loading_pct": {int(i): round(float(v), 2) for i, v in net.res_line.loading_percent.items()},
        "scope_note": "Power flow seimbang untuk jaringan radial/meshed sederhana; bukan studi lengkap.",
    }


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("network_json")
    args = p.parse_args(argv)
    try:
        with open(args.network_json, encoding="utf-8") as fh:
            spec = json.load(fh)
        result = solve(spec)
    except (OSError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except pp.powerflow.LoadflowNotConverged as exc:
        print(f"ERROR: load flow tidak konvergen: {exc}", file=sys.stderr)
        return 3
    print(json.dumps(result, indent=2))
    return 0 if result["converged"] else 3


if __name__ == "__main__":
    sys.exit(_main())
