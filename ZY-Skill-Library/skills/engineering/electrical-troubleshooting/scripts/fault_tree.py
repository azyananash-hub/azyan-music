"""Pohon keputusan troubleshooting kelistrikan: setiap simpul menguji satu pengukuran.

Format pohon: {"start": "n1", "nodes": {
   "n1": {"measure": "tegangan_input_v", "op": "between", "value": [a, b], "yes": "n2", "no": "leaf_x"},
   "leaf_x": {"cause": "...", "action": "..."}}}
Batas (value) HARUS diisi dari SOP atau data pabrikan Anda. Skill ini tidak menyediakan nilai standar.
Operator: eq, lt, gt, between. Pengukuran yang belum tersedia menghentikan penelusuran dengan status
NEED_MEASUREMENT, bukan menebak.
"""
from __future__ import annotations

import json
import sys

OPS = {"eq": lambda v, x: v == x, "lt": lambda v, x: v < x, "gt": lambda v, x: v > x,
       "between": lambda v, x: x[0] <= v <= x[1]}


def walk(tree: dict, observations: dict) -> dict:
    nodes = tree["nodes"]
    path, cur = [], tree["start"]
    for _ in range(len(nodes) + 1):
        node = nodes.get(cur)
        if node is None:
            return {"status": "ERROR", "path": path, "reason": f"simpul '{cur}' tidak ada"}
        if "cause" in node:
            return {"status": "CAUSE", "path": path, "cause": node["cause"], "action": node.get("action", "")}
        m = node["measure"]
        if m not in observations:
            return {"status": "NEED_MEASUREMENT", "path": path, "measure": m}
        if node["op"] not in OPS:
            return {"status": "ERROR", "path": path, "reason": f"operator '{node['op']}' tidak dikenal"}
        ok = OPS[node["op"]](observations[m], node["value"])
        path.append({"node": cur, "measure": m, "observed": observations[m], "result": ok})
        cur = node["yes"] if ok else node["no"]
    return {"status": "ERROR", "path": path, "reason": "pohon berputar (siklus)"}


def _main(argv=None) -> int:
    if len(sys.argv) < 3:
        print("usage: fault_tree.py tree.json observations.json", file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as fh:
            tree = json.load(fh)
        with open(sys.argv[2], encoding="utf-8") as fh:
            obs = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    res = walk(tree, obs)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0 if res["status"] == "CAUSE" else 1


if __name__ == "__main__":
    sys.exit(_main())
