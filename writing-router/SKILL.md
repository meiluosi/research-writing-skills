---
name: writing-router
description: "Use ONLY when a writing request does not name a skill or combines several jobs (draft, restructure, trim, de-AI, verify, audit author presence, review claims): classify the request once, pick the narrowest owning skill, pass one handoff envelope forward, run the pipeline in order, and stop when the job is done. Covers the research-process skills (preregistered-experiment, independent-review), the writing skills in this folder (result-writeup-editor, concise-edit, ai-pattern-edit, preservation-check, tech-article-draft), and optional external skills (human-in-the-loop-writing, rewrite-fidelity, zh-disambiguate). Triggers: which skill should I use, run the whole pipeline, 该用哪个 skill, 全流程处理. If the request is clearly one job (restructure, trim sentences, de-AI, verify), go straight to that skill."
version: 0.1.0
---

# Writing Router

Classify once, route to the narrowest owner, keep context in one envelope, stop at the cap. The router never edits text itself.

## Routing table (first match wins)

| The request is about | Owner | Notes |
|---|---|---|
| Whether the experiment or its claim is sound, before or after writing | `independent-review`; for new runs `preregistered-experiment` | Do this before polishing prose if results may change |
| A first draft or outline from results | `tech-article-draft` | Needs an evidence inventory |
| The author is missing, no stance or experience | `human-in-the-loop-writing` (external) | Its audit asks questions; it does not rewrite |
| Structure, headings, "too much I did", repetition, too long, hard mechanisms, "why this design" | `result-writeup-editor` | Default for result-heavy documents |
| Wordy or indirect sentences | `concise-edit` | |
| Sounds machine-written | `ai-pattern-edit` | Never as an authorship verdict |
| Did the edit change the meaning | `preservation-check` (fast) or `rewrite-fidelity` (strict) | Required after any edit |
| Chinese instructions for an agent (tool descriptions, prompts, error text) | `zh-disambiguate` (external) | Different goal: one reading for an agent |

Combined requests use a pipeline below. Ambiguous: ask one question (what is the text for, who reads it, how much cutting).

## Pipelines

| # | Situation | Order |
|---|---|---|
| P1 | New article from results | `independent-review` (if claims are strong) -> `tech-article-draft` -> author fills slots -> `human-in-the-loop-writing` audit (optional) -> `result-writeup-editor` -> `concise-edit` (optional) -> `ai-pattern-edit` (if needed) -> `preservation-check` |
| P2 | Trim and restructure an existing document or series | `result-writeup-editor` (diagnose -> headings -> narration -> subtract -> explain -> why) -> `concise-edit` (optional) -> `preservation-check` |
| P3 | "Sounds like AI" | `ai-pattern-edit` -> `preservation-check` |
| P4 | Author absent | `human-in-the-loop-writing` -> author -> P2 |
| P5 | Results not yet trustworthy | `preregistered-experiment` -> `independent-review` -> P1. If the review demands a re-run, allow one review -> re-run cycle, then report the open issues and stop |
| P6 | Strict meaning check on any edit | `rewrite-fidelity` (or `preservation-check`) |

## Handoff envelope

Carry only observed or user-given facts. Template and field meanings: `references/handoff-contract.md`. Minimum fields: intent, language, audience, strength (light / standard / heavy), files, protected facts (numbers, verdict wording, hedges), voice sample if any, steps already run with evidence they ran, flags.

## Guards
1. Never record a step as executed unless it ran. For `preservation-check` the evidence is its printed `RESULT:` line, which must be quoted in the envelope.
2. Definition: one *pass* = one editing skill applied once to the text. Cap: each editing skill at most once per request, and at most three editing skills per request. A failed `preservation-check` returns to the editing skill that caused the flag, once; if it fails again, stop and report the flags.
3. `preservation-check` runs after the last editing step and its `RESULT:` line is part of the deliverable. It is not enforced by tooling: do not hand text back as final without it, and say plainly if it was not run.
4. Do not move a number, verdict, or hedge out of the protected list without saying so.
5. Stop when the requested job is complete. Do not run optional steps unrequested.

## When an external skill is not installed
`human-in-the-loop-writing` missing: skip its audit, say so, and list the slots and unconfirmed stances yourself. `rewrite-fidelity` missing: use `preservation-check` and say that the stricter check was not run. `zh-disambiguate` missing: say the request needs it and stop for that part.

## Conflicts between skills
See `references/conflict-rules.md`. Short form: stance and experience are kept or added (human-in-the-loop-writing), task logistics are cut (result-writeup-editor); a hedge outranks concision; a number outranks style; the author's voice sample outranks pattern rules; a domain term outranks a pattern list.

## Files
- `references/handoff-contract.md`, `references/conflict-rules.md`, `references/skill-graph.json`
