# FGA 04 requirements

The canonical contract is a fixed 32-table Canonical Model v1 package. Every package has one case identity (`case_id`, `case_version`, `snapshot_version`), one supported model version, deterministic receipts, and an explicit family/profile. Conversion is performed only by a registered source adapter. Validation covers ordered headers, types, nullability, receipts, identity, relational integrity, controlled values, and the truth firewall.

Authoritative artifacts are the canonical model, typed schema registry, physical registry, and package validator.
