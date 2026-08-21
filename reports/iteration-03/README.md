# Iteration 03 evidence

Run `python scripts/run_iteration_03_gate.py --report reports/iteration-03/gate.json` from a clean candidate checkout. The runner records the exact commit, environment, clean-source status, per-check output, and whether every mandatory check passed.

Two independent clean candidate runs are required by the repository policy before closure evidence or an immutable tag is created. Approved artwork is an external prerequisite; this runner intentionally does not fabricate approval metadata.
