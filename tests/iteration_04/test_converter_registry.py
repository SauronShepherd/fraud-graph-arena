from fraud_graph_arena.case_data.converters import registry

def test_all_approved_families_have_registered_converters():
    assert registry.ids() == ("academy.csv.v1", "adult.csv.v1", "puppy.csv.v1", "senior.csv.v1")
