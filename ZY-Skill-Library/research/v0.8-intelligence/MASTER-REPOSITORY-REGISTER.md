# MASTER-REPOSITORY-REGISTER — ZY v0.8 Intelligence Audit

Status: RESEARCH PACKAGE. Static audit only. No implementation, no installation, no repository code executed.
Date: 2026-11-25. Repository HEAD before this package: `79cccccb` (research checkpoint). Frozen code baseline: `7039fed`. Previous frozen snapshot: `940368f`.

## 1. Method and evidence

- Identity: `git ls-remote` on every candidate URL (HEAD hash), then README, LICENSE and package metadata read from a shallow clone.
- Static triage: `--depth 1` clones into `/home/user/ext/research-cache/` (outside the repository). Counts of hooks, MCP configs, installers, network references, subprocess, credential-related and telemetry-related files were produced by read-only `grep`/`find`. Summary: `evidence/triage-summary.tsv` (52 rows).
- Deep read: LICENSE head, README essentials, external hosts referenced by code, pipe-to-shell lines, root lifecycle scripts, hook and MCP config heads. Read-only.
- Nothing was installed, built, run, or executed. Clones are not part of the repository.
- Counts are static indicators, not verdicts. A count of zero is not proof of absence.

## 2. Coverage

| Item | Result |
|---|---|
| Candidates reviewed (static) | 51 of 51 |
| Canonical identity resolved | 50 of 51 |
| IDENTITY UNRESOLVED | 1 (item 39, Blender Skills: two exact-name repositories, both audited) |
| Depth of review | 49 read in depth (41 before the 2026-11-26 audit, plus 25, 29, 31, 34, 38, 41, 50, 51); 2 with targeted checks (04, 32); 0 triage-only. See section 8 |
| Decision-basis note | Resolved 2026-11-26: item 38 is verified by code reading (section 8). Before that audit it rested on triage counts only |
| Identity notes | item 02: PyPI install name `graphifyy` differs from repo name; item 32: `Bujiazi/MotionClone` and `LPengYang/MotionClone` share HEAD `8b3d937f`; item 40: README credits `@anshuc`, LICENSE says "Anshu Chimala" |

## 3. Historical deduplication

Canonical identities, owner/repo, lowercased for comparison.

| Group | Count | Members (repo, reviewed or recorded commit) |
|---|---|---|
| A. Imported skill sources | 19 | anthropics/skills (e4bb5d9); obra/superpowers (22f0b46); haidrrrry/claude-remotion-skill (1dcbe5e); Liamrjohnston/remotion-motion-graphics-skill (b860c79); kajisho5/ffmpeg-skill (73436cb); alton47/threejs-skills (7b8e256); MIGO-OvO/plc-skill (82e5419); zakariaf/Flutter-Skills (e073e5e); supabase/agent-skills (c9be0e9); siegerts/skill-canvas-video (6419a14); acelera-agency/html-animation (8b88879); iart-ai/web-animation-skills (ed3a045); calesthio/generative-media-skills (8c85352); bianbianzhu/procedural-sfx (5eff10f); meiiie/structured-root-cause-research-skill (bf2b7ef); K-Dense-AI/scientific-agent-skills (c21d13b); KalarisLabs/research-agent-skills (a74b0db); evanclan/OpenJLPT (0d1d341, data); github/spec-kit (3df7575) |
| B. Dependency repositories | 8 | pymodbus-dev/pymodbus; e2nIEE/pandapower; CoolProp/CoolProp; ranaroussi/quantstats; microsoft/markitdown; joshyattridge/smartmoneyconcepts; cmusphinx/pocketsphinx; `fsrs` (PyPI; repository identity not recorded, UNRESOLVED) |
| C. Candidates not imported | 18 | obra/superpowers-skills (archived); langchain-ai/langgraph; microsoft/playwright; appium/appium; Power-Agent/PowerMCP (BLOCKED); Power-Agent/PowerSkills (license conflict); thiagoralves/OpenPLC_v3 (GPL-3.0); node-red/node-red; remotion-dev/skills (no LICENSE); motion-canvas/motion-canvas; mrdoob/three.js; ManimCommunity/manim; hexgrad/kokoro; docling-project/docling; yomidevs/yomitan; kernc/backtesting.py (AGPL-3.0); polakowo/vectorbt (Commons Clause); open-spaced-repetition/fsrs4anki |
| D. Historical, not in the sources list | 4 | Zacklinkk/svg-foundry-skill (no LICENSE); RandyHaylor/audio-and-vocal-mastering (no LICENSE); full-stack-skills/threejs-skills; full-stack-skills/flutter-skills |
| E. Added in v0.8 audits | 7 | google-labs-code/stitch-skills (75f4696); elementalsouls/Claude-BugHunter (6a2153d); firecrawl/firecrawl (98ae8c7); firecrawl/firecrawl-claude-plugin (d6e42a4); firecrawl/firecrawl-mcp-server (f5488e4); firecrawl/skills (1d4b072); nextlevelbuilder/ui-ux-pro-max-skill (bde080f) |
| **Historical canonical total** | **56** | Groups A–E |
| New candidate repositories | 52 | 51 candidates; item 39 counts as two repositories |
| Overlap with historical | 2 | obra/superpowers (item 04); kajisho5/ffmpeg-skill (item 31) |
| **Unique repositories after deduplication** | **106** | 56 + 52 − 2 |

Angka 32 dalam laporan terdahulu telah ditelusuri dan dikesampingkan sebagai jumlah historis. Rincian rekonsiliasi ada di bagian 3a.

## 3a. Rekonsiliasi angka 32, 56, dan 106

