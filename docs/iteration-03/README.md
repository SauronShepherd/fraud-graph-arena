# FGA Iteration 03

Iteration 03 moves screen sequencing into a frontend-owned declarative runtime. JSON describes finite screen data and registered capability IDs; typed code owns loading, actions, routing, lifecycle, effects, and validation.

The current screen set is `LAUNCH → PATH_SELECTION → CASE_SELECTION → CASE_INTRODUCTION → INVESTIGATION_BOARD`. `CASE_RESOLUTION` is registered as an internal reusable type but is deliberately unreachable in production because submission and evaluation are not in scope.

Run the qualification slice with:

```text
python scripts/validate_screen_definitions.py
cd apps/web
npm run typecheck
npm run validate:screens
npm test
```

No evidence, graph analytics, credits, submissions, evaluator behavior, ranked content, or public case resolution is added by this iteration.
