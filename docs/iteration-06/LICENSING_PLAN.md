# FGA06 renderer licensing and supply-chain record

The executable comparison contains only redistributable open-source packages. Values below were read from the installed package metadata in `apps/web/node_modules` and cross-checked against the committed lockfile versions.

| Package | Exact version | Declared licence | Role | Current conclusion |
|---|---:|---|---|---|
| `cytoscape` | 3.34.4 | MIT | Normative incumbent | Compatible for OSS redistribution; retain source/reference review |
| `sigma` | 4.0.3 | MIT | Comparison candidate | Compatible for OSS redistribution; Graphology dependency must remain recorded |
| `graphology` | 0.26.0 | MIT | Sigma data dependency | Compatible for OSS redistribution |
| `d3` | 7.9.0 | ISC | Comparison candidate | Compatible for OSS redistribution |
| `@xyflow/react` | 12.12.0 | MIT | Comparison candidate | Compatible for OSS redistribution |

This table is not legal advice and is not a substitute for retaining the package license files in the final distribution. Before a production decision, record the package-manager lockfile, transitive license scan, attribution obligations and any extension-specific terms in the release evidence.

Commercial graph engines are intentionally not installed, benchmarked or bundled. A commercial product may be discussed as a total-cost/support reference, but it is not an executable finalist for this open-source, non-commercial branch.
