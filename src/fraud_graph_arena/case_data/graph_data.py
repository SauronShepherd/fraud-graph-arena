from __future__ import annotations
from dataclasses import dataclass
from .identity import stable_id
@dataclass(frozen=True)
class GraphNode:
    record_id: str
    record_type: str
    label: str
@dataclass(frozen=True)
class GraphEdge:
    relationship_id: str
    source_record_id: str
    target_record_id: str
    relationship_family: str
    directed: bool
    provenance: str
def project_graph(records: list[dict], relationships: list[dict]) -> dict:
    nodes=tuple(GraphNode(r['record_id'],r.get('record_type',''),r.get('display_label','')) for r in sorted(records,key=lambda x:x['record_id']))
    edges=tuple(GraphEdge(r['relationship_id'],r['source_record_id'],r['target_record_id'],r.get('relationship_family',''),str(r.get('directed','')).lower()=='true',r.get('provenance','')) for r in sorted(relationships,key=lambda x:x['relationship_id']))
    return {'nodes':nodes,'edges':edges}
