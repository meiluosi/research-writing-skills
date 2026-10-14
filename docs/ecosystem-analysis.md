# Ecosystem analysis: what each skill is good for, and what is redundant

Scope: the open writing skills read while building this set, the author's own three writing skills, and the eight skills in this repository. Sources were read from their public repositories; sizes are file sizes at the time of reading. Claims about the registry-only skills are from their public descriptions and were not verified against their code.

## 1. Capability matrix

`●` primary, `○` partial, blank none.

| Capability | humanizer | stop-slop | avoid-ai-writing | elements-of-style | copy-editor | human-in-the-loop-writing | rewrite-fidelity | zh-disambiguate | this repo |
|---|---|---|---|---|---|---|---|---|---|
| Sentence concision | ○ | ○ | ○ | ● | ● | | | | `concise-edit` |
| AI-pattern removal, English | ● | ● | ● | | | ○ | | | `ai-pattern-edit` (points to others) |
| AI-pattern removal, Chinese | | | | | | ○ | | ○ | `ai-pattern-edit` |
| Document-level structure and narration | ○ (two patterns) | | | | | | | | `result-writeup-editor` |
| Drafting from evidence | | | | | | ● (with slots) | | | `tech-article-draft` |
| Author-presence audit | | | | | | ● | | | uses it |
| Meaning-preservation check | ○ (self-check) | | ● (verifier) | | | | ● | | `preservation-check` |
| Routing and handoff | | | ● (router, typed edges) | | ○ | | ○ | | `writing-router` |
| Detect-only and false-positive guard | | | ● | | | ○ | | | `ai-pattern-edit` (never a verdict) |
| Text meant for agents (tool descriptions) | | | | | | | | ● | uses it |
| Experiment trustworthiness (before writing) | | | | | | | | | `preregistered-experiment`, `independent-review` |

Reading the matrix: the English pattern-removal row has four owners and the preservation row has three; the document-level row and the experiment-trust rows have one each. Duplication is concentrated where it is cheapest to remove.

## 2. Per skill

### blader/humanizer (MIT, about 32 KB)
- **Effective:** patterns grouped by cause (staging, rhythm, inflation, formatting, leftovers, wrong reader) and ordered strongest first; structural habits that outlast model releases; explicit "when not to act" (quotes, titles, discussed phrases); a voice sample overrides the rules; file mode that changes prose only; "writing about the document instead of its subject" and "re-explaining what the reader knows" are the two closest ideas to document-level editing anywhere in the set.
- **Redundant / costly:** the word-level lists age with each model release; three return modes; English only; the whole file must be loaded for every use.
- **Verdict:** keep as the English long-tail reference. Do not re-implement its lists here.

### hardikpandya/stop-slop (MIT, about 2.6 KB plus references)
- **Effective:** tiny core, a quick-check list, a five-dimension self-score with a revise threshold.
- **Redundant / risky:** bans all adverbs and all em dashes, which collides with hedging and with legitimate dashes; reads as a style preference, not a rule that protects meaning.
- **Verdict:** borrow the self-score (already used in `ai-pattern-edit`). Do not adopt the blanket bans.

### conorbronsdon/avoid-ai-writing (MIT, about 33 KB main plus six sub-skills, 7 MB repository)
- **Effective:** the editing contract (a detected pattern is not authorisation to edit; scope comes from the user), treating the source as data, severity tiers, a bounded pass budget, a router with typed edges, a separate preservation verifier, and a false-positive reviewer that refuses to turn style signals into accusations.
- **Redundant / costly:** seven skills for one job; the main file is read in full on each run; English only; detector and validator infrastructure beyond what an editing session needs; its verifier duplicates `rewrite-fidelity`.
- **Verdict:** keep the architecture ideas (already in `writing-router`), keep the false-positive stance. Do not vendor it.

### obra/the-elements-of-style (no licence file, about 2 KB skill plus a long reference)
- **Effective:** a short numbered principle list; the "limited context: dispatch a sub-agent to copy-edit" tip.
- **Redundant / costly:** the reference is about 12,000 tokens; most grammar rules models already follow; no licence, so it cannot be forked and modified legitimately.
- **Verdict:** do not fork. `concise-edit` restates the principles independently.

