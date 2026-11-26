# BENCHMARK-AND-ROLLBACK-PLAN — ZY v0.8 Intelligence Audit

Status of every benchmark below: PROPOSED. NOT EXECUTED. No benchmark result is claimed in this package.

Rules:
- No external component is executed to produce a benchmark result unless the owner approves that component.
- Fixtures are ZY-owned, synthetic, or public-domain / CC0 / permissively licensed material with the licence recorded.
- No live trading, no broker credentials, no market data that lacks a clear licence. Forex benchmarks are research and paper only.
- No guaranteed win-rate or profit claim is permitted. Forex benchmarks report risk and validation metrics only.
- Token consumption cannot be measured in every runtime. Where measurement is not possible, the benchmark is recorded as NOT MEASURABLE.

## 1. Core AI

| ID | Task (proposed) | Fixture | Metric | Acceptance (proposed) | Applies to |
|---|---|---|---|---|---|
| B-CORE-1 | Instruction comprehension: follow a multi-step instruction with an explicit stop point | ZY-owned instruction set of 10 items | Items completed correctly; stop respected | 10 of 10 completed; stop respected | Governance core (L0) |
| B-CORE-2 | Flutter bug investigation on a seeded defect | ZY-owned small Flutter project with one defect | Defect located; fix proposed; no unrelated edit | Located and fixed in a scratch copy | Flutter skills (existing) |
| B-CORE-3 | Codebase architecture discovery | ZY-owned repository of 30 files | Correct module map (precision, recall) | Recall ≥ 0.8 on named modules | C05 (diagram), router |
| B-CORE-4 | Cross-session continuity | Two sessions with notes stored by the memory standard | Facts recovered from memory alone | ≥ 0.9 of facts recovered; no unlisted facts | B-MEM-1, P12 |
| B-CORE-5 | Code review of a seeded diff | ZY-owned diff with 5 defects | Defects found; false positives | ≥ 4 of 5 found; ≤ 1 false positive | P09 (review rubric) |
| B-CORE-6 | Regression prevention | Test suite run before and after a seeded change | Regressions caught | 100% of seeded regressions caught | Existing tests |
| B-CORE-7 | Token consumption | Same task with and without a candidate skill loaded | Input and output tokens | NOT MEASURABLE unless the runtime reports tokens. Previously NOT TESTED (v0.6) | All ADAPT items |
| B-MEM-2 | Retrieval relevance of project memory | Synthetic memory entries (100) and 20 queries | Precision at 3 | ≥ 0.8 precision at 3 | P12 |

## 2. Creative production

| ID | Task (proposed) | Fixture | Metric | Acceptance (proposed) | Applies to |
|---|---|---|---|---|---|
| B-CRE-1 | Vertical 9:16 video render | ZY-owned 4-second composition | Resolution, duration, fps, file integrity | Matches spec exactly | Existing render-link-builder; qc_gate |
| B-CRE-2 | Smooth motion graphics | ZY-owned animation with eased keyframes | Frame-to-frame jitter; motion-curve smoothness | Jitter below threshold set in the rubric | P05 (GSAP), P06 (recipes) |
| B-CRE-3 | Audio synchronisation | ZY-owned narration and beat track | Offset of cue times from target (ms) | ≤ 50 ms median offset | narration-subtitle-sync |
| B-CRE-4 | Indonesian human-like narration | Short ZY-owned Indonesian script | Intelligibility by owner rating; naturalness | Owner rating ≥ 4/5; no paid API | D2 (Voicebox), elevenlabs-narration (BLOCKED live) |
| B-CRE-5 | Japanese pronunciation | ZY-owned Japanese script with pitch-accent check | Owner rating; mora-timing check | Owner rating ≥ 4/5 | D2; JLPT profile |
| B-CRE-6 | Sound effects | ZY-owned SFX list | Loudness target met; clipping absent | Loudness and clipping checks pass | procedural-sfx; audio-mixing-mastering |
| B-CRE-7 | Editable production assets | ZY-owned project folder | Assets editable and reproducible | Re-render identical | P06; remotion-motion-graphics |
| B-CRE-8 | Rendering reliability | Same composition rendered 10 times | Failures; output hash variance | 0 failures; deterministic output | ffmpeg-skill; existing renderers |

## 3. Design

