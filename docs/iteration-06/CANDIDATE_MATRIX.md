# FGA06 candidate matrix

This is the four-candidate OSS inventory before formal benchmark collection. Commercial graph components are deliberately excluded from this project scope: no commercial dependency, license obligation or vendor-specific production path is introduced.

| Candidate | Exact version | Local adapter | Hard requirements | Benchmark | License evidence | Decision |
|---|---|---|---|---|---|---|
| Cytoscape.js (normative incumbent) | 3.34.4 | Adapter + raw A/B run | Measured raw; interaction review pending | Raw report present | MIT; record source | BLOCKED_PENDING_QUALIFICATION |
| Sigma.js | 4.0.3 | Adapter + raw A/B run | Measured raw; interaction review pending | Raw report present | MIT; record source | NOT_QUALIFIED |
| D3 | 7.9.0 | Adapter + raw A/B run | Measured raw; interaction review pending | Raw report present | ISC; record source | NOT_QUALIFIED |
| React Flow (`@xyflow/react`) | 12.12.0 | Adapter + raw A/B run | Measured raw; interaction review pending | Raw report present | MIT; record source | NOT_QUALIFIED |
| Commercial graph component | Excluded by project scope | None | Not applicable | Not run | Not applicable | OUT_OF_SCOPE |

The dependency-free exhibit is a semantic baseline and fallback demonstration, not a renderer-selection result. A production renderer decision must remain blocked until the frozen requirements and performance envelope are measured honestly.
