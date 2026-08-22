-- Generated active-pointer serving views. Do not hand-edit.

CREATE OR REPLACE VIEW fga_active_published_records_csv AS SELECT source.* FROM fga_published_records_csv AS source JOIN fga_active_publications AS active ON source.case_id = active.case_id AND source.case_version = active.case_version AND source._publication_id = active.active_publication_id; -- published/records.csv

CREATE OR REPLACE VIEW fga_active_published_relationships_csv AS SELECT source.* FROM fga_published_relationships_csv AS source JOIN fga_active_publications AS active ON source.case_id = active.case_id AND source.case_version = active.case_version AND source._publication_id = active.active_publication_id; -- published/relationships.csv

CREATE OR REPLACE VIEW fga_active_published_entity_resolution_candidates_csv AS SELECT source.* FROM fga_published_entity_resolution_candidates_csv AS source JOIN fga_active_publications AS active ON source.case_id = active.case_id AND source.case_version = active.case_version AND source._publication_id = active.active_publication_id; -- published/entity_resolution_candidates.csv

CREATE OR REPLACE VIEW fga_active_published_exact_matches_csv AS SELECT source.* FROM fga_published_exact_matches_csv AS source JOIN fga_active_publications AS active ON source.case_id = active.case_id AND source.case_version = active.case_version AND source._publication_id = active.active_publication_id; -- published/exact_matches.csv

CREATE OR REPLACE VIEW fga_active_genie_records_csv AS SELECT source.* FROM fga_genie_records_csv AS source JOIN fga_active_publications AS active ON source.case_id = active.case_id AND source.case_version = active.case_version AND source._publication_id = active.active_publication_id; -- genie/records.csv

CREATE OR REPLACE VIEW fga_active_genie_record_attributes_csv AS SELECT source.* FROM fga_genie_record_attributes_csv AS source JOIN fga_active_publications AS active ON source.case_id = active.case_id AND source.case_version = active.case_version AND source._publication_id = active.active_publication_id; -- genie/record_attributes.csv

CREATE OR REPLACE VIEW fga_active_genie_relationships_csv AS SELECT source.* FROM fga_genie_relationships_csv AS source JOIN fga_active_publications AS active ON source.case_id = active.case_id AND source.case_version = active.case_version AND source._publication_id = active.active_publication_id; -- genie/relationships.csv
