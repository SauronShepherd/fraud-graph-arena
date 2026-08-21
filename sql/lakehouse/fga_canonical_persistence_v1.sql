-- Generated from Canonical Model v1 registry. Do not hand-edit.

CREATE TABLE IF NOT EXISTS fga_config_cases_csv (case_id STRING, short_id STRING, title STRING, path_code STRING, case_order STRING, case_version STRING, snapshot_version STRING, mechanism STRING, currency_code STRING, base_asset STRING, generation_seed STRING, generation_mode STRING, ranked STRING, career_unlock STRING, disclaimer STRING, canonical_model_version STRING); -- config/cases.csv

CREATE TABLE IF NOT EXISTS fga_config_case_profiles_csv (case_id STRING, profile_code STRING, profile_name STRING, cumulative STRING, starting_credits STRING, manual_cost STRING, zingg_cost STRING, graphframes_cost STRING, genie_cost STRING, genie_row_limit STRING, quote_required STRING, no_result_charged STRING, initial_item_count STRING, description STRING, snapshot_version STRING); -- config/case_profiles.csv

CREATE TABLE IF NOT EXISTS fga_config_case_initial_items_csv (case_id STRING, profile_code STRING, sequence STRING, record_id STRING, reason_internal STRING, snapshot_version STRING); -- config/case_initial_items.csv

CREATE TABLE IF NOT EXISTS fga_config_ui_contracts_csv (case_id STRING, semantic_name STRING, data_testid STRING, role STRING, snapshot_version STRING); -- config/ui_contracts.csv

CREATE TABLE IF NOT EXISTS fga_config_registries_csv (case_id STRING, registry_type STRING, registry_key STRING, display_name STRING, properties_json STRING, snapshot_version STRING); -- config/registries.csv

CREATE TABLE IF NOT EXISTS fga_config_reveal_steps_csv (case_id STRING, profile_code STRING, step_order STRING, trigger_type STRING, trigger_value STRING, revealed_record_ids_json STRING, revealed_relationship_ids_json STRING, description_internal STRING, snapshot_version STRING); -- config/reveal_steps.csv

CREATE TABLE IF NOT EXISTS fga_config_genie_benchmarks_csv (case_id STRING, profile_code STRING, benchmark_id STRING, prompt STRING, expected_columns_json STRING, expected_min_rows STRING, expected_max_rows STRING, expected_semantics STRING, snapshot_version STRING); -- config/genie_benchmarks.csv

CREATE TABLE IF NOT EXISTS fga_authoring_records_csv (case_id STRING, record_id STRING, record_type STRING, record_subtype STRING, display_label STRING, source_system_id STRING, source_dataset STRING, source_record_key STRING, occurred_at STRING, valid_from STRING, valid_to STRING, status STRING, summary STRING, attributes_json STRING, provenance_ref STRING, content_role STRING, source_payload_hash STRING, snapshot_version STRING); -- authoring/records.csv

CREATE TABLE IF NOT EXISTS fga_authoring_record_attributes_csv (case_id STRING, record_id STRING, attribute_name STRING, attribute_type STRING, string_value STRING, integer_value STRING, decimal_value STRING, boolean_value STRING, date_value STRING, timestamp_value STRING, json_value STRING, is_sensitive STRING, is_masked STRING, ordinal STRING, source_dataset STRING, source_column STRING, snapshot_version STRING); -- authoring/record_attributes.csv

CREATE TABLE IF NOT EXISTS fga_authoring_relationships_csv (case_id STRING, relationship_id STRING, relationship_family STRING, relationship_type STRING, source_record_id STRING, target_record_id STRING, directed STRING, event_time STRING, valid_from STRING, valid_to STRING, weight STRING, supporting_record_ids_json STRING, summary STRING, provenance STRING, attributes_json STRING, content_role STRING, snapshot_version STRING); -- authoring/relationships.csv

