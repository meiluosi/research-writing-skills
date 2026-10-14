---
name: result-writeup-editor
description: "Not for sentence polish (concise-edit) or AI-sounding patterns (ai-pattern-edit). Use to edit a result-heavy document (experiment write-ups, audits, retrospectives, technical posts, a series) at the DOCUMENT level: headings into a spine 'N. function: point', process narration into statements, cut repetition, plain-language explainers, 'why this design' tables, then verify. Triggers: restructure headings, cut the narration, 做减法, 标题结构化, 去掉流水账, 补大白话, 补为什么."
version: 0.2.0
---

# Result Write-up Editor

Most editing skills work on sentences: cut a filler word, break a triad, remove an AI phrase. A result write-up usually fails one level up. The headings do not say what each chapter is for. The author keeps narrating their own work ("I checked, then I changed it, then I reran") instead of stating what is true. The same limitation appears in five posts. A hard mechanism is explained in jargon only. This skill edits that level and then proves the numbers survived.

It was distilled from a seven-post series that was edited twice by hand; the rules below are the rules that edit used.

## When to use

- A document or series reports experiments, audits, comparisons, or a project history.
- The author says it is too long, too much "I did X", too repetitive, hard to follow, or headings feel arbitrary.
- Someone needs the reader to know why a design choice was made, not only what it was.

If the text is only clumsy sentences, use `concise-edit`. If it sounds machine-written, use `ai-pattern-edit`. If the author is missing from the piece, use `human-in-the-loop-writing` first (see Pairing).

## Process

Run the steps in this order. Steps 1 and 7 are mandatory.

### 1. Diagnose before touching anything

```bash
python3 scripts/doc_metrics.py post1.md post2.md ...
```

It reports narration density, first-person density, headings off the spine, limit sections, boilerplate (preface/outro/teaser lines), and near-duplicate sentences across files. Read the numbers as hints, then read the text. Mark reviewed lines you keep on purpose with `<!--keep-->`; headings such as a glossary or reproduction note are exempt by default (`--exempt`). The title block (h1 plus a one-line blockquote) is not boilerplate.

Write a short edit plan: which rules apply to which file, expected size change, anything you will keep on purpose. In an interactive session show it before a large edit; in a non-interactive run print it at the top of the report, proceed with the standard defaults, and list the assumptions you made.

### 2. Give headings a spine

Every level-2 heading names the function of the chapter, then its point: `N. function: point`.

| Document type | Function words that work |
|---|---|
| Experiment or result post | motivation, setup, participants, method, result, anomaly, check, cause, limits, next |
| Audit or review | entry point, design, findings, failures, boundary, takeaways |
| Process or protocol | scenario, pipeline, checkpoints, takeaways, blind spots |
| Multi-round study | round 1/2/3 each with: method, result, issues found |
| Summary | recap, conclusion, credibility, lessons, assessment, next steps, resources |
| Single-post retrospective | motivation, setup, original claim, review, corrected test, result, lessons, limits |
| Glossary or reproduction note | exempt from the spine; keep it short and put it where the reader first needs it |

Use the same function words across a series. Level-3 headings may use `N.M function: point` or plain labels; be consistent inside a post. Replace bold paragraph leaders ("**Result.** ...") with level-3 headings. A heading that is only a topic ("Results") gets its point: "3. Results: four findings". Details: `references/heading-spines.md`.

### 3. Turn narration into statements

Process narration says who did what. Statements say what is the case. A conversion may reorder and shorten; it may not add a finding, a cause, or a verdict that the source did not state. If the source gave no cause, do not supply one.

| Narration | Statement |
|---|---|
| 我查了：被选中的索引平均在 990 左右，前半部分占 51%。但我还是把并列改成了显式的随机打破 | 排查：被选中的索引平均在 990 左右，前半部分占 51%。仍改成显式随机打破。 |
| 我第一反应写的是“没有任何特征映射超过 0.5”，审查指出这句话说过头了，两个区间的下界到了 −0.59、−0.72 | 原先的结论“没有任何特征映射超过 0.5”说过头了：区间下界到了 −0.59、−0.72。 |
| I ran the sweep and noticed X | The sweep shows X. |

Rules:
1. Keep first person for **stance, trade-off, or an experience only this author had** ("I would not publish this without a positive control"). Cut it for **task logistics** (I ran, I wrote, I checked, I changed).
2. Keep one or two failure stories when the story carries the lesson (a wrong claim that was overturned). State the rest as a fact with its cause.
3. Do not drop the cause or the number. The statement version must say what was found and what changed.
4. Use one pronoun for the author throughout a series ("我", not "我们" in one post and "我" in another).
5. Cut method narration the reader can already see ("the table below compares", "I organised this by"). Keep a source credit the reader can follow.

