"""Validasi dan urutkan rencana multi-agent: dependensi, siklus, dan konflik tulis file.

Input JSON: {"tasks": [{"id": "T1", "deps": ["T0"], "writes": ["src/a.py"]}, ...]}
Keluaran: gelombang (wave) yang aman dijalankan paralel. Tugas dalam satu gelombang tidak boleh
menulis file yang sama. Jika tulis bersinggungan, tugas dipindah ke gelombang berikutnya.
"""
from __future__ import annotations

import json
import sys


def plan(tasks: list[dict]) -> dict:
    ids = [t["id"] for t in tasks]
    if len(set(ids)) != len(ids):
        raise ValueError("id tugas duplikat")
    by_id = {t["id"]: t for t in tasks}
    for t in tasks:
        for d in t.get("deps", []):
            if d not in by_id:
                raise ValueError(f"tugas {t['id']} bergantung pada '{d}' yang tidak ada")
    indeg = {t["id"]: len(t.get("deps", [])) for t in tasks}
    dependents: dict[str, list[str]] = {i: [] for i in ids}
    for t in tasks:
        for d in t.get("deps", []):
            dependents[d].append(t["id"])
    waves: list[list[str]] = []
    done: set[str] = set()
    remaining = set(ids)
    while remaining:
        ready = sorted(i for i in remaining if all(d in done for d in by_id[i].get("deps", [])))
        if not ready:
            raise ValueError(f"siklus dependensi pada: {', '.join(sorted(remaining))}")
        wave: list[str] = []
        written: set[str] = set()
        deferred: list[str] = []
        for i in ready:
            w = set(by_id[i].get("writes", []))
            if w & written:
                deferred.append(i)
            else:
                wave.append(i)
                written |= w
        waves.append(wave)
        done |= set(wave)
        remaining -= set(wave)
        # tugas yang ditunda karena konflik tulis akan dicoba lagi di gelombang berikutnya
        if not wave:
            raise ValueError("tidak ada tugas yang bisa dijadwalkan")
    return {"waves": waves, "tasks": len(ids)}


def _main(argv=None) -> int:
    if len(sys.argv) < 2:
        print("usage: task_graph.py plan.json", file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as fh:
            tasks = json.load(fh)["tasks"]
        result = plan(tasks)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
