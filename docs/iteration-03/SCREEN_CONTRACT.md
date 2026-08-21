# Screen contract

The screen set is versioned JSON. It describes identity, component family, public route metadata, a registered data source, lifecycle hook IDs, semantic action IDs, transition events/targets, effect IDs, history policy, and required safe context keys.

It cannot contain JavaScript, expressions, API URLs, component imports, CSS behavior selectors, arbitrary conditions, or custom animation code. Those capabilities are implemented by typed registries in `apps/web/src/screen-system`.

Lifecycle order is: validate definition, resolve URL, load the registered model with an abort signal, mount the family component, run entry focus/announcement, dispatch semantic actions, resolve the pure machine transition, run the registered exit effect, commit history, then load and enter the target.

`CASE_RESOLUTION` is registered as an internal reusable family with no public route and no production transition. I03 does not expose submission, evaluation, closing truth, evidence, credits, or ranked case content.
