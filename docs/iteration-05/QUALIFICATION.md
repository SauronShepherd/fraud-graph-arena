# FGA 05 qualification

Run:

```text
python scripts/run_iteration_05_gate.py --package-root case-data/canonical/v1 --output reports/iteration-05/gate.json
python -m pytest tests/iteration_05 -q
```

The local gate imports all approved packages once, retries each nine times, and records run/publication counts and a topology hash. With the `sda` profile, the approved `sda_dev.sandbox` namespace has been qualified through clean recreation, 13-package loading, repeat loading, topology audit, row/provenance verification, and failure isolation. See the machine-readable reports under `reports/iteration-05/`.

The non-admin truth-table denial test is qualified with the `fga-web` profile. Response-loss and cleanup-failure boundaries are covered by explicit local test-only fault-injection points; the Databricks SQL adapter does not expose a safe transport fault-injection API, so those two transport fixtures are not claimed as live Databricks tests.
