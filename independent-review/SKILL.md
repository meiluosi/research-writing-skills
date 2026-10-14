---
name: independent-review
description: "Use after you have results from an experiment or analysis and before you write conclusions: hand the project to a fresh, context-free sub-agent to find leakage, unfair comparisons, no-op baselines, broken controls, statistics that do not follow the registration, and claims stronger than the evidence; then verify its key findings yourself and correct the write-up. Triggers: independent review, second pair of eyes, audit my experiment, check for leakage, red-team the results, review before publishing, sub-agent review, 独立审查, 无上下文审查, 子 agent 审查, 挑错, 查泄漏, 结论是不是说过头了. Not a code-style review: it looks for things that make the conclusion wrong."
version: 0.1.0
---

# Independent Review

You are the worst person to find the flaws in your own experiment. You know what you meant, so you read the code as you intended it. A fresh agent with no context reads what is actually there. In the project this skill came from, nine such reviews each changed at least one sentence of the write-up: a "no difference" that was really "uncertain", a control that was mathematically identical to the method, a baseline stuck at chance level because of data order, an analysis script edited after the hash freeze.

The reviewer is an extra pair of eyes, not an authority. It misreads things too. The protocol below makes you check its important claims before acting on them.

## When to Use

- You have results and are about to write them up, or have just written them up.
- You changed the design after seeing a result and want to know whether that was safe.
- You are about to say "no effect", "equivalent", or "the real X does not help".

Run it once per stage (after tuning design, after the test run, after the write-up). Do not run it in a loop on the same files until it stops complaining.

## Process

### 1. Prepare the folder

Make sure the reviewer can find: the registration (or design notes), the frozen-file hash list, the code, the generated results, and your interpretation notes. If there is no registration, say so; that is itself a finding.

Run the mechanical check first so the reviewer's time goes to judgment:

```bash
python3 ../preregistered-experiment/scripts/freeze.py check PREREG_name.sha256
```

### 2. Spawn a context-free reviewer

Use a fresh sub-agent. Give it the prompt in `references/review_prompt.md`, filled in with paths. Rules:

- Read-only: it writes only its own report file.
- No history: do not paste your reasoning or your hopes. Describe the question and the reported result in two sentences, nothing more.
- Tell it what it may run (small checks, under two minutes) and what it must not (the full evaluation, tuning).
- Ask for a ranked report (CRITICAL / MAJOR / MINOR) with file and line, why it matters, and a concrete fix, plus a verdict on how far the headline conclusion is supported.

Start it in the background and keep working on something else; do not poll.

### 3. Verify before acting

For every CRITICAL and MAJOR finding, reproduce the evidence yourself with a small check or by reading the cited lines. Sort each into:

- **confirmed**: change the write-up or the experiment
- **partly right**: record what is true and what is not
- **wrong**: say why in the notes (the reviewer may have lacked context)

Do not copy the report into your notes unchecked. Do not dismiss a finding because it is inconvenient.

### 4. Write it down

Put the corrected interpretation in your notes file ("wording after review"), put procedural changes in the deviations log, and keep the reviewer's report in `verification/` unedited. Update every statement that was stronger than the evidence, including summaries and blog drafts that already exist.

### 5. Decide what needs another run

A review that finds a design flaw (features duplicate the heuristic, no positive control, a grid edge) usually means the honest conclusion is weaker, not that the experiment must be redone. Redo only if a cheap fix changes the answer. Otherwise state the limit.

## What a good reviewer looks at

`references/checklist.md` lists the checks that paid off. The short version:

1. Leakage: seeds, data splits, tuning on test, reference answers used in tuning.
2. Hashes: do they still match, was anything edited after the freeze, was the freeze after tuning.
3. Fairness: same tuning budget, inherited parameters, grid edges, paired seeds.
4. Controls: can each control actually differ from the method? Are absolute numbers sane (not at chance)?
5. Mechanics: indexing, signs, sampling distribution, reward alignment, equality of the no-op arm with the plain baseline.
6. Statistics: does the analysis script do what the registration says, are arms silently skipped, is "equivalent" justified by the CI width?
7. Expressiveness: could the setup have detected the effect at all? Is there a positive control?
8. Wording: is any sentence stronger than the evidence?

## Files

- `references/review_prompt.md` — the prompt to give the reviewer
- `references/checklist.md` — checks, each with the kind of failure it caught
