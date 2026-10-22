from fraud_graph_arena.case_data.graph_data import project_graph
from fraud_graph_arena.case_data.projection_contract import safe_row
def test_graph_projection_is_renderer_neutral_and_preserves_semantics():
    graph=project_graph([{'record_id':'R2','record_type':'PERSON','display_label':'B'},{'record_id':'R1','record_type':'PERSON','display_label':'A'}],[{'relationship_id':'E1','source_record_id':'R1','target_record_id':'R2','relationship_family':'DIRECT_SOURCE','directed':'true','provenance':'source.csv#1'}])
    assert [n.record_id for n in graph['nodes']]==['R1','R2']; assert graph['edges'][0].relationship_family=='DIRECT_SOURCE'; assert graph['edges'][0].directed


def test_safe_projection_is_allowlisted_by_layer_table():
    projected=safe_row({'case_id':'C','record_id':'R','display_label':'Hercule','truth_hint':'answer'},layer='published',table='published/records.csv')
    assert projected=={'case_id':'C','record_id':'R','display_label':'Hercule'}


def test_safe_projection_rejects_truth_layer_and_mismatched_table():
    import pytest
    with pytest.raises(ValueError): safe_row({},layer='truth',table='truth/entities.csv')
    with pytest.raises(ValueError): safe_row({},layer='published',table='genie/records.csv')
