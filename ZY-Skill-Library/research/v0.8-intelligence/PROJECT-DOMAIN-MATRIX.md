# PROJECT-DOMAIN-MATRIX — ZY v0.8 Intelligence Audit

Sources: owner intelligence profile (sections A–H of the protocol) and the 14 project profiles in `references/project-profiles.json`. Candidate IDs refer to `MASTER-REPOSITORY-REGISTER.md`. Relevance here means fit with a stated need, not a judgement of quality.

Scale: HIGH (addresses a stated need with a verified fit), MEDIUM (useful with a clear condition), LOW (marginal), NONE.

## 1. Profile coverage check

| Owner domain or project | Profile in registry | Status |
|---|---|---|
| AmiraVerse | amiraverse | Covered |
| Money App | money-app | Covered |
| DEAMIRA | deamira | Covered |
| ZII Industrial Intelligence | zii | Covered |
| ZY Skill Library (self) | none (meta) | Governed by this package |
| EarthStop | earthstop | Covered (cinematic-camera override exists) |
| SISI GELAP TOKOH | sisi-gelap-tokoh | Covered |
| Sebelum Sepi Menjadi Rumah | none | **GAP: no profile and no brief in the registry** |
| AmiraVerse promotional content | amiraverse (same profile) | Covered, but promo-specific needs not separated |
| Silent Neon Tokyo (game, manhwa) | silent-neon-tokyo-game; silent-neon-tokyo-manhwa | Covered |
| XAUUSD ICT/SMC (research and paper only) | xauusd | Covered |
| JLPT N5–N1 | jlpt | Covered |
| Teknik Elektro and Industrial Utility | teknik-elektro | Covered; WTP/WWTP and boiler/compressor not separated |
| Novel writing | novel | Covered |
| Film production | film-sinematik | Covered |
| ClipACanvas | clipacanvas | Covered |
| Commercial advertising | none | **GAP** |
| Educational explainers | none | **GAP** (partly served by 44 Anatomy in education) |
| Android and browser games (beyond Silent Neon Tokyo) | none | **GAP** |
| Realistic environments (3D) | none | **GAP** |
| WTP and WWTP | none | **GAP** |

Owner decision needed: whether the six GAP rows above become profiles, and what the brief is for Sebelum Sepi Menjadi Rumah.

## 2. Matrix