| ID | Task (proposed) | Fixture | Metric | Acceptance (proposed) | Applies to |
|---|---|---|---|---|---|
| B-UI-1 | Design-quality review of a seeded page | ZY-owned HTML page with 8 known defects (contrast, focus, motion, layout) | Defects found; false positives | ≥ 7 of 8 found; ≤ 2 false positives | P01 |
| B-UI-2 | DESIGN.md token extraction from source code | ZY-owned small project with 3 palettes | Tokens extracted correctly | All palette tokens recovered | P02 (mode A) |
| B-UI-3 | Accessibility check against guidance | ZY-owned page | Checklist items covered | All selected guidance items addressed | P03 |
| B-UI-4 | Flutter UI improvement | ZY-owned Flutter screen with 5 seeded issues | Issues fixed; analyzer clean | 5 of 5 fixed in a scratch copy; analyzer reports no new issues | K1 (Flutter data) |
| B-UI-5 | Responsive dashboard | ZY-owned dashboard fixture at 375, 768, 1024, 1440 px | Layout overflow count | 0 overflow at four widths | P03; ZII dashboards |
| B-UI-6 | Accessibility (functional) | Keyboard-only navigation of ZY-owned page | Reachable controls; focus visible | 100% of controls reachable | P01, P15 |
| B-UI-7 | Visual consistency | Two screens with a shared token set | Token drift count | 0 drift | P02 |
| B-WEB-1 | Functional browser verification | webapp-testing with a ZY-owned local server | Pass or fail on scripted flow | Scripted flow passes | P15 |
| B-WEB-2 | Browser-debugging knowledge applied | Seeded accessibility or performance issue | Issue located with the recommended step | Located in 3 of 3 seeded cases | P15 |

## 4. Engineering

| ID | Task (proposed) | Fixture | Metric | Acceptance (proposed) | Applies to |
|---|---|---|---|---|---|
| B-ENG-1 | Technical diagram of a ZY-owned system | Block description (8 blocks) | Blocks and links drawn; no external resource | All blocks and links present; no external resource | P04 |
| B-ENG-2 | Electrical motor simulation | Existing motor-starting-sizing inputs | Result equals the reference hand calculation | Within 1% of the hand calculation | Existing motor-starting-sizing |
| B-ENG-3 | Industrial system visualisation | ZY-owned SCADA tag set | Tags shown with alarm levels | All tags and alarm levels shown | Existing scada-tag-engineering |
| B-ENG-4 | Technical diagram with standards references | Diagram and text with cited standards | Every cited standard verified to an owner-supplied primary source | No unverified citation | P04; M2 (PUIL) |
| B-ENG-5 | Physical and mathematical accuracy | Existing calculation skills | Reference values match | Matches reference values within stated tolerance | Existing engineering skills |

## 5. Game development

| ID | Task (proposed) | Fixture | Metric | Acceptance (proposed) | Applies to |
|---|---|---|---|---|---|
| B-GAM-1 | Interactive 3D scene | ZY-owned Three.js scene | Scene loads; interactions respond | Loads and responds in test browser | P07 |
| B-GAM-2 | Character movement | ZY-owned controller | Position error after scripted path | Error below threshold in rubric | P07 |
| B-GAM-3 | Mobile rendering performance | ZY-owned scene at mobile profile | Frame time, draw calls | Measured against threshold; NOT MEASURABLE on owner device until tested | P07 |
| B-GAM-4 | Narrative consistency | ZY-owned story bible with 20 facts | Contradictions introduced | 0 contradictions | C26 (proposed) |

## 6. Forex and quantitative research (research and paper only)

Metrics are defined before any run. No win-rate target is set. No live or broker path is tested.

| ID | Task (proposed) | Fixture | Metric | Acceptance (proposed) | Applies to |
|---|---|---|---|---|---|
| B-TRD-1 | Historical XAUUSD research | Licensed or owner-supplied OHLC data only (M1 unresolved) | Data completeness; gaps | Gaps reported, none filled silently | P08; strategy-backtesting |
| B-TRD-2 | Spread and slippage | Fixture with bid-ask data | Net result after spread and slippage | Model parameters stated; sensitivity table produced | P14 |
| B-TRD-3 | Transaction costs | Fee schedule input (owner-supplied) | Costs deducted per trade | Costs deducted in every trade | Existing backtest.py (fee model) |
| B-TRD-4 | Look-ahead bias prevention | Synthetic series with an injected future leak | Leak detected | Test fails when a leak is injected | P14 |
| B-TRD-5 | Out-of-sample testing | Walk-forward split of the historical fixture | In-sample and out-of-sample metrics reported separately | Reported separately; no tuning on out-of-sample | P14 |
| B-TRD-6 | Expectancy, profit factor, maximum drawdown | Trade list from the fixture | Metrics computed by definition | Matches reference computation | trade-statistics (VERIFIED) |
| B-TRD-7 | Trading journal and review | Owner-written sample journal | Review completeness | All required fields present | P08 |