Metode: dihitung dari daftar identitas bagian 3 dan 52 identitas audit (`evidence/identity-ls-remote.tsv`). Pemeriksaan tumpang tindih dan subset dijalankan terhadap nama kanonik (owner/repo, huruf kecil). Angka 32 tidak dipakai sebagai jumlah historis.

| Angka | Nilai | Perhitungan | Status |
|---|---|---|---|
| Total historis (grup A–E) | 56 | A 19 + B 8 + C 18 + D 4 + E 7 | Inventaris aktual; sumber utama |
| Identitas historis tanpa repository | 1 | fsrs (PyPI); identitas repository tidak tercatat | Tidak diklaim sebagai repository terkonfirmasi |
| Repository audit v0.8 | 52 | 51 kandidat; item 39 dihitung sebagai dua repository (39a, 39b) | 52 dari 52 identitas cocok dengan HEAD klon |
| Tumpang tindih historis | 2 | obra/superpowers (04), kajisho5/ffmpeg-skill (31) | Diperiksa terhadap 56 identitas: tepat 2 |
| Entri unik setelah deduplikasi | 106 | 56 + 52 − 2 | Diterima sebagai inventaris sementara, dengan syarat di bawah |
| Tidak diklaim sebagai repository terkonfirmasi | 3 | fsrs (1) + 39a dan 39b (2) | Identitas kandidat belum terselesaikan |
| Repository unik terkonfirmasi | 103 | 106 − 3 | Dasar perencanaan |
| Angka 32 (laporan terdahulu) | 32 | 26 (daftar awal) + 6 (v0.8) pada register konsolidasi BACKLOG-V0.8.md baris 191 | Ditelusuri sebagai subset. Bukan jumlah historis; dikesampingkan |

Penelusuran angka 32 (diverifikasi terhadap daftar identitas): A 3 (anthropics/skills, obra/superpowers, github/spec-kit) + B 5 + C 18 + E 6 (stitch-skills, Claude-BugHunter, dan empat repository Firecrawl). Ke-32 repository itu berada di dalam 56. Setelah bagian I ditulis, UI/UX Pro Max ditambahkan ke tabel register konsolidasi, sehingga tabel tersebut berisi 33 baris.

Selisih 56 − 32 = 24:
- Grup A: 16 impor v0.2–v0.7 yang tidak tercantum di register konsolidasi.
- Grup B: 3 (smartmoneyconcepts, pocketsphinx, fsrs).
- Grup D: 4 (seluruh grup D).
- Grup E: 1 (nextlevelbuilder/ui-ux-pro-max-skill, ditambahkan setelah register konsolidasi ditulis).

Syarat penerimaan 106 (seluruhnya dipenuhi):
1. Identitas kanonik diperiksa: 52 dari 52 HEAD cocok; owner/repo dari URL klon cocok dengan nama direktori; tidak ada HEAD atau owner/repo yang berulang di antara 52 repository.
2. Alias dan fork identik dideduplikasi: LPengYang/MotionClone identik dengan Bujiazi/MotionClone (item 32) dan dihitung sekali.
3. Identitas belum terselesaikan tidak diklaim: fsrs dan item 39 dikeluarkan dari angka repository terkonfirmasi (103).
4. Dapat ditelusuri: tabel ini, bagian 3, dan `evidence/identity-ls-remote.tsv`.

Penjumlahan 32 + 51 = 83 tidak dipakai: angka 32 bukan total historis, dan penjumlahan itu mengabaikan deduplikasi.

## 4. Repository register

Decision vocabulary: ADOPT, ADAPT, MERGE, KNOWLEDGE ONLY, DOMAIN ONLY, DEFER, REJECT, BLOCKED. No candidate is adopted outright.
Commits are the 12-character prefix of the HEAD hash read by `git ls-remote` and confirmed on clone. Full hashes: `evidence/triage-summary.tsv`.

