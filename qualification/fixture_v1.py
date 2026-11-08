from __future__ import annotations

import hashlib
import json
from pathlib import Path


def build_fixture() -> dict:
    node_specs = [
        ("PERSON_RECORD", "J. García", 120, 260, "CANDIDATE", "◉", "northstar"),
        ("ORGANIZATION_RECORD", "Northstar Imports", 330, 190, "INVESTIGATED", "▦", "northstar"),
        ("PERSON_RECORD", "M. Silva", 100, 100, "CANDIDATE", "◉", "northstar"),
        ("ORGANIZATION_RECORD", "Blue Harbor LLC", 560, 110, "UNINVESTIGATED", "▦", "harbor"),
        ("DEVICE_RECORD", "Device 14", 300, 360, "INVESTIGATED", "⌁", "northstar"),
        ("EMAIL_RECORD", "Raven mailbox", 510, 350, "UNINVESTIGATED", "@", "orbit"),
        ("ADDRESS_RECORD", "Cedar address", 80, 470, "DISCARDED", "⌂", "neutral"),
        ("MERCHANT_RECORD", "Orbit Merchant", 760, 245, "FRAUD_CONFIRMED", "$", "orbit"),
        ("PERSON_RECORD", "L. Costa", 180, 500, "INVESTIGATED", "◉", "harbor"),
        ("ORGANIZATION_RECORD", "Eastline Bank", 760, 90, "UNINVESTIGATED", "▦", "orbit"),
        ("DEVICE_RECORD", "Shared phone 42", 410, 260, "CANDIDATE", "⌁", "northstar"),
        ("ORGANIZATION_RECORD", "Northstar Cashbox", 480, 480, "DISCARDED", "▦", "northstar"),
        ("PERSON_RECORD", "G. Romero", 620, 470, "UNINVESTIGATED", "◉", "harbor"),
        ("DEVICE_RECORD", "Pine VPN", 690, 360, "CANDIDATE", "⌁", "harbor"),
        ("ADDRESS_RECORD", "Parcel locker 7", 250, 80, "INVESTIGATED", "⌂", "northstar"),
        ("ORGANIZATION_RECORD", "Vega Payments", 620, 220, "FRAUD_CONFIRMED", "▦", "orbit"),
        ("PERSON_RECORD", "D. Ferrer", 420, 70, "CANDIDATE", "◉", "harbor"),
        ("ACCOUNT_RECORD", "Harbor account", 820, 460, "INVESTIGATED", "◈", "harbor"),
    ]
    nodes = [{"id": f"FIX-N-{index:04d}", "record_type": record_type, "label": label, "x": x, "y": y, "investigation_status": status, "icon": icon, "cluster_id": cluster} for index, (record_type, label, x, y, status, icon, cluster) in enumerate(node_specs)]
    edge_specs = [
        (0, 1, "DIRECT_SOURCE", "DIRECTOR_OF", "documented"), (0, 4, "DEVICE_OBSERVATION", "LOGGED_IN_AS", "high"),
        (1, 3, "DIRECT_SOURCE", "CONTROLS", "documented"), (1, 9, "TRANSACTIONAL", "PAYS", "medium"),
        (2, 10, "DEVICE_OBSERVATION", "USES_DEVICE", "medium"), (10, 4, "SHARED_ATTRIBUTE", "SHARES_DEVICE", "high"),
        (4, 5, "DIRECT_SOURCE", "OBSERVED_WITH", "documented"), (5, 1, "SHARED_ATTRIBUTE", "ASSOCIATED_WITH", "medium"),
        (2, 7, "TRANSACTIONAL", "TRANSACTS_WITH", "medium"), (7, 9, "TRANSACTIONAL", "SETTLED_BY", "high"),
        (8, 7, "TRANSACTIONAL", "TRANSACTS_WITH", "medium"), (8, 14, "DIRECT_SOURCE", "USES_ADDRESS", "documented"),
        (14, 3, "DIRECT_SOURCE", "SHIPS_TO", "documented"), (3, 11, "DIRECT_SOURCE", "AFFILIATED_WITH", "documented"),
        (11, 1, "TRANSACTIONAL", "ROUTES_TO", "medium"), (12, 13, "DEVICE_OBSERVATION", "USES_DEVICE", "medium"),
        (13, 10, "SHARED_ATTRIBUTE", "ROUTES_THROUGH", "low"), (15, 9, "TRANSACTIONAL", "SETTLES_WITH", "high"),
        (15, 16, "SHARED_ATTRIBUTE", "LINKED_TO", "medium"), (16, 17, "TRANSACTIONAL", "USES_ACCOUNT", "medium"),
        (17, 3, "TRANSACTIONAL", "FUNDS", "high"), (0, 2, "SHARED_ATTRIBUTE", "POTENTIAL_MATCH", "low"),
        (1, 15, "TRANSACTIONAL", "TRANSFERS_TO", "high"), (7, 15, "SHARED_ATTRIBUTE", "SHARES_BENEFICIARY", "medium"),
        (6, 8, "DIRECT_SOURCE", "PREVIOUS_ADDRESS", "documented"), (12, 17, "TRANSACTIONAL", "AUTHORISED_BY", "low"),
    ]
    edges = [{"id": f"FIX-E-{index:04d}", "source_id": f"FIX-N-{source:04d}", "target_id": f"FIX-N-{target:04d}", "relationship_family": family, "relationship_type": relationship_type, "directed": True, "confidence": confidence} for index, (source, target, family, relationship_type, confidence) in enumerate(edge_specs)]
    return {"fixture_version": "1", "nodes": nodes, "edges": edges}


def write_fixture(path: Path) -> str:
    payload = json.dumps(build_fixture(), sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
    path.write_text(payload, encoding="utf-8")
    return hashlib.sha256(payload.encode()).hexdigest()


if __name__ == "__main__":
    output = Path(__file__).with_name("fixture-v1.json")
    print(write_fixture(output))
