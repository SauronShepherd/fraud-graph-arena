-- Apply only in the approved disposable development catalog/schema.
-- The concrete principal names are deployment inputs, never package inputs.
-- Normal web serving may read safe published/genie projections only.
REVOKE ALL PRIVILEGES ON TABLE fga_truth_entities FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_claims FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_evidence_requirements FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_evidence_routes FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_allowed_alternatives FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_forbidden_conclusions FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_scoring_rules FROM `fga_web`;
REVOKE ALL PRIVILEGES ON TABLE fga_truth_ending_rules FROM `fga_web`;
GRANT SELECT ON TABLE fga_published_records TO `fga_web`;
GRANT SELECT ON TABLE fga_published_relationships TO `fga_web`;
GRANT SELECT ON TABLE fga_genie_records TO `fga_web`;
GRANT SELECT ON TABLE fga_genie_relationships TO `fga_web`;
