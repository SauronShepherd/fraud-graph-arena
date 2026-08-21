from pathlib import Path

ROOT = Path(__file__).parents[2]
PAGES = ROOT / "apps/web/src/pages"

def test_pages_do_not_own_router_navigation_or_api_calls():
    forbidden = ("useNavigate", "<Routes", "<Route", "window.location", "fetch(", "../api/client")
    violations = []
    for path in PAGES.glob("*.tsx"):
        text = path.read_text(encoding="utf-8")
        for token in forbidden:
            if token in text:
                violations.append(f"{path}:{token}")
    assert violations == []

def test_app_does_not_define_route_tree():
    text = (ROOT / "apps/web/src/App.tsx").read_text(encoding="utf-8")
    assert "<Routes" not in text
    assert "<Route" not in text
