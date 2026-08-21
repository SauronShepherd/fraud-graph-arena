import pytest
from fraud_graph_arena.case_data.types import validate_sql_value

def test_typed_values_reject_invalid_scalars():
    with pytest.raises(ValueError): validate_sql_value("not-an-int", "INT", "sequence")
    with pytest.raises(ValueError): validate_sql_value("yes", "BOOLEAN", "directed")
    with pytest.raises(ValueError): validate_sql_value("not-decimal", "DECIMAL(18,8)", "weight")
