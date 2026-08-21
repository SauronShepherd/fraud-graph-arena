from __future__ import annotations
SAFE_LAYERS={'published','genie'}
TRUTH_LAYERS={'truth'}
def safe_row(row: dict, *, layer: str) -> dict:
    if layer not in SAFE_LAYERS: raise ValueError('projection layer must be published or genie')
    forbidden={'entity_id','culpability','solve_gate','mastermind','guilty','scoring_rule','ending_rule'}
    return {k:v for k,v in row.items() if k.lower() not in forbidden and not k.lower().endswith('_truth')}
