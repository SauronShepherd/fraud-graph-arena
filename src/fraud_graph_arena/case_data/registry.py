from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
CONTRACT=ROOT/'contracts/canonical/v1/canonical-model.json'
TABLE_PATHS=tuple(json.loads(CONTRACT.read_text(encoding='utf-8'))['tables'])
_HEADERS={
'config/cases.csv':'case_id,short_id,title,path_code,case_order,case_version,snapshot_version,mechanism,currency_code,base_asset,generation_seed,generation_mode,ranked,career_unlock,disclaimer,canonical_model_version',
'config/case_profiles.csv':'case_id,profile_code,profile_name,cumulative,starting_credits,manual_cost,zingg_cost,graphframes_cost,genie_cost,genie_row_limit,quote_required,no_result_charged,initial_item_count,description,snapshot_version',
'config/case_initial_items.csv':'case_id,profile_code,sequence,record_id,reason_internal,snapshot_version',
'config/ui_contracts.csv':'case_id,semantic_name,data_testid,role,snapshot_version',
'config/registries.csv':'case_id,registry_type,registry_key,display_name,properties_json,snapshot_version',
'config/reveal_steps.csv':'case_id,profile_code,step_order,trigger_type,trigger_value,revealed_record_ids_json,revealed_relationship_ids_json,description_internal,snapshot_version',
'config/genie_benchmarks.csv':'case_id,profile_code,benchmark_id,prompt,expected_columns_json,expected_min_rows,expected_max_rows,expected_semantics,snapshot_version',
'authoring/records.csv':'case_id,record_id,record_type,record_subtype,display_label,source_system_id,source_dataset,source_record_key,occurred_at,valid_from,valid_to,status,summary,attributes_json,provenance_ref,content_role,source_payload_hash,snapshot_version',
'authoring/record_attributes.csv':'case_id,record_id,attribute_name,attribute_type,string_value,integer_value,decimal_value,boolean_value,date_value,timestamp_value,json_value,is_sensitive,is_masked,ordinal,source_dataset,source_column,snapshot_version',
'authoring/relationships.csv':'case_id,relationship_id,relationship_family,relationship_type,source_record_id,target_record_id,directed,event_time,valid_from,valid_to,weight,supporting_record_ids_json,summary,provenance,attributes_json,content_role,snapshot_version',
'analytics/entity_resolution_candidates.csv':'case_id,candidate_id,left_record_id,right_record_id,entity_type,confidence_band,estimated_score,agreement_fields_json,disagreement_fields_json,missing_fields_json,expected_truth,generation_mode,framework_semantics,actual_engine_run,authoring_method_version,review_status,provenance_note,content_role,metadata_json,snapshot_version',
'analytics/exact_matches.csv':'case_id,match_id,rule_id,relationship_type,left_record_id,right_record_id,exact_field,masked_exact_value,normalization_version,generation_mode,framework_semantics,actual_engine_run,authoring_method_version,review_status,ambiguity_warning,supporting_record_ids_json,content_role,metadata_json,snapshot_version',
'analytics/tool_fixtures.csv':'case_id,profile_code,fixture_id,fixture_type,tool_family,selected_record_ids_json,input_payload_json,expected_result_count,expected_payload_json,description,snapshot_version',
'published/records.csv':'case_id,profile_code,record_id,record_type,record_subtype,display_label,source_system_id,occurred_at,status,safe_summary,safe_attributes_json,provenance_ref,snapshot_version',
'published/relationships.csv':'case_id,profile_code,relationship_id,relationship_family,relationship_type,source_record_id,target_record_id,directed,event_time,weight,supporting_record_ids_json,player_safe_summary,provenance,safe_attributes_json,snapshot_version',
'published/entity_resolution_candidates.csv':'case_id,profile_code,candidate_id,left_record_id,right_record_id,entity_type,confidence_band,estimated_score,agreement_fields_json,disagreement_fields_json,missing_fields_json,generation_mode,framework_semantics,actual_engine_run,provenance_note,snapshot_version',
'published/exact_matches.csv':'case_id,profile_code,match_id,rule_id,relationship_type,left_record_id,right_record_id,exact_field,masked_exact_value,normalization_version,generation_mode,framework_semantics,actual_engine_run,ambiguity_warning,supporting_record_ids_json,snapshot_version',
'genie/records.csv':'case_id,profile_code,record_id,record_type,record_subtype,display_label,source_system_id,source_dataset,source_record_key,occurred_at,status,safe_summary,safe_attributes_json,provenance_ref,snapshot_version',
'genie/record_attributes.csv':'case_id,profile_code,record_id,attribute_name,attribute_type,string_value,integer_value,decimal_value,boolean_value,date_value,timestamp_value,json_value,is_masked,ordinal,source_dataset,source_column,snapshot_version',
'genie/relationships.csv':'case_id,profile_code,relationship_id,relationship_family,relationship_type,source_record_id,target_record_id,directed,event_time,weight,supporting_record_ids_json,safe_summary,provenance,safe_attributes_json,snapshot_version',
'truth/entities.csv':'case_id,entity_id,entity_type,canonical_name,operational_role,expected_classification,culpability,harm_status,fraud_network_membership,protected_notes,snapshot_version',
'truth/claims.csv':'case_id,claim_id,claim_type,claim_text,target_entity_id,required,snapshot_version',
'truth/evidence_requirements.csv':'case_id,requirement_id,claim_id,target_entity_id,evidence_family,minimum_distinct_items,score_weight,required,record_ids_json,description,snapshot_version',
'truth/evidence_routes.csv':'case_id,route_id,claim_id,route_name,step_order,evidence_reference,tool_family,snapshot_version',
'truth/allowed_alternatives.csv':'case_id,alternative_id,claim_id,alternative_description,accepted_payload_json,snapshot_version',
'truth/forbidden_conclusions.csv':'case_id,forbidden_id,entity_id,forbidden_conclusion,penalty,snapshot_version',
'truth/scoring_rules.csv':'case_id,scoring_rule_id,component,max_points,score_weight,description,snapshot_version',
'truth/ending_rules.csv':'case_id,ending_code,priority,min_score,max_score,max_false_accusations,required_gates_json,condition_expression,description,snapshot_version',
'truth/test_scenarios.csv':'case_id,scenario_id,title,action_sequence_json,submitted_suspects_json,expected_score,expected_ending,expected_credits_remaining,false_accusations,notes,snapshot_version',
'truth/assertions.csv':'case_id,assertion_id,assertion_type,subject_record_id,related_record_ids_json,expected_value_json,severity,description,snapshot_version',
'validation/checks.csv':'case_id,check_id,scope,status,details,snapshot_version',
'validation/metrics.csv':'case_id,metric_name,metric_value_decimal,metric_value_string,dimensions_json,status,snapshot_version'}
def headers(path: str)->tuple[str,...]: return tuple(_HEADERS[path].split(','))
def load_registry()->dict[str,tuple[str,...]]: return {p:headers(p) for p in TABLE_PATHS}

@lru_cache(maxsize=1)
def load_typed_registry() -> dict[str, dict]:
    """Load the checked-in typed Canonical Model v1 registry artifact."""
    packages = sorted((ROOT / "case-data/canonical/v1").glob("*/fga_canonical_schema_registry_v1.json"))
    if not packages:
        raise FileNotFoundError("typed canonical registry artifact is missing")
    data = json.loads(packages[0].read_text(encoding="utf-8"))
    if set(data.get("tables", {})) != set(TABLE_PATHS):
        raise ValueError("typed canonical registry does not define exactly 32 tables")
    return data["tables"]

def sql_types(path: str) -> tuple[str, ...]:
    return tuple(column["sql_type"] for column in load_typed_registry()[path]["columns"])
