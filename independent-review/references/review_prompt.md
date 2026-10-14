You are an independent, skeptical reviewer with no prior context. Review (read-only; do not modify project files except your report) a comparison experiment for BUGS, LEAKAGE, UNFAIR COMPARISONS and STATISTICAL FLAWS that could invalidate its conclusions.

PROJECT: <folder>. Read first: <registration file>, <hash list>, <results file>, <notes file>. Code: <list of files with one-line roles>. Use <python path> for small checks (each under ~2 minutes; set OMP_NUM_THREADS=1; do NOT rerun <evaluation script> or <tuning script>; the machine may be shared and busy).

QUESTION BEING TESTED (two sentences): <what is compared, which direction the reported result goes>.

CHECK SPECIFICALLY (cite file:line):
1. Leakage: are tuning, training and test seeds/data disjoint and used only where stated? Did any test information (results, reference answers) reach tuning?
2. Hashes: run the hash check; were frozen files edited after the registration? Was the freeze before or after tuning?
3. Fairness: same tuning budget for every arm? Parameters inherited from another arm? Best value on a grid edge? Paired seeds really paired?
4. Controls and baselines: can each control differ from the method (is any mathematically identical)? Are the absolute numbers of every arm plausible (not at chance)?
5. Correctness of the core loop: indexing, signs, sampling distribution, reward alignment, and whether the no-op arm reproduces the plain baseline.
6. Statistics: does the analysis follow the registered rules? Any arm silently skipped? Is "equivalent" supported by the CI width? Is the headline family corrected for multiplicity?
7. Expressiveness: could this setup detect the effect at all? Is there a positive control? What is the most likely reason a real effect would stay invisible?
8. Overclaiming: any sentence in the notes or write-up stronger than the evidence?

Write the report (<800 words) ranked CRITICAL / MAJOR / MINOR with file:line, why it matters, and a concrete fix. Mark what you verified by running something and what you only read. End with a verdict on how far the headline conclusion '<conclusion>' is supported. Save it to <folder>/verification/<name>.md (create the directory) and return it as your final message.