| Domain or project | Stated need | HIGH | MEDIUM | LOW or NONE | Gap or condition |
|---|---|---|---|---|---|
| A. AI reasoning, memory, context engineering, token optimisation | Persistent memory; context budget | 04 Superpowers (already imported) | 01 ECC (concepts), 07 Plannotator (approval concept), 16 AG-UI (protocol reference), 03 claude-mem (concept only) | 14, 48 (REJECT) | Memory standard (C04) is a design gap |
| A. Multi-agent orchestration and autonomous execution | Orchestration with approval gates | 04 (imported skills) | 07 (approval concept), 16 (event contracts) | 14, 48 (REJECT) | Approval-gate procedure (C02) |
| A. Local AI | Local inference | — | 13 Ollama (DOMAIN, approval) | 41 ComfyUI (DEFER), 10, 11 (REJECT) | Hardware: GTX 1650 4 GB, 16 GB RAM |
| A. Research intelligence | Source reliability | none | 20 Last30Days (methodology only), 47 Qlib (validation) | 18, 19 (REJECT) | Public, read-only retrieval only (K5 allowlist) |
| B. Flutter and Dart (AmiraVerse, Money App) | Architecture, UI, testing | 28 App Store Compliance (KNOWLEDGE, licence pending); 22 Impeccable (critique rules) | 23 Hallmark (gates); UI/UX Pro Max Flutter data via K1 | 26 Modern Web Guidance (web only), 24 Astryx (React only) | Dart support of 02 Graphify and 05 OCR unverified |
| B. Android applications | Store release | 28 (KNOWLEDGE) | 22, 23 (UI gates) | 34 VoiceStudio (AGPL) | Store-policy checklist (C27) |
| B. Web applications | UI/UX, accessibility, browser checks | 26 Modern Web Guidance (ADAPT); 22; 23 | 17 Chrome DevTools (knowledge into webapp-testing); 27 Diagram Design | 24, 25 (web-only, DOMAIN) | ZII web decision |
| B. Supabase and PostgreSQL, backend, API | Authorisation, RLS, API security | Existing supabase skills (RLS covered) | K2 defensive checklists (BugHunter CB-02/03 subset, RLS excluded) | 40 (no backend) | None beyond K2 |
| B. Security and testing | Authorised defensive review; secrets | secret-leak-scan (existing); K3 (artefact checks, from BugHunter CB-04) | K2; 17 (browser verification knowledge) | 09 REA, 51 Hacking-Tools (REJECT); 18–20 (REJECT) | Dependency CVE (K6) |
| B. UI/UX design | Visual QA, tokens, consistency | 22 Impeccable (ADAPT); 23 Hallmark (MERGE); K1 | 26, 27; UI/UX Pro Max data (MERGE into K1) | 24, 25 (DOMAIN, web) | Visual QA gate (K7) |
| C. Cinematic filmmaking (EarthStop, Film, SISI GELAP) | Shot grammar, camera, pacing | 35 Video Shotcraft (recipe data, ADAPT) | cinematic-camera (existing), cinematic-storyboarding (existing), 37 Motionmaxxing (rubric) | 29 OpenMontage (REJECT, AGPL) | Golden Master criteria (V7); palette override for neon (ST-01) |
| C. Documentary videos (SISI GELAP TOKOH) | Source verification | claim_ledger (existing) | 02 Graphify (DEFER: knowledge graph of research notes, if local) | 46, 45 (not relevant) | Source verification stays with a human (M11) |
| C. Motion graphics and 2D/3D animation | Timeline motion, easing | 36 GSAP Skills (ADAPT); existing motion-graphics; remotion-motion-graphics | 30 HyperFrames (DEFER, telemetry); 37 (rubric) | 32 MotionClone (REJECT) | Second renderer not added (C14) |
| C. Realistic environments and 3D scenes | 3D scenes, lighting | 43 Three.js Game Skills (ADAPT subset); threejs-* (existing) | 42 3Dviz (DEFER); 44 Anatomy (explainers) | 38 (REJECT); 39 (BLOCKED); 41 (DEFER) | Blender identity (39, BLOCKED) |
| C. Video editing and rendering | Pipeline, FFmpeg | ffmpeg-skill (existing; update review, 31) | remotion-motion-graphics (existing) | 29 (REJECT) | None |
| C. Human-like narration | Natural voice; Indonesian and Japanese | 33 Voicebox (DEFER; 23 languages incl. Japanese) | elevenlabs-narration (existing; live BLOCKED); narration-subtitle-sync (existing) | 34 VoiceStudio (REJECT), 43 paid-API helpers (REJECT) | Indonesian not evidenced; benchmark required |
| C. Sound design and SFX | SFX, mixing | audio-mixing-mastering, procedural-sfx (existing) | — | — | None |
| C. Music synchronisation | Beat alignment | narration-subtitle-sync (timing); existing audio skills | — | — | Dedicated beat-sync not evaluated (no candidate) |
| C. Commercial advertising | Promo craft | 35 Video Shotcraft (recipes) | 36 GSAP; 22 Impeccable | — | **Profile gap** |
| C. Educational explainers | Explain technical ideas visually | 44 Anatomy (DOMAIN) | 27 Diagram Design (ADAPT) | — | **Profile gap** |
| D. Electrical power systems, industrial automation | Calculation, diagrams | Existing engineering skills (short circuit, load flow, relay curves, motor starting) | 27 Diagram Design (ADAPT) | 02 (DEFER) | Standards (M2, PUIL) |
| D. Industrial utility (boiler, compressor, WTP, WWTP) | Engineering metrics, SCADA | Existing industrial-utility skills | 16 AG-UI (ZII interaction, reference) | — | **Profile gap** for WTP/WWTP |
| D. PLC and SCADA; instrumentation | Tag engineering, loops | Existing automation skills (plc, scada, modbus, instrument loop) | — | — | None |
| D. Industrial visualisation and technical documentation | Diagrams, HMI | 27 Diagram Design (ADAPT) | 24 Astryx (web HMI, DOMAIN) | 08 GitDiagram (REJECT) | ZII web HMI decision |
| E. Android games | Mobile performance | 43 (game guidance subset) | 17 (performance knowledge) | — | **Profile gap** |
| E. Browser games; 3D interactive environments | Rendering, controls | 43 Three.js Game Skills (ADAPT); threejs-* (existing) | 42 3Dviz (DEFER) | — | Profile gap (partly Silent Neon Tokyo game) |
| E. Survival and narrative-driven games | Systems and narrative | game-mechanics (existing) | 50 MuMuAINovel (knowledge, GPL) | — | Narrative continuity (C26) |
| E. Character consistency and realistic animation | Continuity; motion | 36 GSAP (motion); manhwa-production (existing) | 33 (voice) | — | Character continuity memory (C26) |
| F. XAUUSD ICT and SMC; market structure | Market analysis (research, paper) | xauusd-smc-analysis (existing) | 45 Claude Trading Skills (methodology, ADAPT) | 46, 48 (REJECT) | Data licence (M1) |
| F. Backtesting, risk, trading journal | Validation; journal | strategy-backtesting, trade-statistics, position-size-calculator (existing) | 47 Qlib (validation knowledge); 46 (validation methods, knowledge) | 06 (brokerage MCP), 46 (order tool) (REJECT) | Walk-forward and out-of-sample (C23) |
| F. Macroeconomic research | Macro context | — | 49 FinGPT (DEFER) | — | No candidate for macro data (licence needed) |
| G. Novel, manhwa, cinematic storytelling | Continuity, timeline, worldbuilding | novel-typesetting, manhwa-production (existing) | 50 MuMuAINovel (knowledge only) | — | Continuity memory (C26); M3 |
| H. Electrical education and research | Explainers, technical research | 44 Anatomy (DOMAIN); existing engineering skills | 27 Diagram Design | — | Standards (M2) |
| H. Japanese learning, JLPT | SRS, curriculum | fsrs-scheduler, srs-sm2-scheduler, jlpt-curriculum (existing) | 33 Voicebox (Japanese narration, DEFER) | — | Japanese narration (B3) |
| H. Data analysis and knowledge management | Analysis; personal knowledge | existing data skills (pdf, xlsx, markitdown) | 02 Graphify (DEFER); C04 memory (design) | — | Local memory standard (C04) |

