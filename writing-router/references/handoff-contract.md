# Handoff contract

One envelope travels with the text through the pipeline. Fill only what is observed or user-given; leave unknown fields empty rather than guessing.

```yaml
intent: restructure | trim | draft | de-ai | verify | audit-author | review-claims
language: zh | en | mixed
audience: who reads it, what they need to decide or learn
strength: light | standard | heavy          # result-writeup-editor
files: [paths]
protected:
  numbers: [list or "all"]
  verdict_words: [等价, 不确定, ...]        # wording of conclusions
  hedges: [可能, about, ...]
  literals: [urls, code, versions]
voice_sample: path or empty
steps_run:                                  # only with evidence
  - {skill: result-writeup-editor, evidence: "doc_metrics before/after table"}
flags: [claim_may_be_overreaching, figures_in_images, author_stance_unconfirmed]
passes_used: 0                              # cap 2
```

Edge types between skills:
- ROUTE: choose the owner.
- FEED: pass evidence (metrics, flags) without turning it into a command.
- VERIFY: require `preservation-check` on before/after.
- REPAIR: return a failed check to the editing skill once.
- ESCALATE: a flag that the claim itself may be wrong goes to `independent-review`.

A skill receiving an envelope must not widen scope, drop `protected` items, or mark `steps_run` for work it did not do.
