from fraud_graph_arena.case_data.relationships import relationship_id
def test_undirected_relationship_ids_canonicalize_endpoint_order():
    assert relationship_id('C','SHARED','B','A','UNDIRECTED')==relationship_id('C','SHARED','A','B','UNDIRECTED')
def test_directed_relationships_preserve_direction():
    assert relationship_id('C','OWNS','A','B')!=relationship_id('C','OWNS','B','A')
