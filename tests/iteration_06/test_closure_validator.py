from scripts.validate_iteration_06_closure import validate_evidence_scope


def test_fga06_scope_accepts_cumulative_descendant_changes():
    assert validate_evidence_scope(["reports/iteration-06/closure.json", "src/fraud_graph_arena/web/api_models.py"]) == []


def test_fga06_scope_requires_evidence_path():
    assert validate_evidence_scope(["src/fraud_graph_arena/web/api_models.py"]) == [
        "source/evidence range does not contain FGA06 evidence files"
    ]


def test_fga06_scope_rejects_empty_range():
    assert validate_evidence_scope([]) == ["source/evidence range contains no changed files"]
