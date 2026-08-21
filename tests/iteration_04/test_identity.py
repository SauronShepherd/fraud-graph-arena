from fraud_graph_arena.case_data.identity import stable_id
def test_stable_id_is_deterministic_and_label_independent():
    assert stable_id('REC','case','people','42')==stable_id('REC','case','people','42')
    assert stable_id('REC','case','people','42')!=stable_id('REC','case','people','43')
