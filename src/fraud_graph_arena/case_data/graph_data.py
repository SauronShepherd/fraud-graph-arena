from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class GraphNode:
    record_id: str
    record_type: str
    label: str
    safe_summary: str = ""
    record_subtype: str = ""
    source_system_id: str = ""
    provenance_ref: str = ""
@dataclass(frozen=True)
class GraphEdge:
    relationship_id: str
    source_record_id: str
    target_record_id: str
    relationship_family: str
    directed: bool
    provenance: str
    relationship_type: str = ""
    player_safe_summary: str = ""
    event_time: str = ""
def project_graph(records: list[dict], relationships: list[dict]) -> dict:
    record_ids = {record['record_id'] for record in records}
    if any(edge['source_record_id'] not in record_ids or edge['target_record_id'] not in record_ids for edge in relationships):
        raise ValueError('graph edge endpoint must resolve to a visible node')
    nodes=tuple(GraphNode(r['record_id'],r.get('record_type',''),r.get('display_label',''),r.get('safe_summary',''),r.get('record_subtype',''),r.get('source_system_id',''),r.get('provenance_ref','')) for r in sorted(records,key=lambda x:x['record_id']))
    edges=tuple(GraphEdge(r['relationship_id'],r['source_record_id'],r['target_record_id'],r.get('relationship_family',''),str(r.get('directed','')).lower()=='true',r.get('provenance',''),r.get('relationship_type',''),r.get('player_safe_summary',''),r.get('event_time','')) for r in sorted(relationships,key=lambda x:x['relationship_id']))
    return {'projection_version': '1', 'nodes':nodes,'edges':edges, 'node_count': len(nodes), 'edge_count': len(edges)}
