from fraud_graph_arena.case_data.projection_contract import safe_row
def test_safe_projection_allowlist_drops_truth_fields():
    row=safe_row({'record_id':'R','display_label':'x','culpability':'guilty','mastermind':'E'},layer='published',table='published/records.csv')
    assert row=={'record_id':'R','display_label':'x'}
