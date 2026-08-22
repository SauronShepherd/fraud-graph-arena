# FGA06 frozen renderer requirements

Hard requirements: semantic node styling, semantic relationship styling, stable node and edge IDs on selection, zoom/pan, fit/reset, preset positions, predictable resize, lifecycle cleanup, persistent details, project-owned semantic fallback, acceptable measured performance, production-suitable version, compatible license, and no renderer-native objects in application contracts.

The normative incumbent is Cytoscape.js. If it fails any hard requirement or the frozen performance envelope, the production decision is `BLOCKED - normative change required`; another renderer must not be silently substituted.
