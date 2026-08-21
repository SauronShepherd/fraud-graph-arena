from __future__ import annotations
from .identity import stable_id
def relationship_id(case_id: str, family: str, source_record_id: str, target_record_id: str, direction='DIRECTED', provenance='') -> str:
    if direction == 'UNDIRECTED': source_record_id, target_record_id = sorted((source_record_id, target_record_id))
    return stable_id('REL', case_id, family, source_record_id, target_record_id, direction, provenance)
