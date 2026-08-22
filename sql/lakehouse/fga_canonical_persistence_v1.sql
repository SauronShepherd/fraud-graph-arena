-- Generated from Canonical Model v1 registry. Do not hand-edit.
-- physical_registry_sha256: 7f6ccb4f84a3b54a339cf723a25f139c99613b56802d2fcbf9cc5fbf49c03540

CREATE TABLE IF NOT EXISTS fga_config_cases_csv (case_id STRING, short_id STRING, title STRING, path_code STRING, case_order INT, case_version STRING, snapshot_version STRING, mechanism STRING, currency_code STRING, base_asset STRING, generation_seed BIGINT, generation_mode STRING, ranked BOOLEAN, career_unlock BOOLEAN, disclaimer STRING, canonical_model_version STRING, _publication_id STRING, _load_run_id STRING); -- config/cases.csv

CREATE TABLE IF NOT EXISTS fga_config_case_profiles_csv (case_id STRING, profile_code STRING, profile_name STRING, cumulative BOOLEAN, starting_credits INT, manual_cost INT, zingg_cost INT, graphframes_cost INT, genie_cost INT, genie_row_limit INT, quote_required BOOLEAN, no_result_charged BOOLEAN, initial_item_count INT, description STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- config/case_profiles.csv

CREATE TABLE IF NOT EXISTS fga_config_case_initial_items_csv (case_id STRING, profile_code STRING, sequence INT, record_id STRING, reason_internal STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- config/case_initial_items.csv

CREATE TABLE IF NOT EXISTS fga_config_ui_contracts_csv (case_id STRING, semantic_name STRING, data_testid STRING, role STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- config/ui_contracts.csv

CREATE TABLE IF NOT EXISTS fga_config_registries_csv (case_id STRING, registry_type STRING, registry_key STRING, display_name STRING, properties_json STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- config/registries.csv

CREATE TABLE IF NOT EXISTS fga_config_reveal_steps_csv (case_id STRING, profile_code STRING, step_order INT, trigger_type STRING, trigger_value STRING, revealed_record_ids_json STRING, revealed_relationship_ids_json STRING, description_internal STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- config/reveal_steps.csv

CREATE TABLE IF NOT EXISTS fga_config_genie_benchmarks_csv (case_id STRING, profile_code STRING, benchmark_id STRING, prompt STRING, expected_columns_json STRING, expected_min_rows INT, expected_max_rows INT, expected_semantics STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- config/genie_benchmarks.csv

CREATE TABLE IF NOT EXISTS fga_authoring_records_csv (case_id STRING, record_id STRING, record_type STRING, record_subtype STRING, display_label STRING, source_system_id STRING, source_dataset STRING, source_record_key STRING, occurred_at TIMESTAMP, valid_from TIMESTAMP, valid_to TIMESTAMP, status STRING, summary STRING, attributes_json STRING, provenance_ref STRING, content_role STRING, source_payload_hash STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- authoring/records.csv

CREATE TABLE IF NOT EXISTS fga_authoring_record_attributes_csv (case_id STRING, record_id STRING, attribute_name STRING, attribute_type STRING, string_value STRING, integer_value BIGINT, decimal_value DECIMAL(38,10), boolean_value BOOLEAN, date_value DATE, timestamp_value TIMESTAMP, json_value STRING, is_sensitive BOOLEAN, is_masked BOOLEAN, ordinal INT, source_dataset STRING, source_column STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- authoring/record_attributes.csv

CREATE TABLE IF NOT EXISTS fga_authoring_relationships_csv (case_id STRING, relationship_id STRING, relationship_family STRING, relationship_type STRING, source_record_id STRING, target_record_id STRING, directed BOOLEAN, event_time TIMESTAMP, valid_from TIMESTAMP, valid_to TIMESTAMP, weight DECIMAL(18,8), supporting_record_ids_json STRING, summary STRING, provenance STRING, attributes_json STRING, content_role STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- authoring/relationships.csv

CREATE TABLE IF NOT EXISTS fga_analytics_entity_resolution_candidates_csv (case_id STRING, candidate_id STRING, left_record_id STRING, right_record_id STRING, entity_type STRING, confidence_band STRING, estimated_score DECIMAL(18,8), agreement_fields_json STRING, disagreement_fields_json STRING, missing_fields_json STRING, expected_truth STRING, generation_mode STRING, framework_semantics STRING, actual_engine_run BOOLEAN, authoring_method_version STRING, review_status STRING, provenance_note STRING, content_role STRING, metadata_json STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- analytics/entity_resolution_candidates.csv

CREATE TABLE IF NOT EXISTS fga_analytics_exact_matches_csv (case_id STRING, match_id STRING, rule_id STRING, relationship_type STRING, left_record_id STRING, right_record_id STRING, exact_field STRING, masked_exact_value STRING, normalization_version STRING, generation_mode STRING, framework_semantics STRING, actual_engine_run BOOLEAN, authoring_method_version STRING, review_status STRING, ambiguity_warning STRING, supporting_record_ids_json STRING, content_role STRING, metadata_json STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- analytics/exact_matches.csv

CREATE TABLE IF NOT EXISTS fga_analytics_tool_fixtures_csv (case_id STRING, profile_code STRING, fixture_id STRING, fixture_type STRING, tool_family STRING, selected_record_ids_json STRING, input_payload_json STRING, expected_result_count INT, expected_payload_json STRING, description STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- analytics/tool_fixtures.csv

CREATE TABLE IF NOT EXISTS fga_published_records_csv (case_id STRING, profile_code STRING, record_id STRING, record_type STRING, record_subtype STRING, display_label STRING, source_system_id STRING, occurred_at TIMESTAMP, status STRING, safe_summary STRING, safe_attributes_json STRING, provenance_ref STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- published/records.csv

CREATE TABLE IF NOT EXISTS fga_published_relationships_csv (case_id STRING, profile_code STRING, relationship_id STRING, relationship_family STRING, relationship_type STRING, source_record_id STRING, target_record_id STRING, directed BOOLEAN, event_time TIMESTAMP, weight DECIMAL(18,8), supporting_record_ids_json STRING, player_safe_summary STRING, provenance STRING, safe_attributes_json STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- published/relationships.csv

CREATE TABLE IF NOT EXISTS fga_published_entity_resolution_candidates_csv (case_id STRING, profile_code STRING, candidate_id STRING, left_record_id STRING, right_record_id STRING, entity_type STRING, confidence_band STRING, estimated_score DECIMAL(18,8), agreement_fields_json STRING, disagreement_fields_json STRING, missing_fields_json STRING, generation_mode STRING, framework_semantics STRING, actual_engine_run BOOLEAN, provenance_note STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- published/entity_resolution_candidates.csv

CREATE TABLE IF NOT EXISTS fga_published_exact_matches_csv (case_id STRING, profile_code STRING, match_id STRING, rule_id STRING, relationship_type STRING, left_record_id STRING, right_record_id STRING, exact_field STRING, masked_exact_value STRING, normalization_version STRING, generation_mode STRING, framework_semantics STRING, actual_engine_run BOOLEAN, ambiguity_warning STRING, supporting_record_ids_json STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- published/exact_matches.csv

CREATE TABLE IF NOT EXISTS fga_genie_records_csv (case_id STRING, profile_code STRING, record_id STRING, record_type STRING, record_subtype STRING, display_label STRING, source_system_id STRING, source_dataset STRING, source_record_key STRING, occurred_at TIMESTAMP, status STRING, safe_summary STRING, safe_attributes_json STRING, provenance_ref STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- genie/records.csv

CREATE TABLE IF NOT EXISTS fga_genie_record_attributes_csv (case_id STRING, profile_code STRING, record_id STRING, attribute_name STRING, attribute_type STRING, string_value STRING, integer_value BIGINT, decimal_value DECIMAL(38,10), boolean_value BOOLEAN, date_value DATE, timestamp_value TIMESTAMP, json_value STRING, is_masked BOOLEAN, ordinal INT, source_dataset STRING, source_column STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- genie/record_attributes.csv

CREATE TABLE IF NOT EXISTS fga_genie_relationships_csv (case_id STRING, profile_code STRING, relationship_id STRING, relationship_family STRING, relationship_type STRING, source_record_id STRING, target_record_id STRING, directed BOOLEAN, event_time TIMESTAMP, weight DECIMAL(18,8), supporting_record_ids_json STRING, safe_summary STRING, provenance STRING, safe_attributes_json STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- genie/relationships.csv

CREATE TABLE IF NOT EXISTS fga_truth_entities_csv (case_id STRING, entity_id STRING, entity_type STRING, canonical_name STRING, operational_role STRING, expected_classification STRING, culpability STRING, harm_status STRING, fraud_network_membership BOOLEAN, protected_notes STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- truth/entities.csv

CREATE TABLE IF NOT EXISTS fga_truth_claims_csv (case_id STRING, claim_id STRING, claim_type STRING, claim_text STRING, target_entity_id STRING, required BOOLEAN, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- truth/claims.csv

CREATE TABLE IF NOT EXISTS fga_truth_evidence_requirements_csv (case_id STRING, requirement_id STRING, claim_id STRING, target_entity_id STRING, evidence_family STRING, minimum_distinct_items INT, score_weight DECIMAL(18,8), required BOOLEAN, record_ids_json STRING, description STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- truth/evidence_requirements.csv

CREATE TABLE IF NOT EXISTS fga_truth_evidence_routes_csv (case_id STRING, route_id STRING, claim_id STRING, route_name STRING, step_order INT, evidence_reference STRING, tool_family STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- truth/evidence_routes.csv

CREATE TABLE IF NOT EXISTS fga_truth_allowed_alternatives_csv (case_id STRING, alternative_id STRING, claim_id STRING, alternative_description STRING, accepted_payload_json STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- truth/allowed_alternatives.csv

CREATE TABLE IF NOT EXISTS fga_truth_forbidden_conclusions_csv (case_id STRING, forbidden_id STRING, entity_id STRING, forbidden_conclusion STRING, penalty INT, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- truth/forbidden_conclusions.csv

CREATE TABLE IF NOT EXISTS fga_truth_scoring_rules_csv (case_id STRING, scoring_rule_id STRING, component STRING, max_points INT, score_weight DECIMAL(18,8), description STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- truth/scoring_rules.csv

CREATE TABLE IF NOT EXISTS fga_truth_ending_rules_csv (case_id STRING, ending_code STRING, priority INT, min_score INT, max_score INT, max_false_accusations INT, required_gates_json STRING, condition_expression STRING, description STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- truth/ending_rules.csv

CREATE TABLE IF NOT EXISTS fga_truth_test_scenarios_csv (case_id STRING, scenario_id STRING, title STRING, action_sequence_json STRING, submitted_suspects_json STRING, expected_score INT, expected_ending STRING, expected_credits_remaining INT, false_accusations INT, notes STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- truth/test_scenarios.csv

CREATE TABLE IF NOT EXISTS fga_truth_assertions_csv (case_id STRING, assertion_id STRING, assertion_type STRING, subject_record_id STRING, related_record_ids_json STRING, expected_value_json STRING, severity STRING, description STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- truth/assertions.csv

CREATE TABLE IF NOT EXISTS fga_validation_checks_csv (case_id STRING, check_id STRING, scope STRING, status STRING, details STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- validation/checks.csv

CREATE TABLE IF NOT EXISTS fga_validation_metrics_csv (case_id STRING, metric_name STRING, metric_value_decimal DECIMAL(38,10), metric_value_string STRING, dimensions_json STRING, status STRING, snapshot_version STRING, _publication_id STRING, _load_run_id STRING); -- validation/metrics.csv

-- Operational DDL: sql/lakehouse/fga_import_ledger_v1.sql