CREATE TABLE IF NOT EXISTS fga_analytics_entity_resolution_candidates_csv (case_id STRING, candidate_id STRING, left_record_id STRING, right_record_id STRING, entity_type STRING, confidence_band STRING, estimated_score STRING, agreement_fields_json STRING, disagreement_fields_json STRING, missing_fields_json STRING, expected_truth STRING, generation_mode STRING, framework_semantics STRING, actual_engine_run STRING, authoring_method_version STRING, review_status STRING, provenance_note STRING, content_role STRING, metadata_json STRING, snapshot_version STRING); -- analytics/entity_resolution_candidates.csv

CREATE TABLE IF NOT EXISTS fga_analytics_exact_matches_csv (case_id STRING, match_id STRING, rule_id STRING, relationship_type STRING, left_record_id STRING, right_record_id STRING, exact_field STRING, masked_exact_value STRING, normalization_version STRING, generation_mode STRING, framework_semantics STRING, actual_engine_run STRING, authoring_method_version STRING, review_status STRING, ambiguity_warning STRING, supporting_record_ids_json STRING, content_role STRING, metadata_json STRING, snapshot_version STRING); -- analytics/exact_matches.csv

CREATE TABLE IF NOT EXISTS fga_analytics_tool_fixtures_csv (case_id STRING, profile_code STRING, fixture_id STRING, fixture_type STRING, tool_family STRING, selected_record_ids_json STRING, input_payload_json STRING, expected_result_count STRING, expected_payload_json STRING, description STRING, snapshot_version STRING); -- analytics/tool_fixtures.csv

CREATE TABLE IF NOT EXISTS fga_published_records_csv (case_id STRING, profile_code STRING, record_id STRING, record_type STRING, record_subtype STRING, display_label STRING, source_system_id STRING, occurred_at STRING, status STRING, safe_summary STRING, safe_attributes_json STRING, provenance_ref STRING, snapshot_version STRING); -- published/records.csv

CREATE TABLE IF NOT EXISTS fga_published_relationships_csv (case_id STRING, profile_code STRING, relationship_id STRING, relationship_family STRING, relationship_type STRING, source_record_id STRING, target_record_id STRING, directed STRING, event_time STRING, weight STRING, supporting_record_ids_json STRING, player_safe_summary STRING, provenance STRING, safe_attributes_json STRING, snapshot_version STRING); -- published/relationships.csv

CREATE TABLE IF NOT EXISTS fga_published_entity_resolution_candidates_csv (case_id STRING, profile_code STRING, candidate_id STRING, left_record_id STRING, right_record_id STRING, entity_type STRING, confidence_band STRING, estimated_score STRING, agreement_fields_json STRING, disagreement_fields_json STRING, missing_fields_json STRING, generation_mode STRING, framework_semantics STRING, actual_engine_run STRING, provenance_note STRING, snapshot_version STRING); -- published/entity_resolution_candidates.csv

CREATE TABLE IF NOT EXISTS fga_published_exact_matches_csv (case_id STRING, profile_code STRING, match_id STRING, rule_id STRING, relationship_type STRING, left_record_id STRING, right_record_id STRING, exact_field STRING, masked_exact_value STRING, normalization_version STRING, generation_mode STRING, framework_semantics STRING, actual_engine_run STRING, ambiguity_warning STRING, supporting_record_ids_json STRING, snapshot_version STRING); -- published/exact_matches.csv

CREATE TABLE IF NOT EXISTS fga_genie_records_csv (case_id STRING, profile_code STRING, record_id STRING, record_type STRING, record_subtype STRING, display_label STRING, source_system_id STRING, source_dataset STRING, source_record_key STRING, occurred_at STRING, status STRING, safe_summary STRING, safe_attributes_json STRING, provenance_ref STRING, snapshot_version STRING); -- genie/records.csv

CREATE TABLE IF NOT EXISTS fga_genie_record_attributes_csv (case_id STRING, profile_code STRING, record_id STRING, attribute_name STRING, attribute_type STRING, string_value STRING, integer_value STRING, decimal_value STRING, boolean_value STRING, date_value STRING, timestamp_value STRING, json_value STRING, is_masked STRING, ordinal STRING, source_dataset STRING, source_column STRING, snapshot_version STRING); -- genie/record_attributes.csv

