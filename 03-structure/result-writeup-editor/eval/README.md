# Evaluation of the narration flag in `doc_metrics.py`

Independent labels (context-free sub-agent, labels: narration / stance / fact / other) for sentences drawn from project write-ups. The sample is stratified: every flagged sentence plus a random sample of unflagged ones; recall is weighted by the sampling ratio. Run `python3 eval/score.py dev` or `python3 eval/score.py heldout`.

| Set | Used to tune the pattern? | Flagged | Precision | Flagged but stance | Recall (weighted) |
|---|---|---|---|---|---|
| dev (122 sentences, 6 documents) | yes (the pattern was revised after seeing its errors) | 26 | 0.65 | 0.19 | 0.74 |
| heldout (107 sentences, 8 documents) | no | 7 | 0.71 (n = 7, very small) | 0.00 | **0.07** |

## What this means
- The flag is a detector of **first-person work narration** ("我查了…", "I ran…"). On the dev set it is usable as a hint; on documents written in the impersonal change-log voice ("已改为…", "已记入偏离日志", "运行前已锁定") it misses almost everything, because that voice has no first person.
- That impersonal voice is normal and appropriate in deviation logs and registrations, so a low recall there is not necessarily a defect; but the metric must not be read as "amount of process narration in the document".
- Precision on the dev set is below the 0.8 that was set as a target; the patterns were not tuned further on the held-out set, to keep it clean.
- Use the metric to find first-person narration in prose posts; do not use it to rank files or to decide that a document is "clean".

## Next
A larger held-out set from prose posts (not logs), a second annotator for agreement, and separate treatment of change-log voice.
