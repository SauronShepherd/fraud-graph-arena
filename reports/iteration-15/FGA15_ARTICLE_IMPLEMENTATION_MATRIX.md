# FGA-15 article ↔ implementation matrix

This matrix is the editorial and technical coverage gate for `The World Around the Case`. Every article claim must point to a shipped implementation or be labelled as deferred scope; every shipped FGA-15 behaviour must be explained in the article.

| Article section / claim | Code or contract | Test / evidence | Status |
| --- | --- | --- | --- |
| Opening comic is a declared, skippable experience | `contracts/narrative/fga15-narrative.schema.json`; `narrative/manifest.py`; `OpeningComicPage.tsx` | manifest review; full Vitest; Playwright | Implemented |
| Captions, transcripts and alt text are first-class | `ComicPage`; narrative generator; opening and resolution pages | all 14 manifests; API media test; opening browser smoke | Implemented |
| Closing differs for excellent, partial and failed outcomes | `CLOSURE_VARIANTS`; resolution mapper; variant manifest fields | distinct-variant review; closing API media test; mapper path | Implemented |
| The visual layer is fictionalized and cannot become evidence | `fictionalization_statement`; schema boundary; page rendering | fictionalization-boundary review | Implemented |
| Audio has master/music/voice/effects buses | `apps/web/src/narrative/audio.ts`; `AudioControls.tsx` | audio Vitest | Implemented, optional audio only |
| Mute, persistence and reduced sensory mode | `fga.narrativeAudio.v1`; `AudioManager.update()`; controls | persistence/mute/reduced-sensory tests | Implemented |
| Autoplay, missing assets and concurrency fail visibly | `AudioManager.record()` and fallback events | missing/autoplay/suppression/stacking Vitest; opening fallback browser smoke | Implemented |
| No enabled asset may hide missing rights or provenance | narrative schema and validator; adversarial cases | local review script | Implemented |
| No unshipped audio is presented as available | generated catalog has disabled `NOT_SHIPPED` slots with null file refs | review report | Implemented |
| Existing case entry flow remains stable | generator preserves Academy's two original panels and one panel for other legacy cases | Playwright regression | Implemented |
| Full future 130-panel visual programme | master outline backlog | no production asset claim | Deferred explicitly |
| Production radio, music, effects and voice library | governance slots and fallbacks only | no enabled binary audio | Deferred explicitly |
| Databricks qualification | `scripts/qualify_fga15_narrative.py` | profile `fga` remote receipt at `reports/iteration-15/databricks-fga15-narrative-current.json` | Verified PASS on source commit `d051bba`; receipt committed in `aec14ee` |