| ID | Candidate | Canonical repo @ commit | Identity | License (verified) | Verified capabilities (static) | Dependencies / install path | Final class | Decisive reason | Unresolved |
|---|---|---|---|---|---|---|---|---|---|
| 01 | ECC | affaan-m/ECC @4adeee6732a1 | Resolved | MIT | Agent harness; 1,089 SKILL.md; PreToolUse hooks run inline `node -e` on every Bash call; memory hooks; global git-hook installer | Node; ps1/npm installers | KNOWLEDGE ONLY (install REJECT) | Wholesale harness and per-call hook surface conflict with approval gates | Which concepts remain useful after review |
| 02 | Graphify | Graphify-Labs/graphify @02c27dc246cd | Repo resolved. README install name `graphifyy` (double y) differs from repo name | Apache-2.0 (+ MIT alternate) | Local tree-sitter code graph (claim); Cloud upsell; Gemini extension manifest; Python 3.11–3.14 with uv or pipx | uv/pipx; pipe-to-shell in README for uv | DEFER | Promising for a Flutter codebase map, but package identity, Dart support and local-only behaviour are unverified | Dart parser support; network calls on the local path; PyPI identity |
| 03 | claude-mem | thedotmack/claude-mem @11b47f9f4b8d | Resolved | Apache-2.0 (+ NOTICE) | Persistent memory with cloud sync to cmem.ai; remote MCP `cmem.ai/api/mcp`; OpenRouter calls; 35 hook files; installer runs a pipe-to-shell via execSync | Bun, uv, npx | REJECT | Default cloud sync and remote MCP violate deny-by-default; installer pipe | Local-only mode not evaluated |
| 04 | Superpowers | obra/superpowers @22f0b463e7a5 (= imported commit) | Resolved | MIT | 15 skills; 14 already in registry by name | None | MERGE (already imported) | Identical commit; 14 of 15 present | `diagnosing-superpowers` not imported (DEFER) |
| 05 | Open Code Review | alibaba/open-code-review @d4f568f71d3a | Resolved (open-codereview.ai) | Apache-2.0 | AI review CLI that sends changed code to a configured LLM (OpenAI/Anthropic endpoints in code); root postinstall script; pipe-to-shell in docs | npm postinstall; Go; LLM keys | DEFER | Code egress to paid LLM APIs; lifecycle script; benchmark not reproduced | Dart support claim; benchmark method |
| 06 | Cursor plugins | cursor/plugins @41e400932eca | Resolved (official Cursor marketplace) | NONE at root (no LICENSE) | Multi-plugin marketplace; 175 SKILL.md; stop and loop hooks, one with `loop_limit: null`; third-party MCPs including Interactive Brokers and QuickBooks; a skill doc suggests a pipe to `sudo sh` | Cursor or Claude plugin loaders | REJECT | No license means no reuse rights; brokerage MCP; unbounded hook loops | Per-plugin licenses (reference by URL only) |
| 07 | Plannotator | backnotprop/plannotator @9d77678f4db7 | Resolved | Apache-2.0 OR MIT | Local browser review UI for agent plans and diffs; 283 hook files with blocking timeouts up to 4 days; pipe-to-shell installer; hosted Inbox | bun; npm postinstall | KNOWLEDGE ONLY (tool REJECT) | Approval-gate concept is useful; the tool adds hooks, network and installer risk | None material |
| 08 | GitDiagram | ahmedkhaleel2004/gitdiagram @dae121cd2e52 | Resolved (gitdiagram.com) | MIT | Hosted diagram service; private repositories need a GitHub token; OpenAI calls; remote MCP `gitdiagram.com/mcp`; ad space in README | Hosted service | REJECT | Hosted egress for private repositories; remote MCP; advertising | Local-only variant not tested |
| 09 | REA | morluto/rea @a9d103167484 | Resolved (rea.tools; npm `rea-agents`) | MIT | "Reverse Engineer Anything" MCP for binaries and applications; `npx -y rea-agents@6.10.1 mcp` (pinned) | npx | REJECT | Dual-use reverse-engineering scope, outside the authorized defensive default | None |
| 10 | OmniRoute | cheaper-inference/OmniRoute @29a023c6b39f | Resolved (created by Diego Souza) | MIT | Gateway that pools third-party free tiers (≈1.62B tokens/month claim); MITM certificate installer (`src/mitm/cert/install.ts`); 12,794 credential-related files; npm postinstall | npm | REJECT | MITM and root-CA installation are prohibited; pooling risks provider-term violations | None |
| 11 | FreeLLMAPI | tashfeenahmed/freellmapi @7c9a38050814 | Resolved (freellmapi.co) | MIT | Aggregates free LLM tiers across 87 providers (claim); commercial "live" plan; pipe-to-shell installer in README | npm | REJECT | Pooling free tiers risks provider-term violations; pipe-to-shell installer | None |
| 12 | Awesome Free LLM APIs | mnfst/awesome-free-llm-apis @0838371416a4 | Resolved | CC0-1.0 (file named `license`) | Curated provider list; provider claims unverified | None | KNOWLEDGE ONLY | CC0 allows reference; provider data changes and must be verified per provider | Official verification per provider (not performed) |
| 13 | Ollama | ollama/ollama @784dd5442918 | Resolved (ollama.com) | MIT | Local model runtime; README pipe-to-shell for macOS; `cmd/launch/*` runs third-party install scripts | Go binary; optional GPU | DOMAIN ONLY | Local AI runtime fits the owner's needs; install only from a verified binary, no launch integrations | Owner-machine install status (not accessible); VRAM fit untested |
| 14 | OpenHands | OpenHands/OpenHands @ccdc5f51c359 | Resolved | MIT | Agent Canvas platform (local, cloud, self-hosted); 462 hook files; npm postinstall; Docker runtime | Docker; LLM keys | REJECT | Heavy autonomous platform with cloud dependency; overlaps Claude Code | None |
| 15 | Nod | n8n-io/nod @9333d3be8ee0 | Resolved (README "n8n presents Nod") | Apache-2.0 | Personal assistant that uses saved logins and website automation; vault for secrets; subscription sign-in option; MCP servers for Notion and Linear | Node; model keys | REJECT | Saved-login automation of websites and subscription sign-in are not acceptable | Ask-before-act pattern only |
| 16 | AG-UI | ag-ui-protocol/ag-ui @ed94ca4a3240 | Resolved (docs.ag-ui.com) | MIT | Event protocol spec 1.0 with JSON Schema; TypeScript, Python and .NET SDKs | pnpm (examples) | KNOWLEDGE ONLY | Stable reference; no current runtime need | ZII relevance not established |
| 17 | Chrome DevTools MCP | ChromeDevTools/chrome-devtools-mcp @8c43179464d3 | Resolved (Chrome team) | Apache-2.0 | Controls and inspects a live Chrome; accessibility and performance insights; plugin config pins `chrome-devtools-mcp@1.14.0` | npx (pinned) | MERGE (knowledge into webapp-testing) | MCP attaches to a live browser; webapp-testing uses an isolated headless profile | Whether a profile can carry logged-in sessions (not tested) |
| 18 | Agent Reach | Panniantong/agent-reach @8d9ecc1f5521 | Resolved | MIT | Login-based reading of social platforms (X, Reddit, Xiaohongshu, LinkedIn, Bilibili and others); cookie handling | uv | REJECT | Cookie and login-based access is prohibited by policy | None |
| 19 | Scrapling | D4Vinci/Scrapling @938867232230 | Resolved | BSD-3-Clause | Scraping framework with stealth browser and Cloudflare bypass features; MCP server metadata | Python | REJECT | Anti-bot bypass conflicts with policy; overlaps the rejected Firecrawl set | Parsing-only subset not evaluated |
| 20 | Last30Days | mvanhorn/last30days-skill @ed7ec6752b76 | Resolved | MIT | Multi-platform social research (X, Reddit, LinkedIn, TikTok, Polymarket); Stop hook runs Python every session; keychain setup scripts; Grok CLI install hint (pipe-to-shell) | Python | REJECT | Credential handling and scraping across platforms; hook on every session | Source-ranking methodology (not classified) |
| 21 | CLI-Anything | HKUDS/CLI-Anything @34f519533bc1 | Resolved | Apache-2.0 | Generates CLIs for arbitrary software; CLI-Hub installs third-party CLIs via pip; 151 SKILL.md; subprocess-heavy | Python | REJECT | Unnecessary; arbitrary application automation and supply-chain surface | None |
| 22 | Impeccable | pbakaus/impeccable @9e460a87ef33 | Resolved (impeccable.style) | Apache-2.0 (+ NOTICE.md) | Design critique and audit vocabulary (polish, bolder, critique, audit); 27 SKILL.md; hooks run local scripts on Write and SessionStart; `npx impeccable install` (unpinned); cloud API hosts | Node or Bun | ADAPT | Fills the missing visual QA gate (K7); keep the rules, drop hooks, npx and cloud | Rule-text fidelity; overlap diff against frontend-design |
| 23 | Hallmark | nutlope/hallmark @04977e15f3df | Resolved (usehallmark.com; "Made by Together AI") | MIT | Anti-AI-look gates in Floor and Reflex tiers; fifty themes; hook installers; LLM API hosts in code | Node | MERGE (into a design-quality rubric with item 22) | Overlaps Impeccable and taste-design; keep gate tiers only | Whether gates are machine-checkable |
| 24 | Astryx | meta/astryx @d7c7aa428652 | Resolved (Meta; MIT) | MIT | React 19 and StyleX design system; 150+ components; 419 MB; 191 hook files | pnpm; React | DOMAIN ONLY | Web and React only; not applicable to Flutter | Relevant only if a ZII web UI is approved |
| 25 | Shadcn Admin | satnaing/shadcn-admin @a156d9b90519 | Resolved | MIT | React and Vite admin dashboard reference | pnpm | DOMAIN ONLY | Architecture reference for web dashboards | None |
| 26 | Modern Web Guidance | GoogleChrome/modern-web-guidance-src @92686ac7d6eb | Resolved (source of npm `modern-web-guidance`; stewarded by Chrome, Edge, Firefox and MDN) | Apache-2.0 | Web-platform guidance skills; `npx modern-web-guidance@latest install`; postinstall TypeScript; cron installer script | npm | ADAPT | Authoritative guidance; adapt a pinned, offline subset without `@latest` or cron | Exact version to pin |
| 27 | Diagram Design | cathrynlavery/diagram-design @b228c5d77794 | Resolved (diagramdesign.dev) | MIT | Single-file HTML and SVG diagrams, 52 types; onboarding fetches a brand palette from a URL; Google Fonts link in output; maintainer scripts use subprocess | None at runtime | ADAPT | Strong for engineering documentation; remove the external font link and URL fetch | Runtime subprocess absent (only maintainer scripts call it) |
| 28 | App Store Compliance | mjmirza/app-store-compliance @7f7f0377620b | Resolved | OpenRoots Agent License 2.3 (LICENSE and NOTICE) | Release-rejection checklist for iOS and Android; scan installer | git, bash | KNOWLEDGE ONLY | Individual use permitted; AI training not granted; canonical legal text is external and unreviewed | Canonical legal text; NOTICE content |
| 29 | OpenMontage | OpenMontageInc/OpenMontage @2e003e65fa99 | Resolved | AGPL-3.0 | 141 SKILL.md; orchestrates many external APIs (327 credential-related files); 93 MB | Python; many APIs | REJECT | AGPL network copyleft; heavy external dependencies | None |
| 30 | HyperFrames | heygen-com/hyperframes @c7cb3eefd482 | Resolved (HeyGen) | Apache-2.0 | HTML to deterministic MP4 via headless Chrome and FFmpeg; 29 SKILL.md; 436 hook files; PostHog telemetry with embedded key and opt-out variable `HYPERFRAMES_NO_TELEMETRY`; hosted Studio upsell | Node 22+, FFmpeg, Chrome | DEFER | Telemetry on by default conflicts with deny-by-default; re-evaluate after telemetry removal | Default state confirmed by code reading only; render speed on GTX 1650 untested |
| 31 | FFmpeg Skill | kajisho5/ffmpeg-skill @31b47c263348 (imported at 73436cb) | Resolved | MIT | Upstream advanced since import; 19 SKILL.md; installer `bin/install.js` | Node; FFmpeg | MERGE (update review) | Already imported at recipe level; review the diff before any re-import | Diff against imported commit not yet compared |
| 32 | MotionClone | Bujiazi/MotionClone @8b3d937f005a (HEAD identical to LPengYang/MotionClone) | Resolved (official ICLR 2025 implementation per project page) | NONE (no LICENSE) | Training-free motion transfer for text-to-video diffusion; 17 model references; manual AnimateDiff and FreeControl downloads | conda; GPU | REJECT | No license means no reuse rights; GPU and model needs exceed a GTX 1650 with 4 GB VRAM | None (identity aliased) |
| 33 | Voicebox | jamiepine/voicebox @8dc2a5bfe0f7 | Resolved (voicebox.sh) | MIT | Local voice studio: TTS (LuxTTS about 1 GB VRAM; Kokoro 82M on CPU), STT (Whisper, Parakeet, Qwen3-ASR); 23 languages including Japanese; local MCP; model downloads | Python or Bun; PyTorch; model files | DEFER | Candidate to unblock narration (B1) and Japanese; needs hardware and language benchmark; voice-cloning consent policy | Indonesian not evidenced; engine-language table to confirm |
| 34 | VoiceStudio | debpalash/VoiceStudio @d9061408c204 | Resolved (repo) | AGPL-3.0 (+ LICENSE-NOTICE) | Desktop voice studio; 390 model references; 31 pipe-to-shell files; 227 telemetry-related files | Python or Bun; many installers | REJECT | AGPL copyleft; heavy installers; telemetry-related code | Owner identity beyond repo not needed for the decision |
| 35 | Video Shotcraft | louiseliu/hyperFrames-video-shotcraft @1df77f1ab080 | Resolved (repo) | Apache-2.0 | Agent skill: 157 shot recipe cards, 218 HTML compositions, camera and SFX recipes; no hooks, MCP or installers | Node (compositions) | ADAPT | Recipe data complements the cinematic skills; no runtime risk seen | Relation to the environment plugin `video-shotcraft` unverified; overlap diff against cinematic-* |
| 36 | GSAP Skills | greensock/gsap-skills @aed9cfd32777 | Resolved (GreenSock) | MIT | 8 SKILL.md on GSAP usage; no hooks, network or installers at root | None (content) | ADAPT | Clean, MIT, directly useful for HTML motion | Nested package.json lifecycle script not inspected (not executed) |
| 37 | Motionmaxxing | Tejashmakwana/motionmaxxing @8c8ec0f2a6f6 | Resolved | Apache-2.0 (+ NOTICE) | Motion-graphics rating rubric; product upsell (FinalMotion); `install.sh` | None | KNOWLEDGE ONLY | Rubric concepts are useful for K7; marketing-led and early release | `install.sh` not reviewed line by line |
| 38 | MCP for Blender | ahujasid/blender-mcp @a5a8acf2c6ae (formerly mcp-for-blender) | Resolved | MIT | MCP that lets an LLM execute Python inside Blender through a socket bridge; uvx; installers | Python 3.10+; Blender 3.0+ | REJECT | Arbitrary code execution path through MCP; unpinned uvx | None |
| 39 | Blender Skills | IDENTITY UNRESOLVED: EL4CTEO/blender-skills @1a1cc6c49312 and arjun988/blender-skills @904f095d8f36 | Two exact-name repositories | MIT (both) | EL4CTEO: 28 SKILL.md, no network references, 5 subprocess lines. arjun988: 188 SKILL.md (README says 94); Blender MCP via uvx in `.mcp.json` and `.cursor/mcp.json` | Blender; uvx (arjun988) | BLOCKED (identity) | Canonical repository cannot be chosen from evidence; arjun988 depends on MCP | Owner must confirm the intended repository; skill-count discrepancy |
| 40 | Dream Loop | achimala/dream-loop @9bddb901f7d0 | Resolved (README credits @anshuc; LICENSE "Anshu Chimala") | MIT | Closed loop: image target, then build, then critic; no iteration cap ("run until an exit criterion"); fal.ai image API | Image generation API | REJECT (as-is) | Unbounded loop; paid image API; screenshot egress | Bounded critic-loop design is a concept for K7 |
| 41 | ComfyUI | Comfy-Org/ComfyUI @a2103ae69d98 | Resolved | GPL-3.0 | Node-based local generation; 190 model references; custom nodes | Python; GPU | DEFER | GPL; GPU and custom-node risk; 4 GB VRAM constraint | Hardware test not performed |
| 42 | 3Dviz Pro Max | viettranx/3dviz-pro-max @d077e0e68915 | Resolved (3dviz.dev) | MIT | 3D visualization skill; GPU captures; references openstax, MIT and Creative Commons assets; 79 telemetry-related files | Node | DEFER | Telemetry code path unverified; asset licenses of referenced material unverified | Telemetry path; asset licenses |
| 43 | Three.js Game Skills | majidmanzarpour/threejs-game-skills @8286774b22a2 | Resolved | MIT | 9 SKILL.md; Vite and TypeScript scaffold; helper scripts reference Tripo3D and ElevenLabs APIs | Node | ADAPT | Game guidance subset; drop paid-API helpers | Overlap diff against imported alton47/threejs-skills |
| 44 | Anatomy | wheresryan22/anatomy @1482e8469b0a | Resolved (LICENSE "Ryan") | MIT | Interactive technical illustrations (SVG, WebGL, 3D); README install uses `npx skills add -g` (global) | Node | DOMAIN ONLY | Useful for electrical-engineering explainers; local copy only, no global install | Node version requirement differs between sources |
| 45 | Claude Trading Skills | tradermonty/claude-trading-skills @5de030b068d1 | Resolved | MIT | 94 SKILL.md; methodology for risk, journaling and review; FMP API (208 references); CME references; launchd installer; broker data references (Alpaca) in docs | Python; uv | ADAPT (methodology, paper-only) | Methodology is valuable; APIs, launchd and broker paths are excluded | Paid-API terms (FMP); order-placement code not found by pattern search |
| 46 | Vibe-Trading | HKUDS/Vibe-Trading @2134f408b1cd | Resolved | MIT | Research lab plus broker order tool (`trading_place_order`, label "Place broker order"); Robinhood and IBKR endpoints in code; OpenRouter and DeepSeek | Python; Node | REJECT | Live broker order path is prohibited | Validation methods (walk-forward, Monte Carlo) move to knowledge |
| 47 | Qlib | microsoft/qlib @543552324638 | Resolved | MIT | Quant research infrastructure; upcoming safe-by-default artifact loading (`trusted=True`); data from an Azure blob (Chinese markets) | Python | KNOWLEDGE ONLY | Methodology reference; Chinese-market data; not adopted | XAUUSD data coverage absent |
| 48 | TradingAgents | TauricResearch/TradingAgents @121265d18d46 | Resolved | Apache-2.0 | Multi-agent LLM trading research; requires Tauric or paid LLM keys; README pipe-to-shell installer | Node or npm | REJECT | Paid LLM dependency; pipe-to-shell installer; data egress | Role decomposition as a design reference |
| 49 | FinGPT | AI4Finance-Foundation/FinGPT @464916bdf91a | Resolved | MIT | Financial LLM project; 65 model references; sentiment over news sites | Python; GPU; Hugging Face models | DEFER | Heavy models; GPU; LLM APIs | Local sentiment feasibility not tested |
| 50 | MuMuAINovel | neosun100/MuMuAINovel @9a9f275993e1 | Resolved (README "MuMu") | GPL-3.0 | Novel-writing web app; MCP config; Postgres setup; 69 credential-related files; LLM keys | Python; Postgres | KNOWLEDGE ONLY | GPL means no code reuse; runtime needs keys and a database | Narrative-memory design only |
| 51 | Hacking-Tools | yogsec/Hacking-Tools @eac2233fc86b | Resolved | MIT | Curated list of penetration-testing tools (13 files) | None | REJECT | Offensive catalog; do not install; no defensive value needed | None |

