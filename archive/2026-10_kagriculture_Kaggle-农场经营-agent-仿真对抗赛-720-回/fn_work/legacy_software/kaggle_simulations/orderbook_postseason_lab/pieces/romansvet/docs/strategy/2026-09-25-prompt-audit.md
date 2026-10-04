# Prompt audit (2026-09-25) — `/claude-api prompt-audit`

## Assumptions
- **Scope**: whole working directory. The repo makes **no LLM API calls** (bounded grep of src/, scripts/, S/pipeline, docs/, tests/ for anthropic/openai/messages.create/model IDs: none), so the prompt surface is the text that reaches Claude Code and its Opus subagents: the session memory (`~/.claude/projects/-mnt-e--work-kaggriculture3/memory/`, 258 files, `MEMORY.md` 24.2 KB loaded every session), `docs/PIPELINE.md`, `S/pipeline/50_new_switch.md`, `S/pipeline/60_actionrl.md`, `.claude/settings.local.json` (skill override only), and the ad-hoc Agent dispatch prompts composed each firing (not on disk). No CLAUDE.md / AGENTS.md / SKILL.md exists.
- **Target model**: Claude Fable 5.1 for the coordinating session (this harness); Claude Opus (Agent tool `model: opus`) for subagents. No migration in progress.
- Non-Anthropic provider markers: none.

## Inventory
| surface | files | provenance |
|---|---|---|
| memory feedback/rules | `feedback-*.md`, `no-polling.md`, `finalize-subagent-results.md`, `tight-budget-2026-09-14.md`, `dev-null-incident-2026-09-11.md`, `pytest-suite-oom-2026-09-16.md`, `MEMORY.md` | user corrections 09-05..09-24, each tied to a named incident |
| operator docs read by agents | `docs/PIPELINE.md` (e509c764, 09-21), `S/pipeline/50_new_switch.md`, `S/pipeline/60_actionrl.md` | written 09-19..21 for the same model family |
| request config | none (no SDK code) | — |

## Findings (highest confidence first)
Counts: Group 1 (dated prompt text) 3 findings; Group 2 (skill files) 0; Group 3 (tool descriptions) 0; Group 4 (request config) 0. Surface is largely clean: the emphatic prohibitions are all provenance-backed (each names a reproduced failure: /dev/null write, `pkill -f` self-kill, full-pytest OOM, TaskOutput transcript dump) and stay under keep-list item 5.

### F1 — subagent budget line asks for behaviour the target model already has (Medium, `rewrite`)
- Location: `memory/tight-budget-2026-09-14.md:16` (applied in every Agent dispatch).
- Evidence: "every Agent prompt must carry a strict-budget line (no narration, no re-reading, targeted tests, terse doc, hand-back ≤ 15 lines of numbers and verdict)".
- Pattern: 1a pressure language / 1d fossil. Fable 5 / 5.1 and Opus 4.8+ narrate less between tool calls by default and scope work to what is asked; "no narration, no re-reading" now reads literally and can suppress useful progress notes and the re-reads that catch stale state (the VRPREPAIR1 arm found an infeasible-route bug precisely by re-reading a dawn). The parts that carry information the model cannot know (hand-back ≤ 15 lines, targeted test files, terse doc) stay.
- Proposed replacement: "Budget is tight: pick the few tool calls that decide the verdict, run only the named test files, and hand back ≤ 15 lines of numbers plus the verdict."

### F2 — "NEVER"-cased rules restated in the always-loaded index (Medium, `rewrite`)
- Location: `memory/MEMORY.md` index lines for pgrep self-kill, /dev/null incident, pytest OOM, no-polling (9 pressure tokens in the index), and `no-polling.md:10`, `finalize-subagent-results.md:12`.
- Evidence: "NEVER TaskOutput a local_agent task", "never `kill $(pgrep -f …)`", "NEVER `pytest -q tests`", "NEVER message a running agent with follow-up scope".
- Pattern: 1a — say it at normal volume. The prohibitions themselves are load-bearing (each reproduced on this box and the reasons are recorded), so the action is case, not content: current models follow a plain statement exactly, and shouting in an always-loaded index risks over-triggering (e.g. refusing any SendMessage to a running agent, which is sometimes the right call for a bounded status ask).
- Proposed replacement (index hooks): "never TaskOutput a local agent (dumps the transcript into context)"; "kill literal PIDs only (`pkill -f` matched the tool shell once)"; "run named test files only (the full suite OOMs the box)"; "don't widen a running agent's scope by message (it withholds its report)". Bodies keep the incident dates.

### F3 — mannered headings in operator docs (Low, `flag`)
- Location: `S/pipeline/50_new_switch.md:97` ("the LAW you must not fight"), `docs/PIPELINE.md:169,176-181` (bolded LAW blocks), `S/pipeline/60_actionrl.md:63`.
- Pattern: idiom-dating only; the mechanics under each heading are contract text (precedence rule, PYTHONPATH routing) and stay. No edit proposed.

### Re-baselining checks (nothing to add)
- Long-horizon nudge (don't stop at "next I'll…"): already supplied by the harness system prompt and `be-proactive.md`.
- Batching independent tool calls: the harness already injects the nudge; dispatch prompts need nothing.
- Anti-formatting language: none present. "Answers 2–5 sentences" (`feedback-less-wordy.md`) is the user's quality bar and stays.
- Verbatim user directives in caps ("THEN CONTINUE PATH TILL WE HAVE IMPROVEMENTS!!!!") are quotations required by the memory format, not instructions authored for an older model; keep.

## Proposed diff (memory files; not applied)
```diff
--- memory/tight-budget-2026-09-14.md
-every Agent prompt must carry a strict-budget line (no narration, no re-reading, targeted tests, terse doc, hand-back ≤ 15 lines of numbers and verdict)
+every Agent prompt carries a budget line: "Budget is tight: pick the few tool calls that decide the verdict, run only the named test files, and hand back ≤ 15 lines of numbers plus the verdict."
--- memory/no-polling.md
-NEVER TaskOutput a local_agent task (it dumps the JSONL transcript into context — happened once, ~15k tokens)
+Do not TaskOutput a local agent task: it dumps the JSONL transcript into context (happened 2026-09-11, ~15k tokens)
--- memory/finalize-subagent-results.md
-NEVER message a running agent with follow-up scope (it withholds the report until its turn ends
+Do not widen a running agent's scope by message: it withholds its report until its turn ends; a bounded status question is fine
--- memory/MEMORY.md (index hooks only)
-- [pgrep self-kill](feedback-pgrep-self-kill.md) — never `kill $(pgrep -f …)`: matches the tool shell (exit 144); list PIDs, then kill
+- [pgrep self-kill](feedback-pgrep-self-kill.md) — kill literal PIDs only; `pkill -f`/`kill $(pgrep -f)` matched the tool shell once (exit 144)
```

## Verification plan (Step 7)
Behavioural probe, not self-report: after applying F1, compare the next two subagent hand-backs against the ≤ 15-line bar and check that no agent skipped a re-read that a gate depended on. F2 is case-only; verify by grepping the wider tree for the exact old strings (none are matched by tests or log parsers: `grep -rn "NEVER TaskOutput" S tests` is empty).

## Applied (user: "apply proposed diff", 2026-09-25)
F1 and F2 hunks applied to the memory files (`tight-budget-2026-09-14.md`, `no-polling.md`, `finalize-subagent-results.md`, `MEMORY.md` index hooks for pgrep, pytest, no-polling, finalize). F3 left as flag. Verification: next two subagent hand-backs checked against the ≤ 15-line bar.
