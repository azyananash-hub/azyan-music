# CROSS-AGENT-COMPATIBILITY — ZY v0.8 Intelligence Audit

Principle: the presence of a `SKILL.md` file does not establish compatibility. Each agent is classified separately, and each classification names what kind of use it supports.

## 1. Classes

| Class | Meaning |
|---|---|
| NATIVE | The agent loads and executes the artefact as shipped (skill folder, plugin manifest, or MCP config), in an environment verified for that agent |
| ADAPTABLE | The instruction content can be used after a manual or scripted adaptation. Hooks, MCP and installers are not portable |
| REFERENCE ONLY | Read as knowledge. No execution, no tool access, no scripts |
| UNSUPPORTED | The artefact cannot run in that agent's model (for example, a runtime or server that the agent cannot start) |
| UNVERIFIED | Claimed or manifest-declared, but not tested here |

## 2. What was verified in this session

| Agent | Status in this session | Evidence |
|---|---|---|
| Claude Code (cloud sandbox) | Environment in use; skill discovery is verified by the library's own tests and tooling. Hooks and MCP were not executed | Shell, file tools, registry, unit tests from earlier versions |
| Claude Chat | Not tested | No access from this session |
| Codex | Not verified. Earlier attempts to reach developer documentation failed (DNS). Manifest and AGENTS.md presence in repositories is recorded but not treated as proof | PROGRESS.md (Codex discovery marked unverified) |
| ChatGPT | Not tested | No access from this session |
| Gemini CLI | Not tested. Manifests such as `gemini-extension.json` and `GEMINI.md` are present in some repositories | Triage counts only |
| Gemini Chat | Not tested | No access from this session |
| Antigravity | Not tested. Some READMEs list it as supported | README claims only |
| Local AI | Not tested. Would require the owner's machine and a local client | Owner hardware not accessible from this session |

Consequence: no candidate can be described as universally compatible. The classes below are based on file structure and declared support. Each UNVERIFIED cell is an open test item in `BENCHMARK-AND-ROLLBACK-PLAN.md`.

## 3. Candidate matrix (ADAPT, MERGE, KNOWLEDGE ONLY, DOMAIN ONLY, DEFER)

