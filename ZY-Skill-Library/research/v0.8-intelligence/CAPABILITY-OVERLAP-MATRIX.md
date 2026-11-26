# CAPABILITY-OVERLAP-MATRIX — ZY v0.8 Intelligence Audit

Audit unit: capabilities, not repository names. Existing coverage is taken from the 115-skill registry (`SKILL_REGISTRY.json`, 2026-11-25). Candidate IDs refer to `MASTER-REPOSITORY-REGISTER.md`.

Overlap classes: UNIQUE, PARTIAL OVERLAP, FULL DUPLICATE, CONFLICTING (with policy or with an existing skill), OBSOLETE, UNNECESSARY, UNVERIFIED.

Rule applied: no new skill is created for a capability that already has coverage, unless a measurable gap is shown.

## 1. Matrix

| # | Capability | Existing ZY coverage (registry names) | Candidates (IDs) | Overlap class | Decision and consolidation |
|---|---|---|---|---|---|
| C01 | Agent planning, TDD, debugging, verification discipline | superpowers set (brainstorming, writing-plans, executing-plans, test-driven-development, systematic-debugging, verification-before-completion, subagent-driven-development, requesting-code-review, receiving-code-review, using-git-worktrees, finishing-a-development-branch, writing-skills, using-superpowers, dispatching-parallel-agents); skill-engineering-standard; quality-gate | 01 ECC; 04 Superpowers | FULL DUPLICATE (01); MERGE (04) | No new skill. ECC workflow concepts are already represented. Keep the imported superpowers set. 14 of 15 present; `diagnosing-superpowers` is the only unimported one (DEFER) |
| C02 | Human approval gate for plans and diffs | None as a skill. Approval protocol exists in standing instructions | 07 Plannotator (tool); 16 AG-UI (approval events) | PARTIAL OVERLAP (concept) | KNOWLEDGE. Write an approval-gate procedure in ZY instructions. No tool |
| C03 | Code review | requesting-code-review; receiving-code-review; secret-leak-scan | 05 Open Code Review; 07 Plannotator (code review) | PARTIAL OVERLAP | DEFER tool (LLM egress, lifecycle script). Review rubric stays in the existing review skills |
| C04 | Persistent cross-session memory | None. Environment memory directories are not a ZY skill | 03 claude-mem (REJECT); 01 ECC memory hooks (REJECT); 02 Graphify (DEFER) | UNIQUE GAP | Design a local, bounded project-memory standard owned by ZY. No cloud, no hooks, no daemon. Not implemented in this package |
| C05 | Codebase knowledge graph and architecture map | None | 02 Graphify (DEFER); 08 GitDiagram (REJECT); 27 Diagram Design (ADAPT) | UNIQUE GAP (partly) | Diagram rules from 27 (ADAPT). Local graph from 02 only after verification (Dart support, no network path) |
| C06 | Browser verification and debugging | webapp-testing (VERIFIED, local Playwright) | 17 Chrome DevTools MCP | PARTIAL OVERLAP | MERGE: debugging and accessibility checks as knowledge into webapp-testing. No MCP (live browser profile exposure) |
| C07 | Web research and content retrieval | citation-management (WebSearch, WebFetch); markitdown-converter (local files); claude-api and mcp-builder mention web fetch as instructions | 18 Agent Reach (REJECT); 19 Scrapling (REJECT); 20 Last30Days (REJECT); Firecrawl set (REJECT or DEFER, see v0.8 backlog) | CONFLICTING (policy) | No new scraping skill. Public, read-only retrieval only through existing tools and an allowlist (K5). Cookie, login, bypass and social-scrape paths are prohibited |
| C08 | Local document-to-Markdown with loss guard | markitdown-converter (VERIFIED) | Firecrawl FC-07 (earlier audit) | PARTIAL OVERLAP | K4: extend markitdown-converter with loss detection and fallback. Not a new skill |
| C09 | Turning arbitrary software into CLIs | None | 21 CLI-Anything (REJECT) | UNNECESSARY | REJECT. Registry-based installs and broad app automation are out of scope |
| C10 | Visual design critique and UI quality gate (K7 gap) | frontend-design (IMPORTED); web-artifacts-builder; theme-factory; brand-guidelines; quality-gate (video only) | 22 Impeccable (ADAPT); 23 Hallmark (MERGE); 37 Motionmaxxing (rubric, KNOWLEDGE); 40 Dream Loop (bounded-loop concept); 24 Astryx and 25 Shadcn Admin (DOMAIN, web only) | UNIQUE GAP, now partly filled | One consolidated design-quality rubric (critique, audit, anti-generic gates, reduced-motion, contrast, layout checks), no hooks, no npx, no cloud. Feeds K7 |
| C11 | Design tokens and DESIGN.md | theme-factory; brand-guidelines | ST-01 taste-design (earlier, ADAPT); ST-02 design-md (ADAPT); ST-03 extract-design-md (ADAPT, local mode); UI/UX Pro Max data (MERGE); 27 Diagram Design (palette onboarding) | PARTIAL OVERLAP | K1 remains the single design-token skill. Sources: taste rules, schema, local extraction, UI/UX Pro Max data after licence and pinning |
| C12 | Web-platform guidance (CSS, HTML, JS, accessibility) | accessible-animation; micro-interaction; svg-animation; accessibility-as-code (flutter) | 26 Modern Web Guidance (ADAPT) | PARTIAL OVERLAP (accessibility of motion) | ADAPT a pinned, offline subset. No `@latest`, no cron |
| C13 | Motion graphics and timeline animation | motion-graphics; remotion-motion-graphics; threejs-animation; svg-animation; micro-interaction; accessible-animation; creating-canvas-video-animations | 36 GSAP Skills (ADAPT); 37 Motionmaxxing (KNOWLEDGE); 30 HyperFrames (DEFER) | PARTIAL OVERLAP | ADAPT GSAP guidance. Do not add a second renderer: Remotion is the existing one. HyperFrames stays DEFER |
| C14 | End-to-end video pipeline (edit, render, QC) | ffmpeg-skill (IMPORTED); remotion-motion-graphics; quality-gate (video QC); narration-subtitle-sync; creating-canvas-video-animations | 29 OpenMontage (REJECT); 30 HyperFrames (DEFER); 31 ffmpeg-skill (MERGE, update review) | PARTIAL → FULL DUPLICATE risk | No second end-to-end pipeline. Use the existing stack. Review the ffmpeg-skill upstream diff before any re-import |
| C15 | Shot composition and cinematic recipes | cinematic-camera (IMPORTED); cinematic-3d-camera; cinematic-storyboarding | 35 Video Shotcraft (ADAPT recipe data) | PARTIAL OVERLAP | ADAPT the recipe cards as data into cinematic-storyboarding after a diff. No runtime code |
| C16 | Narration, TTS and voice | elevenlabs-narration (custom; live BLOCKED); narration-subtitle-sync (custom); audio-mixing-mastering (IMPORTED); procedural-sfx (IMPORTED) | 33 Voicebox (DEFER); 34 VoiceStudio (REJECT); 43 (paid-API helpers, REJECT) | PARTIAL OVERLAP; GAP for Japanese and Indonesian narration | Evaluate 33 under the benchmark plan (languages, hardware, consent). Indonesian support not evidenced |
| C17 | 3D web and browser games | threejs-* (14, IMPORTED via alton47); game-mechanics; cinematic-3d-camera | 43 Three.js Game Skills (ADAPT subset); 42 3Dviz Pro Max (DEFER); 44 Anatomy (DOMAIN) | PARTIAL OVERLAP | MERGE 43 guidance into the threejs domain after a diff. Drop paid-API helpers |
| C18 | Blender 3D pipeline | None | 39a EL4CTEO blender-skills (DOMAIN candidate, identity unresolved); 38 MCP for Blender (REJECT); 39b arjun988 (REJECT) | UNIQUE GAP | BLOCKED until the owner confirms the intended repository. No MCP |
| C19 | Local visual generation (image or video models) | None for visual generation. audio-mixing-mastering is audio only | 41 ComfyUI (DEFER); 32 MotionClone (REJECT); 40 Dream Loop (REJECT) | UNIQUE GAP, hardware-blocked | DEFER. The GTX 1650 with 4 GB VRAM is below the stated requirements of these tools |
| C20 | Engineering and electrical diagrams | None (automation, industrial-utility and engineering skills exist but do not draw diagrams) | 27 Diagram Design (ADAPT); 44 Anatomy (DOMAIN, explainers) | UNIQUE GAP | ADAPT 27 for engineering documentation. DOMAIN for 44 in education |
| C21 | Local LLM runtime | None | 13 Ollama (DOMAIN); 10 OmniRoute (REJECT); 11 FreeLLMAPI (REJECT); 14 OpenHands (REJECT) | UNIQUE GAP, hardware-limited | DOMAIN for 13 with owner approval and verified binary only |
| C22 | Agent-to-UI event protocol | None | 16 AG-UI (KNOWLEDGE ONLY) | UNIQUE (reference) | KNOWLEDGE. Relevant only if a ZII web interface is approved |
| C23 | Quantitative research and backtesting | strategy-backtesting (custom); trade-statistics; position-size-calculator; portfolio-metrics-quantstats (IMPORTED); xauusd-smc-analysis (custom); smartmoneyconcepts (dependency) | 47 Qlib (KNOWLEDGE ONLY); 46 Vibe-Trading (REJECT; validation methods → KNOWLEDGE); 48 TradingAgents (REJECT); 49 FinGPT (DEFER) | PARTIAL OVERLAP; GAP: walk-forward and out-of-sample validation | KNOWLEDGE. Implement a small validator in ZY code later (not in this package). Research and paper only |
| C24 | Trading methodology: journal, risk, review | trade-statistics (partial); position-size-calculator | 45 Claude Trading Skills (ADAPT methodology, paper-only) | PARTIAL OVERLAP; journaling UNIQUE | ADAPT methodology docs. Exclude FMP API paths, launchd jobs and any broker data path |
| C25 | Live trading or broker integration | None, by policy | 06 Cursor plugins (brokerage MCP); 46 Vibe-Trading (broker order tool); 45 (Alpaca references in docs) | CONFLICTING with policy | REJECT. No broker credentials, no order placement |
| C26 | Long-form narrative continuity (character, timeline, worldbuilding) | novel-typesetting; manhwa-production; documentary-production; literature-review; citation-management; citation-verification | 50 MuMuAINovel (KNOWLEDGE ONLY, GPL) | PARTIAL OVERLAP; GAP: character and timeline memory (M3) | KNOWLEDGE for a continuity design. No GPL code reuse |
| C27 | Mobile store-release compliance | flutter set (8, including accessibility-as-code and testing-strategy); governance set | 28 App Store Compliance (KNOWLEDGE ONLY; licence pending) | UNIQUE GAP (store policy checklist) | KNOWLEDGE. Re-author any checklist after the canonical licence is reviewed |
| C28 | Flutter UI intelligence (palettes, typography, stack rules) | flutter set (8); design skills in K1 | UI/UX Pro Max data (MERGE into K1, only if K1 is approved); 22 Impeccable (critique rules) | PARTIAL OVERLAP | Data source for K1 only after licence (MIT, OFL fonts, per-font check) and pinning. flutter.csv covers Flutter rules |
| C29 | Security review: authorization, authentication, API | secret-leak-scan (VERIFIED); third-party-skill-audit; supabase and supabase-postgres-best-practices (RLS guidance) | BugHunter CB-02/CB-03 (K2) | PARTIAL OVERLAP (RLS covered) | K2 remains, defensive checklists only, excluding RLS already covered |
| C30 | Dependency and CVE scanning | secret-leak-scan (secrets only) | BugHunter CB-05 (K6) | UNIQUE GAP | K6, after a licence-clear vulnerability data source is approved |
| C31 | Outbound data control and deny-by-default policy | third-party-skill-audit (scanner) | Policy in this package (K9 decisions) | UNIQUE (policy) | Adopt the policy as governance text. No third-party code |

