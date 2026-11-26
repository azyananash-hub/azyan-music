# SECURITY-LICENSE-MATRIX — ZY v0.8 Intelligence Audit

Basis: static triage counts (`evidence/triage-summary.tsv`) and deep reads of LICENSE, README, hook and MCP configs, external hosts referenced by code, and pipe-to-shell lines. Counts are indicators. "refs" means occurrences in code or docs. Nothing was executed.

Gates applied (mandatory, not weighted): security and privacy, licence clarity, Rp0 budget, deny-by-default data egress, no broker credential access, no offensive tooling, no provider-restriction circumvention, no MITM.

## 1. Matrix

| ID and candidate | Licence | Hooks / MCP | Install-path risk | Observed external hosts (refs) | Credential-related files | Telemetry-related files | Cost status | Hardware (GTX 1650 4 GB, 16 GB RAM; estimates marked) | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 01 ECC | MIT | 208 hook files; PreToolUse runs inline `node -e` on every Bash call; `.mcp.json` | ps1 and npm installers; global git-hook installer | ecc.tools (17); v3.fal.media (15); api.github.com (14) | 709 | 187 | Rp0 locally; API keys vary | Light | Concepts only; no install |
| 02 Graphify | Apache-2.0 (+MIT) | Gemini extension manifest; no MCP | uv or pipx; pipe-to-shell in README for uv | Local claim; Cloud upsell; localhost refs only in deep read | 168 | 43 | Rp0 local; Cloud paid | Light (CPU) | DEFER: verify local path, package identity |
| 03 claude-mem | Apache-2.0 (+NOTICE) | 35 hook files; 4 MCP configs including remote `cmem.ai/api/mcp` | execSync pipe-to-shell (bun, uv) inside installer | cmem.ai (313); sync.cmem.ai (55); openrouter.ai (124) | 1,158 | 341 | Cloud subscription | Medium | REJECT: cloud sync, remote MCP, installer pipe |
| 04 Superpowers | MIT | 6 hook files; none | none | none significant | 22 | 9 | Rp0 | Light | MERGE (already imported) |
| 05 Open Code Review | Apache-2.0 | 7 hook files; plugin manifests | npm postinstall `scripts/install.js`; pipe-to-shell in docs | api.openai.com (54); api.anthropic.com (42) | 265 | 121 | Paid LLM API | Medium | DEFER: code egress to LLMs; lifecycle script |
| 06 Cursor plugins | NONE at root | 11 hook files; 6 third-party MCP configs incl. Interactive Brokers and QuickBooks | skill doc suggests `curl … \| sudo sh` | mcp-e2e.quickbooks.intuit.com and other brokerage/finance endpoints | 159 | 51 | Varies | Light | REJECT: no licence; brokerage MCP; unbounded loops |
| 07 Plannotator | Apache-2.0 OR MIT | 283 hook files; blocking timeouts up to 345,600 s | pipe-to-shell installer; postinstall (bun) | plannotator.ai (142); linear.app (81); gitlab (203); bitbucket (93) | 645 | 78 | Hosted Inbox | Medium | KNOWLEDGE ONLY: concept only |
| 08 GitDiagram | MIT | 23 hook files; remote MCP `gitdiagram.com/mcp` | prepare script sets git hooksPath | gitdiagram.com (308); api.github.com (21); api.openai.com (12) | 115 | 84 | Hosted; ads | Light | REJECT: private-repo egress; remote MCP |
| 09 REA | MIT | MCP `npx -y rea-agents@6.10.1 mcp` (pinned) | npx; pipe-to-shell examples on website | rea.tools (website, docs) | 386 | 60 | Rp0 | Medium | REJECT: dual-use scope |
| 10 OmniRoute | MIT | 79 hook-related files | postinstall; MITM certificate installer `src/mitm/cert/install.ts`; pipe-to-shell in scripts | api.openai.com (239); provider APIs pooled | 12,794 | 2,451 | Free-tier pooling | Heavy (970 MB) | REJECT: MITM, root CA, provider circumvention |
| 11 FreeLLMAPI | MIT | 5 hook files; no MCP | docs install.sh and install.ps1; `curl … \| bash` in README | api.groq.com (22); relay hosts (examples) | 645 | 181 | Paid "live" plan | Medium | REJECT: provider-terms risk; pipe installer |
| 12 Awesome Free LLM APIs | CC0-1.0 | None | None | Reference links only | 9 | 0 | Rp0 | None | KNOWLEDGE ONLY |
| 13 Ollama | MIT | 14 hook-related files; no MCP | `scripts/install.sh` and `.ps1`; README pipe-to-shell (macOS); `cmd/launch/*` runs other tools' install scripts | ollama.com (124); model downloads | 72 | 19 | Rp0 local; cloud models paid | GPU optional; 7–8B Q4 roughly 5–6 GB RAM (estimate) | DOMAIN ONLY (owner approval; verified binary only) |
| 14 OpenHands | MIT | 462 hook files; AGENTS.md | postinstall `node -e`; `.openhands/setup.sh` | app.all-hands.dev (254); dev.azure.com (28) | 659 | 185 | LLM keys; cloud | Heavy (Docker) | REJECT |
| 15 Nod | Apache-2.0 | MCP to Notion, Linear, qontext (remote) | self-host `setup.sh`; n8n `install.ps1` | api.openai.com (29); remote MCP hosts | 300 | 165 | Monthly limit on API models; subscription sign-in | Medium | REJECT: saved logins; website automation |
| 16 AG-UI | MIT | `.mcp.json` (repo dev config, npx) | npx in dev config; pnpm | a2ui.org (172); docs.ag-ui.com (75) | 387 | 159 | Rp0 | Light | KNOWLEDGE ONLY |
| 17 Chrome DevTools MCP | Apache-2.0 | `mcp.json` pins `chrome-devtools-mcp@1.14.0` | npx (pinned) | developer.chrome.com (96); web.dev (24) | 49 | 39 | Rp0 | Light | MERGE (knowledge only; no live-profile MCP) |
| 18 Agent Reach | MIT | None | uv; pipe-to-shell in docs | xueqiu (21); v2ex (18); reddit (13); linkedin (10); xiaohongshu (9) | 50 | 2 | Rp0 plus cookies | Light | REJECT: cookie and login access |
| 19 Scrapling | BSD-3-Clause | MCP metadata | none | Stealth proxies; anti-bot bypass features | 207 | 12 | Rp0 | Light | REJECT: bypass features |
| 20 Last30Days | MIT | Stop hook runs Python every session | keychain setup scripts; Grok CLI `curl … \| bash` hint | x.com (392); reddit.com (356); linkedin (104); tiktok (74); polymarket (69) | 291 | 27 | X or Grok subscriptions | Light | REJECT: credentials and multi-platform scraping |
| 21 CLI-Anything | Apache-2.0 | No hooks; setup.py per harness | CLI-Hub pip installs; pipe-to-shell in docs | mailchimp (59); zoom (12); iterm2 installer | 181 | 38 | Varies | Medium | REJECT: unnecessary; arbitrary automation |
| 22 Impeccable | Apache-2.0 (+NOTICE.md) | 8 hook files (postToolUse on Write; SessionStart runs local script) | `npx impeccable install` (unpinned) | impeccable.style (42); api.impeccable.style (22); app.impeccable.style (20) | 243 | 220 (non-test code: no analytics SDK found) | Rp0 local; cloud app | Light | ADAPT: rules only; drop hooks, npx, cloud |
| 23 Hallmark | MIT | None; hook installers `install-hook.mjs`, `install.mjs` | Node scripts that install hooks | LLM API hosts in code (together.xyz, anthropic, z.ai, moonshot) | 14 | 8 | LLM keys | Light | MERGE: gates only; drop installers |
| 24 Astryx | MIT | 191 hook files; lifecycle `prepare` runs husky | pnpm; husky | fonts.googleapis.com (45); placeholder image service (90) | 103 | 209 (review) | Rp0 | Heavy (419 MB) | DOMAIN ONLY (web only) |
| 25 Shadcn Admin | MIT | 4 hook-related files (React hooks) | pnpm | None | 30 | 5 | Rp0 | Light | DOMAIN ONLY |
| 26 Modern Web Guidance | Apache-2.0 | Postinstall TypeScript; cron installer `setup-cron.sh` | `npx modern-web-guidance@latest install`; cron | developer.chrome.com (26); webstatus.dev (23); chromestatus.com (10) | 178 | 143 | Rp0 | Light | ADAPT: pinned offline subset; no `@latest`; no cron |
| 27 Diagram Design | MIT | None | None | fonts.googleapis.com (11) in generated output | 4 | 31 | Rp0 | Light | ADAPT: strip external font link and URL fetch |
| 28 App Store Compliance | OpenRoots ORA 2.3 (non-OSI) | 2 hook files | `install.sh`; `install_harness.py` | developer.apple.com (24); developer.android.com (23) | 20 | 26 | Individual use free; AI training not granted | Light | KNOWLEDGE ONLY: licence text external |
| 29 OpenMontage | AGPL-3.0 | None | `setup.py`; test-corpus `setup.sh` | Many external APIs | 327 | 90 | Paid APIs by design | Heavy (93 MB; 43 model refs) | REJECT: AGPL network copyleft |
| 30 HyperFrames | Apache-2.0 | 436 hook files | Browser install in CLI; `lefthook` | cdn.jsdelivr.net (189); fonts.googleapis.com (101); PostHog telemetry module | 197 | 796 (PostHog) | Studio paid plans | Medium (Chrome, FFmpeg) | DEFER: telemetry on by default |
| 31 FFmpeg Skill | MIT | 1 hook file | `bin/install.js` | None significant (12 net lines) | 3 | 10 | Rp0 | Light | MERGE (update review) |
| 32 MotionClone | NONE | None | conda; manual model downloads | Hugging Face model references | 0 | 0 | Rp0 | GPU heavy; 17 model refs | REJECT: no licence; GPU |
| 33 Voicebox | MIT | 23 hook-related files; local MCP `127.0.0.1:17493` | No installers; bun | huggingface.co (4); download.pytorch.org (5); repo.radeon.com (10) | 26 | 2 | Rp0 | Medium: LuxTTS about 1 GB VRAM; Kokoro on CPU | DEFER: benchmark; consent policy |
| 34 VoiceStudio | AGPL-3.0 | 48 hook files; MCP docs | 31 pipe-to-shell files; many installers | 1,173 net lines; 390 model refs | 353 | 227 | Rp0 | Heavy | REJECT: AGPL; installers; telemetry |
| 35 Video Shotcraft | Apache-2.0 | None | None | Minimal | 0 | 11 | Rp0 | Light | ADAPT (recipe data) |
| 36 GSAP Skills | MIT | None at root | None | cdn.jsdelivr.net (2, examples) | 0 | 0 | Rp0 | Light | ADAPT (content only) |
| 37 Motionmaxxing | Apache-2.0 (+NOTICE) | None | `install.sh` (not reviewed line by line) | Wikipedia and Microsoft docs (references); my-cnd-server.com (4) | 8 | 2 | FinalMotion upsell | Light | KNOWLEDGE ONLY |
| 38 MCP for Blender | MIT | MCP configs (`.mcp.json`) | install.ps1, install.sh, setup_cli.py; uvx | localhost sockets | 12 | 19 | Rp0 | Light | REJECT: arbitrary code execution path |
| 39a EL4CTEO blender-skills | MIT | Plugin manifest only | `install/install.sh` and `.ps1` (not executed) | None | 0 | 1 | Rp0 | Light | Identity unresolved (see 39) |
| 39b arjun988 blender-skills | MIT | MCP via uvx (`.mcp.json`, `.cursor/mcp.json`) | uvx unpinned | github.com; astral.sh (docs) | 1 | 7 | Rp0 | Light | REJECT: MCP-dependent |
| 40 Dream Loop | MIT | None | None | queue.fal.run (12): paid image API | 2 | 0 | Paid image API | Light | REJECT: unbounded loop; egress |
| 41 ComfyUI | GPL-3.0 | None | `utils/install_util.py` | 190 model refs | 74 | 15 | Rp0 local | GPU heavy; custom nodes | DEFER |
| 42 3Dviz Pro Max | MIT | 3 hook files | None | openstax.org (14); MIT OCW; Creative Commons | 0 | 79 | Rp0 | GPU captures | DEFER: telemetry path; asset licences |
| 43 Three.js Game Skills | MIT | None | `install.sh` (not reviewed) | api.tripo3d.ai (2); api.elevenlabs.io (1) | 10 | 1 | Paid APIs in helper scripts | Light | ADAPT: drop paid-API helpers |
| 44 Anatomy | MIT | None | `npx skills add -g` (global install) | w3.org (references) | 2 | 6 | Rp0 | Light | DOMAIN ONLY: local copy only |
| 45 Claude Trading Skills | MIT | 4 hook files; launchd installer | `scripts/install_launchd.py` (persistent jobs) | financialmodelingprep.com (208); cmegroup.com (21) | 410 | 19 | FMP paid tiers | Light | ADAPT: methodology only; paper-only |
| 46 Vibe-Trading | MIT | 11 hook files | None | agent.robinhood.com (35); api.ibkr.com (32); api.deepseek.com (29); openrouter.ai (26) | 317 | 40 | Broker and LLM costs | Heavy (115 MB) | REJECT: live broker order path |
| 47 Qlib | MIT | None | `setup.py` | qlibpublic blob storage (4); csindex.com.cn (5) | 4 | 2 | Rp0 | Medium | KNOWLEDGE ONLY |
| 48 TradingAgents | Apache-2.0 | None | Pipe-to-shell `install.sh` | tauric.ai (7); api.tauric.ai (2); openrouter.ai (2); platform.openai.com (1) | 22 | 0 | Paid LLM keys | Light | REJECT: paid LLM; pipe installer |
| 49 FinGPT | MIT | None | `setup.py` | huggingface.co (3); minimaxi (3) | 68 | 16 | GPU and LLM costs | Heavy (65 model refs) | DEFER |
| 50 MuMuAINovel | GPL-3.0 | MCP config | `setup_postgres.py` | 128 net lines; LLM keys | 69 | 1 | LLM keys | Medium | KNOWLEDGE ONLY: no code reuse |
| 51 Hacking-Tools | MIT | None | None | None | 1 | 1 | Rp0 | None | REJECT: offensive catalog |

