# INTELLIGENCE-ARCHITECTURE-V0.8 — Proposed target state

Status: PROPOSAL. Nothing in this document is implemented. Every component is either an existing ZY component (named) or a proposed item awaiting owner approval (marked PROPOSED).

Design goal: a small, always-loaded governance core; domain capabilities loaded on demand; no external runtime inside the library; deny-by-default data egress; every component traceable to a verified source and a rollback path.

## 1. Layers

```
L0  GOVERNANCE CORE            always loaded, small
    - deny-by-default egress, Rp0, approval gates, identity and licence gate
    - existing: AGENTS.md, CLAUDE.md, skill-engineering-standard, third-party-skill-audit
    - PROPOSED: approval-gate procedure (C02)

L1  ROUTER AND REGISTRY        index only, loaded per task
    - existing: SKILL_REGISTRY.json (115 entries), scripts/route_skill.py,
      references/project-profiles.json (14), references/skill-constraints.json
    - PROPOSED: profiles for the GAP rows in PROJECT-DOMAIN-MATRIX.md (owner decision)

L2  DOMAIN CAPABILITIES        loaded on demand by router
    - existing: 115 skills (see CAPABILITY-OVERLAP-MATRIX.md)
    - PROPOSED ADAPT modules (only after approval): design-quality review (K7/K1),
      web-platform guidance subset, engineering diagrams, GSAP motion guidance,
      cinematic shot recipes (data), Three.js game patterns, trading methodology (paper)
    - PROPOSED CUSTOM (design, no third-party code): project memory standard (C04),
      walk-forward and out-of-sample validation procedure (C23)

L3  KNOWLEDGE (data)           read on demand, never preloaded
    - existing: CSV and JSON reference data inside skills
    - PROPOSED: UI/UX Pro Max data as a K1 data source only after licence and per-font checks
    - Rule: data files are read with a query, not dumped into context

L4  EXTERNAL TOOLS             quarantined; never global; never by default
    - None installed. Any tool requires owner approval, a pinned version and commit,
      a dedicated folder, no hooks, no MCP unless approved, and an egress allowlist
    - Rejected classes: remote MCP, global installers, pipe-to-shell, `@latest`

L5  PROJECT MEMORY             local, bounded, explicit writes only
    - PROPOSED per-project `memory/` folder with markdown entries:
      frontmatter (source, date, owner-approved yes or no), capped summary size per entry
    - No cloud sync. No automatic capture. No embeddings in the first version
      (keyword retrieval through the existing router approach)

L6  CROSS-AGENT ADAPTERS       SKILL.md is canonical
    - Claude Code: native skill folders (verified in this environment)
    - Other agents: ADAPTABLE or REFERENCE ONLY until tested (see CROSS-AGENT-COMPATIBILITY.md)
    - No hook dependence in any core component

L7  EVALUATION AND ROLLBACK    proposed harness, nothing executed
    - BENCHMARK-AND-ROLLBACK-PLAN.md; registry validation; git revert for rollback
```

## 2. Admission gate for any new component

A component is admitted only if all of the following hold, recorded in its ADAPTATION.md or SOURCE.md:

1. Capability gap confirmed against the registry (CAPABILITY-OVERLAP-MATRIX.md).
2. Canonical identity verified; upstream commit pinned.
3. Licence clear; attribution and NOTICE carried; no copyleft code reuse.
4. No hooks, no MCP, no installer that writes outside its own folder.
5. Network: none, or an explicit allowlist approved by the owner.
6. Credentials: none. Telemetry: none, verified by code reading.
7. Cost: Rp0 for the adopted form. Paid APIs are excluded.
8. Hardware: fits the stated constraints, or is marked DEFER.
9. A benchmark exists in the plan and a rollback is written.
10. Existing validation passes (`validate_library.py`, registry check, tests).

Any failed gate blocks admission. A high usefulness score does not override a failed gate.

## 3. What is deliberately not built

| Not built | Reason | Candidates |
|---|---|---|
| Persistent memory daemon or cloud memory | Data egress; hooks | 03, 01 |
| MITM, root CA, provider pooling | Prohibited | 10, 11 |
| Broker or order placement path | Prohibited (no broker credentials) | 06, 46 |
| Cookie or login-based scraping | Prohibited | 18, 19, 20 |
| Autonomous trading, unattended agents | Out of scope | 14, 48 |
| A second end-to-end video renderer | Duplicates Remotion | 29, 30 |
| Global installers and `-g` installs | Protocol prohibition | 21, 44 (`-g`) |
| Offensive tooling | Prohibited | 09, 51 |

## 4. Token economy (rules; not measured)

- Registry index only at routing time. Full SKILL.md only for the top candidate. References only when a step needs them.
- Byte budget per task (proposed): cap the number of loaded SKILL.md files at three per task. Measured values are pending the benchmark plan; the current value is a design target, not a finding.
- No broad subagent fan-out for research tasks. Parallelism is capped and each worker's output is summarised before return.
- Retries are bounded (maximum two) and logged.
- Maintenance estimate: each adopted ADAPT module adds one upstream to re-audit on each release; each pin needs an update review. Expected maintenance is proportional to the number of pins, so the pin count is kept small.

## 5. How this maps to existing ZY components

| Architecture element | Existing component | Change proposed |
|---|---|---|
| Governance core | AGENTS.md, CLAUDE.md, skill-engineering-standard, third-party-skill-audit | Add the admission gate (section 2) as a reference document |
| Registry | SKILL_REGISTRY.json, build_registry.py | Unchanged; new entries only after approval |
| Router | route_skill.py, project-profiles.json, skill-constraints.json | New profiles for GAP rows (owner decision); constraints for palette conflicts (K1) |
| Adaptation tracking | ADAPTATION.md, import_upstream.py, import_personal.py | Use for every ADAPT item |
| Validation | validate_library.py, tests/ | New tests for each approved module |
| Research record | research/, BACKLOG-V0.8.md | This package and the updated backlog |

## 6. Open architecture questions (owner input)

1. Is project memory wanted at all, given the data-egress policy? The local design in L5 is the only variant proposed.
2. Which of the six GAP rows (section 1 of PROJECT-DOMAIN-MATRIX.md) should become profiles?
3. Should K7 (visual QA gate) be a separate module or a section of K1?
4. Is a local Ollama runtime wanted, given the GTX 1650 4 GB constraint? If yes, which model size class is acceptable?