## 5. Classification totals (51 candidates)

| Final class | Count | Items |
|---|---|---|
| ADOPT | 0 | — |
| ADAPT | 7 | 22, 26, 27, 35, 36, 43, 45 (methodology only) |
| MERGE | 4 | 04, 17, 23, 31 |
| KNOWLEDGE ONLY | 8 | 01, 07, 12, 16, 28, 37, 47, 50 |
| DOMAIN ONLY | 4 | 13, 24, 25, 44 |
| DEFER | 7 | 02, 05, 30, 33, 41, 42, 49 |
| REJECT | 20 | 03, 06, 08, 09, 10, 11, 14, 15, 18, 19, 20, 21, 29, 32, 34, 38, 40, 46, 48, 51 |
| BLOCKED | 1 | 39 (identity) |
| **Total** | **51** | |

## 6. Where the other required fields live

- Security, licence, data egress, cost, hardware: `SECURITY-LICENSE-MATRIX.md`
- Capability overlap and duplicate classes: `CAPABILITY-OVERLAP-MATRIX.md`
- Cross-agent compatibility: `CROSS-AGENT-COMPATIBILITY.md`
- Owner domain and project fit: `PROJECT-DOMAIN-MATRIX.md`
- Proposed integration details: `SELECTIVE-INTEGRATION-PROPOSAL.md`
- Benchmarks and rollback: `BENCHMARK-AND-ROLLBACK-PLAN.md`
- Static indicators per repository: `evidence/triage-summary.tsv`