| ID | Candidate | Claude Code | Claude Chat | Codex | ChatGPT | Gemini CLI | Gemini Chat | Antigravity | Local AI | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 22 | Impeccable | NATIVE (plugin and skill in repo) | ADAPTABLE (paste rules) | UNVERIFIED (AGENTS.md present) | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED (README claims) | ADAPTABLE | Hooks are Claude/Cursor specific; not portable and not adopted |
| 23 | Hallmark | NATIVE (plugin manifest) | ADAPTABLE | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED (README claims) | ADAPTABLE | Gate tiers only; installers excluded |
| 26 | Modern Web Guidance | NATIVE (claude plugin manifest) | ADAPTABLE | UNVERIFIED (codex plugin manifest present) | REFERENCE ONLY | UNVERIFIED (gemini extension manifest present) | REFERENCE ONLY | UNVERIFIED | ADAPTABLE | Pinned offline subset; cron installer excluded |
| 27 | Diagram Design | NATIVE (skill folder) | ADAPTABLE | UNVERIFIED (codex plugin manifest present) | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | ADAPTABLE | Output is one HTML/SVG file: portable to any chat that can render it |
| 35 | Video Shotcraft | NATIVE (SKILL.md) | ADAPTABLE (recipe cards as text) | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | ADAPTABLE | Its renderer is HyperFrames; ZY adapts recipes for Remotion only |
| 36 | GSAP Skills | NATIVE (plugin and SKILL.md) | ADAPTABLE | UNVERIFIED (AGENTS.md present) | REFERENCE ONLY | UNVERIFIED (GEMINI.md present) | REFERENCE ONLY | UNVERIFIED | ADAPTABLE | Guidance text; GSAP library itself not part of ZY |
| 43 | Three.js Game Skills | NATIVE (SKILL.md folders) | ADAPTABLE | UNVERIFIED (README claims Codex) | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | ADAPTABLE | Scaffold and helper scripts not adopted |
| 45 | Claude Trading Skills | NATIVE (SKILL.md, CLAUDE.md) | ADAPTABLE (methodology text) | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | ADAPTABLE | Scripts need data APIs; excluded |
| 31 | FFmpeg Skill | NATIVE (already imported) | ADAPTABLE | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | NATIVE (FFmpeg is local) | Already in library at recipe level |
| 04 | Superpowers | NATIVE (already imported; 14 of 15) | ADAPTABLE | UNVERIFIED (AGENTS.md present) | REFERENCE ONLY | UNVERIFIED (gemini manifest present) | REFERENCE ONLY | UNVERIFIED | ADAPTABLE | Already in library |
| 17 | Chrome DevTools MCP | NATIVE via MCP (not adopted) | UNSUPPORTED (no MCP client) | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | ADAPTABLE (knowledge only) | MERGE as knowledge into webapp-testing |
| 01 | ECC | NATIVE for its own plugin (not adopted) | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | Concepts only |
| 07 | Plannotator | NATIVE via hooks (not adopted) | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | Approval concept only |
| 12 | Awesome Free LLM APIs | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | List only; provider claims unverified |
| 16 | AG-UI | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | Protocol spec |
| 28 | App Store Compliance | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | Licence pending |
| 37 | Motionmaxxing | REFERENCE ONLY (SKILL.md present; rubric concepts) | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | Rubric concepts for K7 |
| 47 | Qlib | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | Methodology reference |
| 50 | MuMuAINovel | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | GPL; no code reuse |
| 13 | Ollama | REFERENCE ONLY (runtime, not a skill) | UNSUPPORTED | UNSUPPORTED | UNSUPPORTED | UNSUPPORTED | UNSUPPORTED | UNSUPPORTED | NATIVE (is the local runtime) | Hardware and approval gates apply |
| 24 | Astryx | UNSUPPORTED for Flutter (React only) | UNSUPPORTED for Flutter | UNSUPPORTED for Flutter | UNSUPPORTED for Flutter | UNSUPPORTED for Flutter | UNSUPPORTED for Flutter | UNSUPPORTED for Flutter | UNSUPPORTED for Flutter | Web-only relevance |
| 25 | Shadcn Admin | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | Web dashboard reference |
| 44 | Anatomy | NATIVE (SKILL.md) | ADAPTABLE | UNVERIFIED (README lists Codex) | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED (README lists Antigravity) | ADAPTABLE | Global install excluded |
| 02 | Graphify | UNVERIFIED (command-based integration claimed) | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED (gemini extension manifest) | REFERENCE ONLY | UNVERIFIED | ADAPTABLE (CLI, if verified) | DEFER |
| 30 | HyperFrames | NATIVE only after telemetry removal (plugin manifest present) | ADAPTABLE | UNVERIFIED (codex manifest present) | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | ADAPTABLE (needs Chrome and FFmpeg) | DEFER |
| 33 | Voicebox | UNVERIFIED (local MCP at 127.0.0.1) | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | NATIVE (local app) | DEFER; benchmark first |
| 41 | ComfyUI | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | NATIVE (local app) | DEFER; hardware |
| 42 | 3Dviz Pro Max | NATIVE (SKILL.md present) | ADAPTABLE | UNVERIFIED (codex manifest present) | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | ADAPTABLE | DEFER: telemetry path |
| 49 | FinGPT | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | REFERENCE ONLY | ADAPTABLE (heavy models) | DEFER |
| 05 | Open Code Review | UNVERIFIED (plugin manifests present) | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | REFERENCE ONLY | UNVERIFIED | ADAPTABLE (CLI, LLM key required) | DEFER |

## 4. Reading the table

- Claude Code is the only agent in which execution was observed in this session. Every other NATIVE claim is a claim about the artefact, not about the agent.
- Scripts and CLIs are ADAPTABLE for a local AI only if the local client can run them. Owner approval and verified binaries are required first.
- MCP entries are not adopted under any agent, for the reasons in `SECURITY-LICENSE-MATRIX.md`. A "NATIVE via MCP" cell describes a capability of the agent, not an approval to use it.
- Hooks are never portable across agents and are not adopted (`SECURITY-LICENSE-MATRIX.md`, section 2).
