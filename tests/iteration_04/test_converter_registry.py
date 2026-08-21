from fraud_graph_arena.case_data.converters import registry
from fraud_graph_arena.case_data.validator import validate_package

def test_all_approved_families_have_registered_converters():
    assert registry.ids() == ("academy.csv.v1", "adult.csv.v1", "puppy.csv.v1", "senior.csv.v1")

def test_registered_converter_emits_a_valid_canonical_package(tmp_path):
    source = tmp_path / "source"; source.mkdir(); (source / "people.csv").write_text("id,name\n1,Hercule\n", encoding="utf-8")
    output = tmp_path / "package"
    registry.resolve("academy.csv.v1").convert(source, output, {"case_id": "CASE_1"})
    assert not validate_package(output)