CREATE TABLE IF NOT EXISTS fga_genie_relationships_csv (case_id STRING, profile_code STRING, relationship_id STRING, relationship_family STRING, relationship_type STRING, source_record_id STRING, target_record_id STRING, directed STRING, event_time STRING, weight STRING, supporting_record_ids_json STRING, safe_summary STRING, provenance STRING, safe_attributes_json STRING, snapshot_version STRING); -- genie/relationships.csv

CREATE TABLE IF NOT EXISTS fga_truth_entities_csv (case_id STRING, entity_id STRING, entity_type STRING, canonical_name STRING, operational_role STRING, expected_classification STRING, culpability STRING, harm_status STRING, fraud_network_membership STRING, protected_notes STRING, snapshot_version STRING); -- truth/entities.csv

CREATE TABLE IF NOT EXISTS fga_truth_claims_csv (case_id STRING, claim_id STRING, claim_type STRING, claim_text STRING, target_entity_id STRING, required STRING, snapshot_version STRING); -- truth/claims.csv

CREATE TABLE IF NOT EXISTS fga_truth_evidence_requirements_csv (case_id STRING, requirement_id STRING, claim_id STRING, target_entity_id STRING, evidence_family STRING, minimum_distinct_items STRING, score_weight STRING, required STRING, record_ids_json STRING, description STRING, snapshot_version STRING); -- truth/evidence_requirements.csv

CREATE TABLE IF NOT EXISTS fga_truth_evidence_routes_csv (case_id STRING, route_id STRING, claim_id STRING, route_name STRING, step_order STRING, evidence_reference STRING, tool_family STRING, snapshot_version STRING); -- truth/evidence_routes.csv

CREATE TABLE IF NOT EXISTS fga_truth_allowed_alternatives_csv (case_id STRING, alternative_id STRING, claim_id STRING, alternative_description STRING, accepted_payload_json STRING, snapshot_version STRING); -- truth/allowed_alternatives.csv

CREATE TABLE IF NOT EXISTS fga_truth_forbidden_conclusions_csv (case_id STRING, forbidden_id STRING, entity_id STRING, forbidden_conclusion STRING, penalty STRING, snapshot_version STRING); -- truth/forbidden_conclusions.csv

CREATE TABLE IF NOT EXISTS fga_truth_scoring_rules_csv (case_id STRING, scoring_rule_id STRING, component STRING, max_points STRING, score_weight STRING, description STRING, snapshot_version STRING); -- truth/scoring_rules.csv

CREATE TABLE IF NOT EXISTS fga_truth_ending_rules_csv (case_id STRING, ending_code STRING, priority STRING, min_score STRING, max_score STRING, max_false_accusations STRING, required_gates_json STRING, condition_expression STRING, description STRING, snapshot_version STRING); -- truth/ending_rules.csv

CREATE TABLE IF NOT EXISTS fga_truth_test_scenarios_csv (case_id STRING, scenario_id STRING, title STRING, action_sequence_json STRING, submitted_suspects_json STRING, expected_score STRING, expected_ending STRING, expected_credits_remaining STRING, false_accusations STRING, notes STRING, snapshot_version STRING); -- truth/test_scenarios.csv

CREATE TABLE IF NOT EXISTS fga_truth_assertions_csv (case_id STRING, assertion_id STRING, assertion_type STRING, subject_record_id STRING, related_record_ids_json STRING, expected_value_json STRING, severity STRING, description STRING, snapshot_version STRING); -- truth/assertions.csv

CREATE TABLE IF NOT EXISTS fga_validation_checks_csv (case_id STRING, check_id STRING, scope STRING, status STRING, details STRING, snapshot_version STRING); -- validation/checks.csv

CREATE TABLE IF NOT EXISTS fga_validation_metrics_csv (case_id STRING, metric_name STRING, metric_value_decimal STRING, metric_value_string STRING, dimensions_json STRING, status STRING, snapshot_version STRING); -- validation/metrics.csv

-- Operational DDL: sql/lakehouse/fga_import_ledger_v1.sql
