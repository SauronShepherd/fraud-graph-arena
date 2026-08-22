# FGA 04 compliance matrix

| Requirement | Authority | Implementation | Evidence boundary |
|---|---|---|---|
| 32-table inventory | `schema-registry.json` | `case_data.registry` | local/static |
| Physical mapping | `physical-registry.json` | `canonical_persistence.registry` | local/static |
| Identity and receipts | package contract | `CanonicalPackage`, manifest builder | local/static |
| Registered conversion | converter registry | `case_data.converters` | local/static |
| Typed validation | canonical registry | package validator/import preflight | local/reference |
| Truth firewall | `TRUTH_BOUNDARY.md` | validator/security modules | local/reference |
| Source provenance | source policy | provenance helpers and receipts | local/static |

Live Databricks qualification is a separate FGA 05 evidence boundary.