## 2. Cross-repository security findings

| Finding | Repositories | Policy consequence |
|---|---|---|
| Pipe-to-shell installers in README or code | 01 (docs), 02, 03, 05, 07, 10, 11, 13, 14, 16, 18, 20, 21, 22 (cloud), 26, 48 | Never execute. Install only from verified binaries or pinned packages, and only after owner approval |
| Unpinned `npx` or `uvx` (`@latest`, or no version) | 03, 08, 22, 26, 38, 39b | Never run unpinned. Pin exact version and review before any use |
| Remote MCP servers | 03 (cmem.ai), 08 (gitdiagram.com), 15 (Notion, Linear), 06 (brokerage) | Reject remote MCP: data leaves the machine by design |
| Hooks executing code on every tool call or session | 01, 03, 07, 14, 22, 30, 46, 20 | No hooks adopted. Governance is handled by explicit procedures, not hooks |
| MITM or root-CA installation | 10 | Prohibited |
| Provider free-tier pooling | 10, 11 | Prohibited (provider-restriction circumvention) |
| Broker or order paths | 06, 45 (Alpaca in docs), 46 | Prohibited for live trading. Research and paper only |
| Credential and cookie access to logged-in services | 18, 20, 15 | Prohibited |
| Telemetry SDK or endpoint by default | 30 (PostHog) | Must be removed before any adoption |
| Dual-use reverse engineering | 09 | Out of scope |
| Offensive tooling catalogue | 51 | Do not install; no enablement |