## 7. Literature and storytelling

| ID | Task (proposed) | Fixture | Metric | Acceptance (proposed) | Applies to |
|---|---|---|---|---|---|
| B-LIT-1 | Character continuity | ZY-owned manuscript with 5 characters over 3 chapters | Continuity errors detected | ≥ 4 of 5 seeded errors detected | C26 (proposed) |
| B-LIT-2 | Timeline consistency | ZY-owned timeline with 10 events and 2 seeded conflicts | Conflicts found | Both conflicts found | manuscript_check (existing) |
| B-LIT-3 | Worldbuilding consistency | ZY-owned worldbuilding notes | Rule violations found | All seeded violations found | C26 |
| B-LIT-4 | Long-form narrative coherence | ZY-owned 20-page excerpt | Coherence review by owner rating | Owner rating ≥ 4/5 | novel-typesetting; C26 |

## 8. Execution order (when approved)

1. Core AI (B-CORE-1 to 6) before any skill is adopted, to establish the baseline without the candidate.
2. Per item: run the item's benchmark with and without the candidate, under the same fixtures.
3. Record the result as MEASURED, NOT MEASURABLE, or NOT EXECUTED, with the exact command and output.
4. An item whose benchmark fails its acceptance is rolled back, not tuned until it passes.

## 8a. Supporting benchmarks referenced by SELECTIVE-INTEGRATION-PROPOSAL.md

| ID | Task (proposed) | Fixture | Metric | Acceptance (proposed) | Applies to |
|---|---|---|---|---|---|
| B-MEM-1 | Memory entry format and size cap | ZY-owned entries, valid and invalid | Entries rejected when frontmatter or size cap fails | 100% of invalid entries rejected | P12 |
| B-SEC-1 | Defensive review on a seeded application | ZY-owned application with 5 seeded defects (authorisation, authentication, API); no payloads | Defects found; false positives | ≥ 4 of 5 found; ≤ 1 false positive | P09 |
| B-SEC-2 | Artefact leak check | ZY-owned build folder with 3 seeded leaks (source map, `.git`, `.env`) | Leaks detected | 3 of 3 detected; ≤ 1 false positive | P10 |
| B-DOC-1 | Loss detection for JavaScript-rendered content | ZY-owned HTML page whose main text is rendered by script | Page flagged as lossy | Flagged in the seeded case; not flagged for a static page | P11 |
| B-DOC-2 | Documentation consistency | Output of validator and unit tests | Numbers in README and PROGRESS equal validator output | 0 mismatches | P17 |
| B-GOV-1 | Approval-gate decision log | Synthetic plan with 3 decisions | Each decision recorded with owner, date, and STOP point | 3 of 3 complete | P13 |
| B-VOI-1 | Narration candidate (Voicebox) benchmark | Short Indonesian and Japanese ZY-owned scripts; owner hardware only | Engine, language, VRAM, real-time factor, owner rating | Recorded per engine; no paid API used | D2 (DEFER) |

Supporting benchmarks: 7. Total proposed benchmarks: 45 (sections 1–7) + 7 (section 8a) = 52.

## 9. Rollback procedure (applies to every item P01–P17)

1. Identify the commit that introduced the item (`git log --oneline -- <path>`).
2. Revert with `git revert <commit>`. Do not use `git reset`. Do not force push.
3. If the item created a new folder, delete the folder only after confirming from its `ADAPTATION.md` or `SOURCE.md` that ZY created it.
4. Rebuild the registry: `python scripts/build_registry.py`.
5. Validate: `python scripts/validate_library.py` and `python scripts/build_registry.py --check`.
6. Run unit tests in the venv: `python -m unittest discover -s tests -t tests -p "test_*.py"` (run from `ZY-Skill-Library/`).
7. Confirm frozen baselines are still ancestors of HEAD: `git merge-base --is-ancestor 7039fed HEAD` and `git merge-base --is-ancestor 940368f HEAD`.
8. Record the rollback in `research/BACKLOG-V0.8.md` with the item ID and reason.
9. Pushing a revert to `ccr-57e40ec8-e8i3fa` requires owner approval for that push.

Expected cost of rollback: Rp0. Expected time: a few minutes per item (estimate, not measured).

## 10. Status summary

| Item | Status |
|---|---|
| Benchmarks proposed | 52 (45 in sections 1–7; 7 in section 8a) |
| Benchmarks executed | 0 |
| Benchmarks with measured results | 0 |
| Token consumption measured | 0 (NOT MEASURABLE in this runtime) |
