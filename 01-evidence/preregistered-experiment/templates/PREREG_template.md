# Preregistration: <name>

Status: written before any run on the test units. Frozen files and hashes: `PREREG_<name>.sha256`.
Tuning happened before / after the freeze (circle one and say what was frozen): ...

## 1. Question
One sentence. What would each outcome (A better / equivalent / worse) mean?

## 2. Arms
| arm | what it is | why it is here |
|---|---|---|
| main method | | |
| control 1 | | which factor it removes |
| baseline (tuned) | | |
| no-op / sanity arm | | must behave as expected |
| positive control | a task or setting with a planted effect | shows the design can detect an effect |

## 3. Units, metric, budget
- unit of replication: ...  n = ...
- metric: ... (direction: lower/higher is better)
- budget per arm (same for all): ...
- replicates per unit: ...

## 4. Seeds (disjoint)
- tuning: ...
- training (if any): ...
- test: ...

## 5. Tuning
Grid per arm, same budget for every arm. Parameters inherited from other arms: ... Edge rule: if the best value sits on the grid edge, extend as follows ...

## 6. Decision rules
- equivalence margin: ± ... (why this size)
- paired bootstrap over units, 4000 resamples, CI level ... (headline family: k contrasts, correction ...)
- verdicts: equivalent / A better / A worse / uncertain (see verdict.py)
- headline contrasts: ...
- descriptive-only contrasts: ...

## 7. Predictions (not criteria)
...

## 8. Known unfairness and limits I am accepting
...
