from __future__ import annotations
SAFE_LAYERS={'published','genie'}
TRUTH_LAYERS={'truth'}
PROTECTED_TOKENS={'canonical_entity','culpability','solve_gate','mastermind','guilty','scoring_rule','ending_rule','expected_classification','protected_notes'}

def truth_leak_paths(value, path: str = "row") -> list[str]:
    """Recursively identify protected keys/sentinel values without exposing data."""
    leaks=[]
    if isinstance(value, dict):
        for key, child in value.items():
            key_text=str(key).lower()
            if any(token in key_text for token in PROTECTED_TOKENS) or key_text.endswith("_truth"):
                leaks.append(f"{path}.{key}")
            leaks.extend(truth_leak_paths(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value): leaks.extend(truth_leak_paths(child, f"{path}[{index}]"))
    elif isinstance(value, str):
        lowered=value.lower()
        if "do_not_show_hercule_this" in lowered: leaks.append(path)
    return leaks
def safe_row(row: dict, *, layer: str) -> dict:
    if layer not in SAFE_LAYERS: raise ValueError('projection layer must be published or genie')
    forbidden={'entity_id','culpability','solve_gate','mastermind','guilty','scoring_rule','ending_rule'}
    return {k:v for k,v in row.items() if k.lower() not in forbidden and not k.lower().endswith('_truth')}
