---
name: edit-verification
description: "Use after ANY edit (restructure, trim, rewrite, translation) to prove numbers, conditions, hedges, scope and claim strength survived. Runs the rewrite-fidelity checker, adds a manual pass for what scripts cannot see, returns one RESULT line. Triggers: verify the edit, did the edit change the meaning, 改完核对, 保真检查. Not an editor, not a style checker."
version: 0.2.0
---

# Edit Verification

The gate at the end of every editing step. The mechanical work is done by the `rewrite-fidelity` skill (bundled as `external/rewrite-fidelity-skill`); this skill is the policy around it, so the chain has exactly one verifier.

## Process

1. **Run the check** (path relative to this skill's folder, or use the absolute path)
   ```bash
   scripts/verify.sh before.md after.md
   ```
   It runs `rewrite-fidelity` (literals, numbers including Chinese and English number words, modality, conditions, negation, scope bounds, quoted labels, per-operator comparisons, claim-strength words), then the number comparison from `result-writeup-editor`. Output ends with `RESULT: FAIL | PASS WITH WARNINGS | PASS`.
2. **Read the manual list** (scripts cannot see these):
   - a condition still present but now attached to a different claim;
   - a negation moved to another verb;
   - a comparison reversed in words ("A better than B" to "B better than A");
   - a cause added where the source only listed two facts;
   - scope narrowed or widened with different words;
   - units and denominators ("per 1000", "relative to the reference").
3. **Decide each flag**: restore the source wording, or state why the change is correct. A FAIL whose every flag is justified in writing is reported as `FAIL (all flags justified)` and may ship with that list; any unjustified flag blocks delivery. The `RESULT:` line itself is never edited. Never edit the check to make a flag go away. If the source itself looks wrong, tell the author; do not fix it silently.
4. **Report** the `RESULT:` line verbatim, each flag with your decision, and what is unverified (figures in images, text outside the files).

## Rules
- A PASS means "nothing mechanical changed", never "same meaning".
- A lost hedge, lost bound, lost number, new strong word, or flipped operator is an error until justified in writing.
- Without `rewrite-fidelity` installed, do the manual list in full and say the mechanical check did not run.

## Chain position
After `concise-edit`, `ai-pattern-edit`, or `result-writeup-editor`; called by `writing-router`. A flag showing that the original claim itself overreached goes to `independent-review`.
