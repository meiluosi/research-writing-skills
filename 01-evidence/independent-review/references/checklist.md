# Checklist, with the failures each item caught

| Check | Failure it caught |
|---|---|
| Seed ranges disjoint; tuning never sees test | a tuning range that was a prefix of a test instance family (harmless here, but not "disjoint") |
| Hash check; edits after registration | an analysis script edited after the freeze; hashes taken after tuning only freeze the outcome |
| Same tuning budget; inherited parameters | learners inheriting the baseline's hyperparameters; baseline tuned over more configs |
| Best value on the grid edge | baseline and learners both sitting at the edge, so the real optimum was not reached |
| Winner's curse | a tuned arm 0.3–0.4 points better on tuning and 0.05 on test |
| Control can differ from the method | a "multi-head" baseline that was mathematically identical to the single-head method |
| Absolute numbers of each arm | baselines at chance level because of class-ordered data; a dense control collapsing to chance and inflating the gain |
| Confounds in a manipulated variable | an "overlap" knob correlated −0.93 with in-degree homogeneity |
| Exclusion rules | the same five NaN seeds removing whole partitions at the high end of a regression |
| Floor effects / capped metrics | forgetting capped by (learned − chance), so weak learners forget less by construction |
| No-op arm equals the plain baseline | verified bit-for-bit with the learner switched off |
| Sampling and indexing | confirmed sampled step distribution matches the weights; previous/current/next alignment in a learning update |
| Feature redundancy | learned feature correlated 0.85 with a heuristic already in the loop |
| Expressiveness probe | learned values that did not vary with the feature the study was about (residual ±0.01) |
| Positive control | none existed, so "no effect" could not be distinguished from "cannot detect" |
| Verdict rule vs registration | "equivalent" claimed where the CI touched the margin or excluded zero |
| Silent skips | analysis wrapped in try/except that dropped missing arms |
| Wording | "equivalent" written where the data showed "dominated"; "no usable information" written after testing one hypothesis |
