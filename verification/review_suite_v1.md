# Review of skills suite v0.1 (independent, skeptical)

Legend: [RAN] verified by executing; [READ] from reading only. Both test suites pass [RAN]; freeze.py write/check round-trip works [RAN]. Frontmatter: all 8 have name = folder and version 0.1.0 [READ].

## CRITICAL
1. **preservation-check/scripts/preserve.py misses negation and comparison flips, and it is the only gate.** [RAN]
   - "not significant" -> "significant": no flag (negation threshold is `max(2, 15%)`, so a single drop passes).
   - "没有证据表明有效" -> "有证据表明有效": only a verdict-word WARN, no negation flag.
   - "p < 0.05" -> "p > 0.05" and "A better than B" -> "B better than A": no flag.
   - "Always" / "Probably" at sentence start: strong-word and hedge lists are case-sensitive, so these are missed.
   - Why it matters: every pipeline ends here and the router calls it "required". A pass reads as safety.
   - Fix: flag any negation-count change, not just a large shift. Lowercase before matching. Track comparison operators. Diff negation-bearing sentences. Say in the output that a PASS is not evidence of equivalence.

## MAJOR
2. **Number extraction false ERRORs.** [RAN]
   - `5-10` -> `5 to 10` and `2026-10-14` -> `14 Oct 2026` report "-10"/"-14" lost.
   - `1e-3` -> `0.001` reports lost and added.
   - A line starting `42.5 percent` is parsed as list item "42." plus "5". So `42.5` -> `12.5` at line start is undetected.
   - Occurrence counts are ignored: `3 3 3` -> `3` passes.
   - Fix: treat `-` as a sign only after whitespace or an open bracket. Normalise ranges and dates. Require a list marker followed by space for enumerators. Compare Counters.
3. **doc_metrics.py `--compare` (named in result-writeup-editor step 7) is brittle.** [RAN]
   - `5 %` vs `5%`, and `1,000` vs `1000`, are reported as lost and added (no separator normalisation, unlike preserve.py).
   - Narration regex counts lines inside code fences and quotes: "I ran it" in a bash block and "> I checked quoted" were counted.
   - `## comment` inside a fence is counted as a heading.
   - "We found 5% gain" counts as narration, though it states a result.
   - The 14-character cap on the spine function word flags "1. Experimental setup and design: x" as off-spine.
   - Fix: strip fences before every line-based metric. Reuse preserve.py's number normaliser.
4. **Router pipelines contradict the router guards.** [READ]
   - Guard 2 caps editing at "two passes", but P1 chains three editing skills. "Pass" is undefined.
   - Guard 3 says verify after the last edit, but P2 ends `... preservation-check -> concise-edit (optional)`, leaving the final edit unverified.
   - REPAIR in skill-graph.json exists only for preservation-check -> result-writeup-editor, not for concise-edit or ai-pattern-edit.
   - skill-graph.json has no router -> preservation-check or router -> preregistered-experiment edge.
   - P5 (preregistered-experiment -> independent-review -> P1) has no stop condition if the review demands a re-run.
   - Fix: define "pass"; move preservation-check last in P2; add edges; cap review->rerun at one cycle, then report.
5. **"Required" is unenforced.** [READ]
   - Nothing blocks delivery without a preservation-check run.
   - `steps_run` evidence is honour-system.
   - Hedge loss is only a WARN, though the router says a hedge outranks concision.
   - Fix: have the script emit a PASS/FAIL line the envelope must quote. Make a lost hedge fail unless a justification is given.
6. **Teaching examples add unsourced claims.** [READ]
   - result-writeup-editor step 3: "看不出偏向" and "结论不变" are not in the source sentence. "区间下界到 −0.59" is also added.
   - The ~25% cut quota and "heavy: fixed length" push toward deleting hedges and caveats.
   - tech-article-draft lets the model write "stances on the author's behalf".
   - Fix: show examples that only restructure. Replace the quota with "cut only what the preservation list allows". Require such stances to be tagged [CONFIRM].
7. **NOTICE.md and README overclaim or dangle.** [READ]
   - "No text copied verbatim" and "none of their scripts were run" cannot be verified here. They are not checked against the third-party files.
   - The joellewis entry has no copyright holder, and no licence is named for it.
   - There is no LICENSE file, yet NOTICE says "Licence follows the repository".
   - preregistered-experiment/SKILL.md cites "README.md in the repo root", which will not exist after install.
   - README says the writing family "was checked on one seven-post series", with no artifact shipped.
   - Fix: soften to "written independently; patterns are common in the public literature". Add a LICENSE. Remove the dangling pointer. Ship or drop the evidence claim.

## MINOR
8. **Substring false positives in the lists.** [RAN]
   - "一定程度" gets an ERROR as "claim strengthened" when added. "制约" counts as the hedge "约". "大约" fires two hedge warnings.
   - Missing strong words: 证实, 显著, clearly, proven, demonstrates, 所有 / all.
   - Scope changes (Some -> All) pass silently.
9. **Trigger overlaps that will mis-route.** [READ]
   - "优化文章": writing-router and result-writeup-editor.
   - "tighten / 简化 / 精简": result-writeup-editor ("tighten this write-up"), concise-edit ("tighten the wording"), and the router's "help me edit".
   - "audit my experiment": independent-review vs preregistered-experiment.
   - "Not for" lines point both ways between tech-article-draft and result-writeup-editor (the second says to use the first for "first structure").
   - Descriptions are 600+ characters, and an agent that reads only part of one may miss "Not for".
10. **External dependencies have no fallback.** Pipelines P1 and P4 depend on human-in-the-loop-writing, which cannot be checked here. README and graph URLs are unverified. Fix: define the behaviour when the skill is missing.

## Verdict
Not ready to ship as-is. The structure is sound: frontmatter is consistent, every named skill exists or is listed as external, and the conflict rules agree with the skills. But the gate that everything relies on (preservation-check) misses the most dangerous edits, negation and comparison flips, and the router's guards contradict its own pipelines. Fix items 1, 2, 4 and 5, soften item 7, and re-test. Then it is a reasonable v0.2.

**Most important risk:** a false sense of verification.
