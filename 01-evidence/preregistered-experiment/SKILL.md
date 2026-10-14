---
name: preregistered-experiment
description: "Use when starting or running a comparison experiment where you will report whether method A beats, matches, or loses to method B (ML, simulation, benchmarks, ablations) and you want the result to be believable: write the hypotheses and decision rules BEFORE running, freeze code with sha256 hashes, keep tuning and test seeds disjoint, run the test once, generate results with the registered script, log every deviation. Triggers: preregister, pre-register, preregistration, freeze the protocol, lock the code, decision rules before running, equivalence margin, tuning vs test split, deviation log, 预先登记, 先登记后运行, 锁哈希, 偏离日志, 等价边界, 调参集和测试集分开. Not for exploratory poking: use it when a conclusion will be written down."
version: 0.1.0
---

# Preregistered Experiment

A comparison experiment goes wrong in quiet ways: the metric gets picked after the numbers are seen, the test set leaks into tuning, a failing baseline is never noticed, "no difference" gets written as "equivalent". This skill is a short protocol that makes those mistakes hard. It was distilled from one long project (github.com/meiluosi/fly-connectome-study) where independent reviews overturned several of the author's own conclusions.

It does not make a result true. It makes it checkable.

## When to Use

- You are about to run something whose outcome you will describe as "A is better / equal / worse than B".
- You have a tuning step (learning rates, grids, thresholds) and a test step.
- A reviewer, a blog post, or a future you will have to trust the numbers.

Skip it for quick exploration. Do run it before any number goes into a write-up.

## Process

### 1. Write the registration (`PREREG_<name>.md`)

Copy `templates/PREREG_template.md` and fill every section **before running anything on the test set**:

- the question in one sentence, and what each outcome would mean
- what is compared, with the exact arms (including controls and a no-op/sanity arm)
- the metric, the unit of replication (instances, worlds, seeds), and the budget
- seed ranges: **tuning**, **training**, **test**, written as disjoint ranges
- tuning grids, per arm, with the same budget for every arm
- decision rules: equivalence margin, what counts as "better", which contrasts form the headline family (and the multiplicity rule), what is descriptive only
- your predictions, written down now, labelled "not a criterion"
- known unfairness you are accepting

The margin must be chosen from the scale of the problem, not from the data. If the paired standard deviation is SD and you have n units, the 95% half-width is about 2·SD/√n; if that is larger than half the margin, the design cannot show equivalence. Say so now and add units or widen the margin openly.

### 2. Add a positive control before you claim "no effect"

If the conclusion may be "nothing helps", include or build a task where you **know** an effect exists (plant it) and show the setup detects it. Without this, a null result only shows the setup is blind. Put it in the registration as a sanity arm.

### 3. Freeze

```bash
python3 scripts/freeze.py write PREREG_name.md  code1.py code2.py tuning_result.json ... > PREREG_name.sha256
```

Include the analysis script, the evaluation script, the registration file, and any tuning output the evaluation reads. Do the freeze **after tuning, before the test run**, and say in the registration that tuning happened before the freeze. A hash taken later only proves what was run, not that the design came first.

### 4. Run the test once, resumably

- One result file per key (arm, unit, replicate). Never one shared results file written by several processes: updates get lost.
- Pass `OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1` to every worker pool, or numpy's own threads will oversubscribe the machine.
- Run the heavy jobs first. Wait on a condition, not on a sleep.
- Do not look at test results and then change the arms, metric, or rules. If you must change something, see step 6.

### 5. Produce results with the registered script

`analysis_<name>.py` reads result files and writes `RESULTS_<name>.md`. Interpretation goes in a separate `NOTES_<name>.md`, so the generated numbers stay clean. `scripts/verdict.py` has the paired bootstrap and the verdict rule used here:

- **equivalent**: the whole CI lies inside ±margin
- **A better / A worse**: the CI excludes 0 and the mean passes the margin
- otherwise **uncertain**. Never write "no difference" for an uncertain verdict.

A CI that lies inside the margin but excludes 0 is "equivalent, but not zero". Report that sentence, because it is true.

### 6. Log deviations

Anything that changes after the freeze goes in `DEVIATIONS_<name>.md` (`templates/DEVIATIONS_template.md`): what was registered, what changed, why, whether any test result had been seen, and the new hash if a frozen file changed. Keep old results. Extensions you add after seeing results are labelled "exploratory".

### 7. Check before you write it up

```bash
python3 scripts/freeze.py check PREREG_name.sha256
```

It reports files whose hash no longer matches and files modified after the registration. Fix or log each one. Then hand the folder to an independent reviewer (see the `independent-review` skill).

## Common traps this protocol was built for

| Trap | What it looks like | Defence |
|---|---|---|
| Test used for tuning | best-of-N config chosen on the test numbers | disjoint seed ranges, tune on tuning units only |
| Winner's curse | tuned arm looks 0.4 points better on tuning, 0.05 on test | more tuning units, report tuning vs test gap |
| Grid edge | best value sits at the edge of the grid | extend the grid in the registration, same for every arm |
| No-op baseline | the "control" is mathematically the same as the method | check that each control can differ from the method |
| Broken control | dense control collapses to chance, inflating the gain | look at the control's absolute numbers, not just the difference |
| Hidden degeneracy | baselines sit at chance because of the data order | print absolute metrics of every arm |
| Equivalence by wording | "about the same" with no CI | margin + CI + verdict function |
| Features duplicate the baseline | learner just reproduces a heuristic already in the loop | correlate learned signal with existing heuristics before claiming anything |

## Files

- `scripts/freeze.py` — `write` and `check` for the hash file, reports files newer than the registration
- `scripts/verdict.py` — paired bootstrap CI and the verdict rule
- `templates/PREREG_template.md`, `templates/DEVIATIONS_template.md`