## 7. Pemisahan keputusan runtime dan adaptasi pengetahuan

Aturan:
1. Keputusan runtime (instalasi, hook, MCP, layanan, jaringan, daemon, jalur broker, dan eksekusi kode upstream) diputuskan terpisah dari adaptasi pengetahuan (konsep, metode, dan teks yang ditulis ulang sendiri).
2. Penolakan runtime tidak otomatis menolak adaptasi pengetahuan. Pengetahuan yang diadaptasi juga tidak membawa runtime ke dalam library.
3. Lisensi menentukan cara adaptasi. Kebijakan proyek (DENY BY DEFAULT, Rp0, larangan MITM, pooling kuota, cookie atau login, bypass, broker, dan konten ofensif) berlaku untuk pengetahuan juga, terlepas dari lisensi.
4. Tidak ada adaptasi yang dieksekusi. Setiap adaptasi memerlukan persetujuan per ID (SELECTIVE bagian 2).

Legenda status pengetahuan:
- DIIZINKAN: lisensi permisif (MIT, Apache-2.0, BSD-3-Clause, CC0). Penulisan ulang atau adaptasi dengan atribusi dan pencatatan commit upstream.
- BATAS: copyleft (GPL-3.0, AGPL-3.0). Hanya konsep yang ditulis ulang sendiri; tanpa menyalin teks atau kode; keputusan pemilik diperlukan.
- TERTUNDA: lisensi belum pasti (teks kanonik belum ditinjau).
- TIDAK DIIZINKAN: tanpa lisensi; tidak ada hak pakai ulang.
- DIBLOKIR KEBIJAKAN: isi bertentangan dengan kebijakan proyek, terlepas dari lisensi.
- TIDAK DIUSULKAN: diizinkan lisensi, tetapi tidak ada kebutuhan atau ruang lingkupnya tidak sesuai.