Pattern lists in Chinese and English: `references/narration-patterns.md`.

### 4. Subtract

Standard strength aims at roughly a quarter off the **original prose**; tables you add in steps 5 and 6 should replace paragraphs, not sit on top of them. A document dense with numbers and intervals may not shrink at all, because the numbers must stay: that is an acceptable result, report it. The target is a guide, never a reason to cut evidence. Apply in this order:

1. **Each fact once.** Search the series for repeated statements (`doc_metrics.py` lists near-duplicates). Keep the fullest version in the post that owns the topic; elsewhere give a one-line pointer ("details: post 4").
2. **Consolidate limits.** Keep only limits specific to this post. Put series-wide limits in the summary.
3. **Delete preface and outro.** "What this post covers", "Thanks for reading", and teasers longer than one line. A next-post pointer is one short line.
4. **Tables only when they add structure.** If a paragraph and a table say the same thing, keep the one that reads faster.
5. **Cut hedges that carry no content, keep hedges that carry uncertainty.** "Probably" stays when the author is not sure.
6. **One document repeating itself.** If a conclusion appears in the summary line, in "what remains", and in the lessons, keep the fullest version in one place (usually the final chapter) and shorten the others to a pointer. If a limit is repeated inside the same document, state it once.
7. **Do not cut**: numbers, intervals, sample sizes, the reason for a design choice, a caveat that changes how a result should be read.

Strength levels: light (wording only), standard (above), heavy (also merge chapters). Every level cuts only what the protected list (numbers, verdict words, hedges, literals) allows. Ask which level if the author has not said.

### 5. Explain hard mechanisms in plain language

When a mechanism is only described in jargon, add a table:

| Mode | Plain analogy | What actually happens | Real or assumed |
|---|---|---|---|

Add one when a term or mechanism is used without definition and a non-specialist reader of this document would stall on it. Rules: say first what the thing is not (real or assumed); give an analogy a non-specialist knows; then the exact mechanism with its parameters; mark any explanation you are offering but have not tested as untested. **Analogies are the editor's addition, not facts from the source: list each one in your report for the author to confirm.** Example in `references/explainer-patterns.md`.

### 6. Add the reason for each design choice

For a design the reader may question, add a two-column table `design | reason`. Reasons must be real: a source, a constraint, a prior result, or an honest "no biological basis, the simplest interface". Never invent a rationale. Take reasons from the text, including later chapters (add a pointer if the reason lives elsewhere). If the author gave none and the reader would plausibly ask, add a row "reason not recorded" and list it in your report; if the reader would not ask, leave the design out of the table.

### 7. Verify

```bash
python3 scripts/doc_metrics.py --compare before.md after.md
```

Then run `edit-verification` (it calls `rewrite-fidelity`) and quote its `RESULT:` line in your report. Required: no number lost or added without an explicit reason, no claim strengthened ("uncertain" must not become "no effect"), no hedge dropped without a stated reason, interval bounds intact. A PASS is not proof of equivalence: read comparisons, scope, and condition attachment yourself. Re-run `doc_metrics.py` on the result and report before and after.

## Output

Return: the edit plan, the edited file(s) (or a diff when asked), a metrics table before/after, and a list of anything you were unsure about and left alone. Do not present the edit as finished if verification found a change you cannot justify.

## Pairing

| Need | Skill |
|---|---|
| Author is absent, text has no stance or experience | `human-in-the-loop-writing` (adds the author; this skill removes logistics) |
| Sentence-level concision | `concise-edit` |
| AI-sounding patterns | `ai-pattern-edit` |
| Prove numbers and claims survived | `edit-verification` (uses `rewrite-fidelity`) |
| A draft needs a first structure | `tech-article-draft` |
| The results themselves may be wrong or overclaimed | `independent-review`, `preregistered-experiment` |
| Which skill, in what order | `writing-router` |

Conflict rule with `human-in-the-loop-writing`: that skill asks for more first person and real experience; this one cuts process narration. They agree once you separate **stance and experience** (keep, add) from **task logistics** (cut).

## Files

- `scripts/doc_metrics.py`: metrics, duplicates, number comparison
- `references/heading-spines.md`, `references/narration-patterns.md`, `references/explainer-patterns.md`
