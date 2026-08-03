# Apply the Academy-first Iteration 01 to the qualified Iteration 00 checkout

From the existing Fraud Graph Arena repository:

```text
git switch Iteration-00
git switch -c Iteration-01
git apply --check /path/to/fraud-graph-arena-iteration-01-academy.patch
git apply /path/to/fraud-graph-arena-iteration-01-academy.patch
```

Then install and qualify the candidate:

```text
python -m pip install -e ".[test]"
python -m pytest -v

cd apps/web
npm install
npx playwright install chromium
npm run typecheck
npm run test
npm run test:e2e
```

Return to the repository root and run the complete iteration gate:

```text
python scripts/run_iteration_01_gate.py --report reports/iteration-01/gate.json
```

Do not close or tag Iteration 01 unless `fully_qualified` is `true`. The expected player route is:

```text
Launch → Detective Academy → ACADEMY_001 → opening comic → empty board → refresh-safe recovery
```