Kelas runtime mengikuti bagian 5. Item 39 dipecah menjadi 39a dan 39b. Status TERTUNDA untuk 02, 05, 28, dan 30 menunggu pemeriksaan lanjutan.

| ID | Kandidat | Lisensi | Runtime (kelas) | Pengetahuan | Syarat dan alasan |
|---|---|---|---|---|---|
| 01 | ECC | MIT | KNOWLEDGE ONLY (instalasi REJECT) | DIIZINKAN | Konsep ditulis ulang; hook per panggilan Bash tidak dibawa |
| 02 | Graphify | Apache-2.0 (+MIT) | DEFER | TERTUNDA | Identitas paket, dukungan Dart, dan jaringan jalur lokal belum diverifikasi |
| 03 | claude-mem | Apache-2.0 | REJECT | DIIZINKAN untuk konsep memori lokal | Sinkronisasi cloud dan MCP jarak jauh ditolak; desain memori lokal ditulis mandiri (P12) |
| 04 | Superpowers | MIT | MERGE (sudah diimpor) | DIIZINKAN | 14 dari 15 skill sudah diimpor; `diagnosing-superpowers` DEFER |
| 05 | Open Code Review | Apache-2.0 | DEFER | TERTUNDA | Runtime mengirim kode ke LLM berbayar; egress belum diverifikasi |
| 06 | cursor/plugins | TIDAK ADA | REJECT | TIDAK DIIZINKAN | Tanpa lisensi; referensi URL saja |
| 07 | Plannotator | Apache-2.0 OR MIT | KNOWLEDGE ONLY (alat REJECT) | DIIZINKAN | Konsep gerbang persetujuan; alat dengan hook dan installer ditolak |
| 08 | GitDiagram | MIT | REJECT | TIDAK DIUSULKAN | Layanan hosted, MCP jarak jauh, dan iklan |
| 09 | REA (morluto) | MIT | REJECT | TIDAK DIUSULKAN | Ruang lingkup dual-use di luar default defensif |
| 10 | OmniRoute | MIT | REJECT | DIBLOKIR KEBIJAKAN | Pooling kuota gratis lintas penyedia dan MITM |
| 11 | FreeLLMAPI | MIT | REJECT | DIBLOKIR KEBIJAKAN | Pooling kuota gratis lintas penyedia |
| 12 | Awesome Free LLM APIs | CC0-1.0 | KNOWLEDGE ONLY | DIIZINKAN sebagai referensi | Data penyedia berubah; verifikasi per penyedia |
| 13 | Ollama | MIT | DOMAIN ONLY | DIIZINKAN (adaptasi tidak diperlukan) | Instalasi dan unduhan model memerlukan persetujuan |
| 14 | OpenHands | MIT | REJECT | TIDAK DIUSULKAN | Platform berat dengan ketergantungan cloud |
| 15 | Nod | Apache-2.0 | REJECT | DIBLOKIR KEBIJAKAN untuk login tersimpan dan otomasi situs; pola "tanya sebelum bertindak" DIIZINKAN | Pisahkan konsep dari fitur login |
| 16 | AG-UI | MIT | KNOWLEDGE ONLY | DIIZINKAN sebagai referensi protokol | Tidak ada kebutuhan runtime saat ini |
| 17 | Chrome DevTools MCP | Apache-2.0 | MERGE (ke webapp-testing) | DIIZINKAN | Tanpa MCP dan tanpa profil browser berisi sesi login (P15) |
| 18 | Agent Reach | MIT | REJECT | DIBLOKIR KEBIJAKAN | Akses berbasis cookie dan login |
| 19 | Scrapling | BSD-3-Clause | REJECT | DIBLOKIR KEBIJAKAN untuk bypass anti-bot | Subset parsing belum dievaluasi |
| 20 | Last30Days | MIT | REJECT | DIIZINKAN untuk metodologi peringkat sumber (belum diklasifikasi); DIBLOKIR KEBIJAKAN untuk scraping dan kredensial | Metodologi ditulis ulang sendiri |
| 21 | CLI-Anything | Apache-2.0 | REJECT | TIDAK DIUSULKAN | Tidak diperlukan; permukaan rantai pasok luas |
| 22 | Impeccable | Apache-2.0 | ADAPT | DIIZINKAN dengan NOTICE dan atribusi | Hanya aturan; hook, npx, dan cloud dibuang (P01) |
| 23 | Hallmark | MIT | MERGE | DIIZINKAN | Gerbang Floor dan Reflex saja (P01) |
| 24 | Astryx | MIT | DOMAIN ONLY | DIIZINKAN sebagai referensi | Web dan React; tidak untuk Flutter |
| 25 | Shadcn Admin | MIT | DOMAIN ONLY | DIIZINKAN sebagai referensi arsitektur | Dashboard web; tidak untuk Flutter |
| 26 | Modern Web Guidance | Apache-2.0 | ADAPT | DIIZINKAN dengan atribusi | Tanpa `@latest` dan tanpa cron (P03) |
| 27 | Diagram Design | MIT | ADAPT | DIIZINKAN | Tautan font eksternal dihapus (P04) |
| 28 | App Store Compliance | OpenRoots ORA 2.3 | KNOWLEDGE ONLY | TERTUNDA | Individu boleh; pelatihan AI tidak diberikan; teks kanonik belum ditinjau |
| 29 | OpenMontage | AGPL-3.0 | REJECT | BATAS | Konsep saja; tanpa teks dan kode |
| 30 | HyperFrames | Apache-2.0 | DEFER | DIIZINKAN setelah telemetri dinonaktifkan dan diuji | Telemetri aktif secara default menurut pembacaan kode; perlu verifikasi lanjutan |
| 31 | FFmpeg Skill | MIT | MERGE (tinjau pembaruan) | DIIZINKAN | Diff terhadap versi impor (73436cb) belum dibandingkan (P16) |
| 32 | MotionClone | TIDAK ADA | REJECT | TIDAK DIIZINKAN | Tanpa lisensi; alias LPengYang memiliki HEAD yang sama |
| 33 | Voicebox | MIT | DEFER | DIIZINKAN | Benchmark bahasa dan hardware belum dijalankan (D2) |
| 34 | VoiceStudio | AGPL-3.0 | REJECT | BATAS | Installer pipe-to-shell, telemetri, dan copyleft |
| 35 | Video Shotcraft | Apache-2.0 | ADAPT (data resep) | DIIZINKAN dengan atribusi | Tanpa komposisi HyperFrames (P06) |
| 36 | GSAP Skills | MIT | ADAPT | DIIZINKAN | Tanpa paket GSAP dalam library (P05) |
| 37 | Motionmaxxing | Apache-2.0 | KNOWLEDGE ONLY | DIIZINKAN untuk konsep rubrik | `install.sh` belum ditinjau baris demi baris |
| 38 | MCP for Blender | MIT | REJECT | DIIZINKAN secara lisensi; runtime ditolak | Dasar penolakan (eksekusi Python lewat MCP) belum diverifikasi pada kodenya |
| 39a | Blender Skills (EL4CTEO) | MIT | BLOCKED (identitas kandidat) | Belum ditentukan | Lihat keputusan item 39 |
| 39b | Blender Skills (arjun988) | MIT | BLOCKED (identitas kandidat) | Belum ditentukan | Bergantung pada MCP `uvx` |
| 40 | Dream Loop | MIT | REJECT (sebagaimana adanya) | DIIZINKAN untuk konsep iterasi terbatas | Tanpa loop tanpa batas dan tanpa API berbayar; konsep untuk K7 |
| 41 | ComfyUI | GPL-3.0 | DEFER | BATAS | Hardware 4 GB; custom nodes |
| 42 | 3Dviz Pro Max | MIT | DEFER | DIIZINKAN; lisensi aset rujukan belum diverifikasi | Jalur telemetri belum diverifikasi |
| 43 | Three.js Game Skills | MIT | ADAPT (subset) | DIIZINKAN | Tanpa helper Tripo3D dan ElevenLabs (P07) |
| 44 | Anatomy | MIT | DOMAIN ONLY | DIIZINKAN sebagai referensi | Instalasi global (`-g`) ditolak |
| 45 | Claude Trading Skills | MIT | ADAPT (metodologi, paper-only) | DIIZINKAN | API, launchd, dan jalur broker dikecualikan (P08) |
| 46 | Vibe-Trading | MIT | REJECT | DIIZINKAN untuk metode validasi (P14); DIBLOKIR KEBIJAKAN untuk jalur order broker | Metode ditulis ulang tanpa kode |
| 47 | Qlib | MIT | KNOWLEDGE ONLY | DIIZINKAN sebagai referensi metodologi | Data pasar Tiongkok tidak dipakai |
| 48 | TradingAgents | Apache-2.0 | REJECT | DIIZINKAN untuk pembagian peran sebagai konsep | Dependensi LLM berbayar; installer pipe-to-shell |
| 49 | FinGPT | MIT | DEFER | DIIZINKAN | Model berat dan GPU |
| 50 | MuMuAINovel | GPL-3.0 | KNOWLEDGE ONLY | BATAS | Konsep memori naratif ditulis ulang sendiri |
| 51 | Hacking-Tools | MIT | REJECT | TIDAK DIUSULKAN | Katalog ofensif; tidak ada nilai defensif yang dibutuhkan |

