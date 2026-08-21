# FGA 05 qualification

Run:

```text
python scripts/run_iteration_05_gate.py --package-root case-data/canonical/v1 --output reports/iteration-05/gate.json
python -m pytest tests/iteration_05 -q
```

The local gate imports all approved packages once, retries each nine times, and records run/publication counts and a topology hash. With the `sda` profile, the approved `sda_dev.sandbox` namespace has been qualified through clean recreation, 13-package loading, repeat loading, topology audit, row/provenance verification, and failure isolation. See the machine-readable reports under `reports/iteration-05/`.

The remaining external qualification gap is the true non-admin truth-table denial test: both available profiles resolve to the administrator identity, so that negative test is recorded as `not_qualified` rather than inferred from admin-session grants. Live response-loss, cleanup-failure, and byte-conflict fixtures are likewise represented by local deterministic tests until a supported fault-injection adapter is available.
