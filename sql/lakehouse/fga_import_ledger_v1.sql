-- FGA 05 operational ledger. Canonical table DDL is generated from the v1 registry.
CREATE TABLE IF NOT EXISTS fga_import_runs (
  import_run_id STRING NOT NULL, case_id STRING NOT NULL, case_version STRING NOT NULL,
  snapshot_version STRING NOT NULL, package_content_digest STRING NOT NULL,
  status STRING NOT NULL, retry_of STRING, error_code STRING, started_at_utc TIMESTAMP NOT NULL,
  finished_at_utc TIMESTAMP
);
CREATE TABLE IF NOT EXISTS fga_import_run_files (
  import_run_id STRING NOT NULL, relative_path STRING NOT NULL, byte_length BIGINT NOT NULL,
  sha256 STRING NOT NULL, observed_at_utc TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS fga_import_run_datasets (
  import_run_id STRING NOT NULL, dataset_path STRING NOT NULL, source_row_count BIGINT NOT NULL,
  staged_row_count BIGINT NOT NULL, validated_row_count BIGINT, phase STRING NOT NULL
);
CREATE TABLE IF NOT EXISTS fga_import_publications (
  publication_id STRING NOT NULL, case_id STRING NOT NULL, case_version STRING NOT NULL,
  snapshot_version STRING NOT NULL, canonical_model_version STRING NOT NULL,
  package_content_digest STRING NOT NULL, semantic_hash STRING, status STRING NOT NULL
);
CREATE TABLE IF NOT EXISTS fga_active_publications (
  case_id STRING NOT NULL, case_version STRING NOT NULL, snapshot_version STRING NOT NULL,
  active_publication_id STRING NOT NULL, activated_at_utc TIMESTAMP NOT NULL
);
