# Skill test report (standard strength)

**Edit plan**: spine all 10 h2 as "N. function: point" (术语/动机/设置/原先的结论/审查/修正后的检验/结果/教训/局限/复现); convert logistics narration to statements; keep stance and failure stories; cut duplicates; add one explainer table (3 control arms); add one design|reason table.

**Metrics** (before -> after): chars 4780 -> 4796 (+0.3%, target was -25%); narration/1000 1.88 -> 0.42; first-person/1000 6.07 -> 1.25; h2 off-spine 10/10 -> 0/10; limit sections 1 -> 1; boilerplate 0 -> 0. --compare: no numbers lost or added. preserve.py: 0 errors, 0 warnings.

**Kept on purpose**: the one-liner summary; "其中好几个问题，我自己连续做了几轮都没有发现" (failure story); lessons 2 and 3 first person (stance); all intervals, counts, thresholds (77% vs 75%, 26 cells); "LLM agent same model family" caveat; the "分歧没有来源" finding; all hedges and "未通过/不足" verdicts.

**Cut**: duplicate "no multiplicity correction" in 6.1, lesson 6 (repeats 6.1), LIF limit repeated from 6.6, filler phrases.

**Preservation flags**: none raised. Manual check: "设计 | 原因" rows paraphrase text-stated reasons (floor effect, r≈−0.93 confound, λ chosen on test set, integer synapses). One row "有界乘法规则 | 原因文中未记录" is my addition per step 6; it is an absence statement, not an invented reason. Needs author confirmation.

**Ambiguities in the skill instructions**
1. Standard "~25% cut" conflicts with steps 5-6 (add tables) and "do not cut numbers". This doc is number-dense, so net size did not shrink. Say whether the target is net or applies to the original text only, and whether added tables count.
2. doc_metrics flags every heading including "先说几个词"; no guidance for glossary, one-liner summary, or the h1/blockquote preface (is the "本文记录..." blockquote boilerplate?).
3. Spine function words lack "glossary", "motivation+setup for a single-post retrospective", "lessons". I improvised.
4. Spine rules cover h2 only. This doc has a numbered ### list (1-6) inside one chapter; unclear whether to prefix ### (a "3.1" style would trip the number checker, which strips only "N."). Also whether "Result" subheads should follow the "N. function: point" form.
5. Narration regex flags the one-liner and stance sentences ("我改隔间归属时..."); skill says keep stance, but no way to mark reviewed items.
6. Step 6 "reason not recorded" row: does it belong in the table, or should unexplained designs be omitted? Ambiguous. Also where the table goes in a document whose reasons come from later chapters.
7. Explainer step says "when only jargon": no threshold. The glossary already defines terms; I only added a table for the control arms. Analogies I wrote are mine, not text facts; skill does not say whether analogies need author sign-off.
8. Rule 4 (one pronoun) irrelevant for single doc. Limit consolidation says "series-wide to summary"; no instruction for a single post's duplicated limits vs body text.
9. Missing: a rule on "wording of conclusion" duplication between one-liner, "what remains", and lessons; no guidance on which to keep.
10. Step 1 says show the plan before a large edit; no instruction for non-interactive runs.

---
## Follow-up (v0.2)
Findings 1–10 above were addressed in SKILL.md and scripts: size target now applies to original prose and yields to the protected list; glossary/reproduction headings are exempt (`--exempt`); spine entries added for single-post retrospectives; `N.M` sub-headings allowed and the number checker strips them; `<!--keep-->` marks reviewed lines; "reason not recorded" rule and analogy-confirmation rule added; repeated conclusions and in-document repeated limits have a rule; a non-interactive path is defined.
The stricter `preserve.py` v0.2 flags one ERROR on this blind test's output (an `=` count change, later downgraded to WARN): the original v0.1 check had reported none.