## 8. Pembaruan audit mendalam (2026-11-26; pasca-checkpoint, belum di-commit)

Delapan kandidat yang sebelumnya hanya triage (25, 29, 31, 34, 38, 41, 50, 51) kini dibaca mendalam. Bukti ada di `evidence/deep-audit-2026-11-26.md` (commit, path, dan baris). Kelas tidak berubah kecuali item 31, yang ditutup.

| ID | Kelas sebelumnya | Kelas sekarang | Perubahan | Bukti |
|---|---|---|---|---|
| 02 | DEFER | DEFER | Dart terbukti di kode. Identitas dalam repositori konsisten (`graphifyy`). Jaringan pada jalur lokal dan kepemilikan PyPI belum terbukti | Deep audit bagian 2 |
| 05 | DEFER | DEFER | Egress hanya ke endpoint yang dikonfigurasi. Telemetri default OFF. Dart tidak terbukti | Deep audit bagian 2 |
| 25 | DOMAIN ONLY | DOMAIN ONLY | Tidak ada skrip lifecycle atau hook. Tidak berubah | Deep audit bagian 1 |
| 28 | KNOWLEDGE ONLY | KNOWLEDGE ONLY (TERTUNDA) | Teks kanonik OpenRoots tidak dapat diambil karena DNS diblokir. Adaptasi tertunda | Deep audit bagian 2 |
| 29 | REJECT | REJECT | API HeyGen berbayar. AGPL. Pengetahuan hanya BATAS | Deep audit bagian 1 |
| 30 | DEFER | DEFER | Telemetri aktif secara default (opt-out), menurut dokumentasi repositori | Deep audit bagian 2 |
| 31 | MERGE (tinjau pembaruan) | MERGE (DITUTUP) | Salinan impor identik dengan upstream. Tidak perlu impor ulang | Deep audit bagian 1 |
| 33 | DEFER | DEFER | Jepang terbukti di kode. Indonesia tidak terbukti | Deep audit bagian 2 |
| 34 | REJECT | REJECT | Telemetri default OFF. Jepang terbukti di kode. Indonesia tidak terbukti | Deep audit bagian 1 |
| 38 | REJECT | REJECT | Dasar terbukti di kode: `exec` tanpa batas secara default; installer `@latest`. Default telemetri belum ditentukan | Deep audit bagian 1 |
| 39 | BLOCKED | BLOCKED | Perbandingan selesai. Rekomendasi: 39a selektif. Kanonik menunggu pemilik | `BLENDER-SKILLS-COMPARISON.md` |
| 41 | DEFER | DEFER | Klaim vendor 4 GB VRAM dan 8 GB RAM belum diuji | Deep audit bagian 1 |
| 45 | ADAPT (metodologi) | ADAPT (metodologi) | Tidak ditemukan pengiriman order pada pola yang diperiksa. Referensi MCP Alpaca hanya dokumen | Deep audit bagian 2 |
| 50 | KNOWLEDGE ONLY | KNOWLEDGE ONLY | `mcp_config.json` ada (runtime REJECT). Pola literal kredensial tidak ditemukan | Deep audit bagian 1 |
| 51 | REJECT | REJECT | Katalog ofensif; 13 berkas tanpa skrip | Deep audit bagian 1 |

Cakupan setelah pembaruan: 49 dibaca mendalam (41 sebelumnya ditambah 8), 2 pemeriksaan terarah (04, 32), dan 0 hanya triage. Jumlah kandidat tetap 51.