## 3. Per-project shortlist

| Project | Shortlist (ADAPT, MERGE, DOMAIN, KNOWLEDGE) | Hold |
|---|---|---|
| AmiraVerse | 28 (store checklist, after licence); 22/23 (UI gates); UI/UX Pro Max Flutter data (via K1, if approved) | 33 (voice for Japanese, after benchmark) |
| Money App | 22/23; 28 (store checklist); privacy and data policy (C31) | Any finance API path |
| DEAMIRA | 04 (imported); 07 (approval concept) | 14 (REJECT) |
| ZII | 16 (protocol reference), 25 (dashboard reference), 27 (diagrams) | 24 (web HMI, only if approved); OT security remains a separate gap |
| ZY Skill Library | C04 (memory standard), C02 (approval gate), C31 (policy) | Any third-party memory daemon (03) |
| EarthStop | 36 (GSAP), 35 (recipe data), 37 (rubric) | 30 (telemetry), 29 (AGPL), 22 hooks |
| SISI GELAP TOKOH | claim_ledger (existing), 02 (if local and verified) | Any web scraping path |
| Sebelum Sepi Menjadi Rumah | Not evaluated (no brief) | — |
| Silent Neon Tokyo (game and manhwa) | 43 (game guidance); 36 (motion); 42 (DEFER) | 41, 32, 40 (REJECT or DEFER) |
| XAUUSD (paper only) | 45 (methodology), 47 (validation knowledge) | 46, 48, 06 (REJECT); 49 (DEFER) |
| JLPT | existing SRS and curriculum; 33 (after benchmark) | — |
| Teknik Elektro and Industrial Utility | 27 (diagrams), 44 (explainers), 13 (local AI, owner approval) | 02 (DEFER) |
| Novel and manhwa | 50 (knowledge only); continuity design (C26) | 37 as a rubric only after review |
| Film production (film-sinematik) | 35 (recipes), 36 (motion) | 29 (AGPL) |
| ClipACanvas | Existing render-link-builder; 26 (web guidance, if HTML outputs need it) | — |

## 4. Token relevance (estimates, not measured)

- Loading a single SKILL.md of ADAPT candidates is estimated at 1–5 k tokens each (based on byte sizes in the triage). Measured token use is not available in this package.
- The largest candidates by byte size in the ADAPT and DOMAIN sets are 45 (94 SKILL.md in repo) and 22 (27 SKILL.md). Only a subset should be adapted; loading all would conflict with the token economy rule.