## 3. Licence summary

| Class | Items |
|---|---|
| Permissive (MIT, Apache-2.0, BSD-3, CC0) with clear text | Most candidates; attribution and NOTICE obligations apply where present (03, 07, 17, 22, 26, 37) |
| Copyleft | GPL-3.0: 41, 50. AGPL-3.0: 29, 34. No code reuse; reference only |
| No licence | 06 (cursor/plugins), 32 (MotionClone). No reuse rights |
| Non-OSI custom licence | 28 (OpenRoots ORA 2.3): individual use permitted; AI training not granted; canonical legal text external and unreviewed |
| Mixed | 07 (Apache-2.0 OR MIT), 22 (Apache-2.0 with NOTICE.md), 12 (CC0 with file named `license`) |

## 4. Unresolved security questions (blockers to any adoption)

1. 30 HyperFrames: confirm telemetry is removable without breaking rendering.
2. 02 Graphify: confirm the local code path makes no network calls; confirm the PyPI package identity behind `graphifyy`.
3. 22 Impeccable: confirm the rules in SKILL.md can be used without its hooks and cloud API.
4. 28 App Store Compliance: read the canonical OpenRoots text and NOTICE before any copying.
5. 45 Claude Trading Skills: confirm no order-placement or broker-credential code path is reachable from the methodology subset.