### joellewis/skill-library, copy-editor (MIT, about 6.8 KB inside a larger collection)
- **Effective:** a five-step process (accept a rough draft, prune, adverb audit, an "all" check, read aloud), a common-mistakes list and a diagnostic checklist.
- **Redundant:** overlaps Strunk-based concision; the repository also holds four unrelated skills.
- **Verdict:** borrow the process shape for `concise-edit`. A fork would carry unrelated material.

### Technical-blog skills on public registries
- **Effective (from descriptions):** a pipeline from idea to structure to draft, a fixed output format, "every sentence needs a job".
- **Redundant:** they fill a template from a topic; none starts from an evidence inventory.
- **Verdict:** not forked. `tech-article-draft` is the independent design.

### Author's own skills
- **human-in-the-loop-writing:** keep unchanged as the author-presence layer. Its `absence_signals.py` overlaps `doc_metrics.py` only on first-person counting; the two answer different questions (is the author absent vs. is the author narrating logistics). Cross-reference, do not merge.
- **rewrite-fidelity:** the strongest verifier in the set. It checks modals, conditions, scope limits, quoted labels and number words in Chinese and English, and adds a model claim-check pass. `preservation-check` is weaker on all of those.
- **zh-disambiguate:** different job (one reading for an agent). Keep separate and cross-reference.

### This repository
| Skill | Unique value | Redundancy or weakness | Action |
|---|---|---|---|
| `preregistered-experiment` | Only skill covering registration, freezing, verdict rules | Template placeholders could be shorter | Keep |
| `independent-review` | Only skill for context-free review with verification of findings | None found | Keep |
| `tech-article-draft` | Evidence inventory before drafting; `[CONFIRM]` tags | Not yet tested on a real draft | Keep, test |
| `result-writeup-editor` | The only document-level editor; metrics script | Narration regex is a heuristic with false positives on results sentences ("We found 5%") | Keep, improve metrics |
| `concise-edit` | Chinese sentence rules | English half repeats Strunk and copy-editor | Shrink to the Chinese rules, link out for English |
| `ai-pattern-edit` | Chinese pattern list, domain-term guard, mandatory verify | English half repeats humanizer | Shrink to Chinese list plus guard, link out for English |
| `preservation-check` | PASS/FAIL line, comparison-operator check, strengthened-word check | **Largely redundant with `rewrite-fidelity`, and weaker** | Fold into `rewrite-fidelity` (see below) |
| `writing-router` | One handoff envelope and guards across both families | Must stay short | Keep, trim |

## 3. Redundancies to remove (ranked by payoff)

1. **Three verifiers.** `preservation-check` (this repo), `rewrite-fidelity` (author), and avoid-ai-writing's verifier do the same job. Make `rewrite-fidelity` canonical. Contribute what `preservation-check` has and it lacks: comparison-operator counts, a "claim strengthened" word list, occurrence-count changes, a single `RESULT:` line, and the rule that a lost hedge fails unless justified. Then reduce `preservation-check` to a short policy page that calls `rewrite-fidelity`, or delete it.
2. **Four English pattern lists.** Keep one English reference (humanizer) and link to it. `ai-pattern-edit` keeps only what no other skill has: the Chinese list, the domain-term guard, and the preservation requirement.
3. **Three concision sources.** `concise-edit` keeps the Chinese rules and links to the English ones.
4. **Two first-person counters.** `doc_metrics.py` and `absence_signals.py` should state which question each answers; do not merge.
5. **Router weight.** Keep a single routing table and a single envelope; drop the JSON graph if nothing reads it.

## 4. Proposed application chain after consolidation

```
evidence      preregistered-experiment -> independent-review
draft         tech-article-draft  (+ human-in-the-loop-writing for author presence)
structure     result-writeup-editor
language      concise-edit (zh rules)  ->  ai-pattern-edit (zh list + guard)
verify        rewrite-fidelity   (canonical; extended with the checks above)
route         writing-router
agent text    zh-disambiguate    (separate branch)
```

Six owned skills plus three external. The two verifier-style and two pattern-style duplicates disappear.

## 5. Acceptance tests for the next round
- `rewrite-fidelity` flags every case in `preservation-check/scripts/test_preserve.py` (port those tests).
- `result-writeup-editor` narration metric: on a labelled set of 100 sentences, precision of the narration flag is reported; target at least 0.8 before the threshold is used to rank files.
- A blind run of P2 on a document not used during development, reviewed by an independent agent, with no protected item changed.
- Token cost: each skill's description under 400 characters and its SKILL.md under 6 KB, with references loaded on demand.