## 2. Summary of overlap classes

| Class | Count (capabilities) | Capabilities |
|---|---|---|
| FULL DUPLICATE | 1 (C01 for ECC concepts) | C01 |
| PARTIAL OVERLAP | 16 | C02, C03, C06, C08, C11, C12, C13, C14, C15, C16 (also UNVERIFIED on Indonesian coverage), C17, C23, C24, C26, C28, C29 |
| CONFLICTING | 2 | C07 (policy for retrieval), C25 (broker integration) |
| UNIQUE GAP | 9 | C04, C05, C10 (partly filled), C18, C19, C20, C21, C27, C30 |
| UNIQUE (concept or reference) | 2 | C22, C31 |
| UNNECESSARY | 1 | C09 |
| OBSOLETE | 0 | — |
| UNVERIFIED (to be checked) | 1 | C16 (Indonesian coverage) |

Note: a capability can appear once only; the table above is a count of primary class per row.

## 3. Consolidation outcome

- Design quality: C10 and C11 converge on one design-quality rubric and one design-token skill (K7 and K1). The earlier K1 list gains the UI/UX Pro Max data source only under approval.
- Motion: C12 and C13 keep GSAP guidance (36) and reject a second renderer. Motionmaxxing remains a rubric reference.
- Video: C14 and C15 keep the existing stack. Video Shotcraft contributes recipe data only.
- Research: C07 stays with existing tools. No new fetch capability without the K5 allowlist.
- Trading: C23, C24 and C25 keep research and paper methodology only. Live-trading paths are rejected by policy.
- Memory: C04 is the largest unique gap. It is a design item, not a tool adoption.
