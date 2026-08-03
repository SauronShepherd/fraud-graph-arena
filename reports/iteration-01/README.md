# Iteration 01 implementation evidence

This directory records the checks executed while preparing the Academy-first Iteration 01 implementation candidate.

## Executed successfully

- Python source compilation: passed.
- Backend, catalogue, narrative, persistence, contract, architecture, opening-comic and SPA fallback tests: **25 passed**.
- Core frontend and test TypeScript sources were parsed and checked with temporary ambient framework stubs. This catches local syntax and internal type errors, but it is not a substitute for the dependency-backed frontend gate.
- The generated OpenAPI contract includes the Academy catalogue, `INTRO_PENDING` lifecycle, opening sequence and opening-completion endpoints.

## Included but not executed in this sandbox

The sandbox package mirror does not provide `@playwright/test`, so the actual npm dependency installation could not complete. Consequently, the dependency-backed TypeScript typecheck, Vitest component suite and Playwright browser suite were not executed here.

The repository includes all three commands and the no-pass-no-progress gate deliberately reports the candidate as not fully qualified until they pass in an environment with npm dependencies installed:

```text
cd apps/web
npm install
npx playwright install chromium
npm run typecheck
npm run test
npm run test:e2e
```

The Playwright test covers:

```text
Launch
→ Detective Academy
→ ACADEMY_001
→ opening page 1
→ opening page 2
→ refresh and retain page 2
→ complete opening
→ empty Academy board
→ refresh and retain the same training case
```

`pytest-results.txt` contains the complete executed Python test output. `gate.json` is implementation evidence, not a formal Iteration 01 closure record, because `fully_qualified` remains `false` until the npm-backed checks pass.
