---
name: preservation-check
description: "Use after ANY rewrite, trim, restructure, translation, or tone edit to check that the new text still says what the old text said: every number and interval bound, URLs and code spans, result verdicts (equivalent / uncertain / better / worse / no evidence), claim strength, hedges, negations. A fast heuristic checker plus a manual pass; the stricter sibling is the rewrite-fidelity skill if installed. Chinese and English. Triggers: did the edit change the meaning, verify nothing was lost, check the numbers survived, before/after check, 改完有没有丢数字, 核对改写, 保真, 结论强度有没有变. Not a style checker."
version: 0.1.0
---

# Preservation Check

An edit that makes a text shorter and cleaner can quietly change its claim: "uncertain" becomes "no effect", an interval bound disappears, "about 5%" becomes "5%", "may" becomes "does". The reader cannot see it; the author often cannot either. This skill compares before and after.

## When to use

After any edit by `result-writeup-editor`, `concise-edit`, `ai-pattern-edit`, a translation, or a human. Required step in the `writing-router` pipelines.

## Process

### 1. Run the checker

```bash
python3 scripts/preserve.py before.md after.md
python3 scripts/preserve.py before.md after.md --allow-number 3000 6000   # numbers you removed on purpose
```

The last line is `RESULT: FAIL | PASS WITH WARNINGS | PASS`; quote it in the handoff envelope. Exit code 1 means FAIL (an ERROR or an unjustified hedge loss). Justify a deliberate hedge removal with `--justified-hedge WORD`. It checks:

| Check | ERROR / WARN | What it catches |
|---|---|---|
| numbers lost or added (normalised: ranges, dates, 1e-3 = 0.001, 5 % = 5%); occurrence count changed | ERROR / WARN | silent data loss, invented figures |
| comparison operators (< > ≤ ≥) count changed | ERROR | p < 0.05 turned into p > 0.05 |
| URLs, inline code, versions lost | ERROR | broken references |
| a strong word newly appears (证明, 一定, 完全, 没有用, proved, always, never, no effect) | ERROR | claim strengthening |
| verdict words change count (等价/不确定/更好/更差/equivalent/uncertain) | WARN | a conclusion reworded |
| hedges lost (可能, 约, 似乎, probably, about, may) | FAIL unless justified | uncertainty removed |
| scope words change (all/every/所有/全部/任何) | WARN | scope widened or narrowed |
| any change in negation count (the sentences are printed) | WARN | "not significant" -> "significant" |

### 2. Read the manual list

The script cannot see these; check them by reading:
- a condition that is still present but now attaches to a different claim;
- a negation that moved to a different verb;
- a scope word narrowed or widened (all, most, in this setting);
- a causal word added ("because", "so") where the source only listed two facts;
- a comparison reversed (A over B -> B over A);
- units and denominators ("per 1000", "relative to the reference").

### 3. Decide each flag

For each ERROR or WARN: restore the source wording, or state why the change is correct ("number removed with the paragraph it belonged to"). Never "fix" a flag by editing the check. If the source itself was wrong, say so to the author instead of silently correcting.

### 4. Report

Return: result (pass / pass with justified changes / fail), the flag list with your decision for each, and what remains unverified (for example, figures inside images).

## Limits

It is a heuristic over surface tokens. It cannot judge meaning on its own; **a PASS means "no flagged change", not "equivalent".** It does not see a reversed comparison ("A better than B" -> "B better than A"), a narrowed scope that uses other words, or a condition that now attaches to another claim; the manual list in step 2 covers those. Figures, tables rendered as images, and code are out of scope unless they appear as text.

## Pairing
- Called by: `result-writeup-editor`, `concise-edit`, `ai-pattern-edit`, `writing-router`.
- Stricter alternative: `rewrite-fidelity` (separate repo) with modal strength, scope, and negation handling.
- If a flag reveals the original claim was overreaching, hand that to `independent-review`.
