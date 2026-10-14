# Heading spines

A spine is the fixed order of chapter functions. Readers learn it once and then skim. Use `N. function: point`; the point is a claim or a content label, not a topic.

## Experiment or result post
1. Motivation: why this question / why this task
2. Setup: world, data, arms (what is compared)
3. Result: what was found (3.1, 3.2 for separate findings)
4. Check: how a surprising result was ruled out as an artifact
5. Limits: only what is specific to this post
6. Next

## Audit of someone else's method
1. Entry point: the observation that shapes the audit
2. Design: benchmarks, replication, opponents
3. Findings: numbered, one claim per sub-heading
4. Failures: mistakes in the audit itself
5. Boundary: what the audit does not show
6. Takeaways
7. Next

## Multi-round study (rounds with revisions)
Each round has the same three sub-headings: `### Method`, `### Result`, `### Issues found`. After the rounds: `Overview` (all rounds side by side), then `Wording of the conclusion`.

## Process or protocol post
Scenario → Pipeline → Checkpoints (what each step catches) → Takeaways → Blind spots.

## Series summary
Recap → Conclusion → Credibility (what can and cannot be trusted) → Lessons → Assessment → Next steps → Resources.

## Lint rules (what `doc_metrics.py` flags)
- level-2 heading without a number, or without a colon after a short function word;
- a bold paragraph leader that should be a level-3 heading;
- the same function word spelled two ways across a series ("Limits" in one post, "Boundary" in another, unless they mean different things);
- more than one "limits" chapter per post.

## Examples
Before: `## 先说一个场景` `## 流程只有七步` `## 审查实际抓到了什么`
After: `## 1. 场景：我把“被超过”写成了“等价”` `## 2. 流程链路：从登记到更正的七个环节` `## 3. 审查点：四个项目里抓到的问题`
