import pytest
from fraud_graph_arena.case_data.semantics import CONFIDENCE_BANDS, require_controlled

def test_controlled_confidence_values_are_jurisdiction_specific():
    require_controlled("HIGH", CONFIDENCE_BANDS, "confidence_band")
    with pytest.raises(ValueError): require_controlled("PROBABLE_FRAUD", CONFIDENCE_BANDS, "confidence_band")
