-- Apply only in the approved disposable development catalog/schema.
-- The concrete principal names are deployment inputs, never package inputs.
-- Normal web serving may read safe published/genie projections only.
REVOKE ALL PRIVILEGES ON TABLE fga_truth_entities_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_claims_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_evidence_requirements_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_evidence_routes_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_allowed_alternatives_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_forbidden_conclusions_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_scoring_rules_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_ending_rules_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_test_scenarios_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_assertions_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_authoring_records_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_authoring_record_attributes_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_authoring_relationships_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_analytics_entity_resolution_candidates_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_analytics_exact_matches_csv FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_analytics_tool_fixtures_csv FROM `fga_web`;
GRANT SELECT ON TABLE fga_published_records_csv TO `fga_web`;
GRANT SELECT ON TABLE fga_published_relationships_csv TO `fga_web`;
GRANT SELECT ON TABLE fga_published_entity_resolution_candidates_csv TO `fga_web`;
GRANT SELECT ON TABLE fga_published_exact_matches_csv TO `fga_web`;
GRANT SELECT ON TABLE fga_genie_records_csv TO `fga_web`;
GRANT SELECT ON TABLE fga_genie_record_attributes_csv TO `fga_web`;
GRANT SELECT ON TABLE fga_genie_relationships_csv TO `fga_web`;
