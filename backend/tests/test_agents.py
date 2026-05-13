import json
from backend.agent.researcher import get_template_content
from backend.agent.evaluator import get_checklist_content

def test_template_content_loading():
    content = get_template_content()
    assert isinstance(content, str)
    assert len(content) > 0
    assert "SECTION 1" in content or "Stock" in content

def test_checklist_content_loading():
    content = get_checklist_content()
    assert isinstance(content, str)
    assert len(content) > 0
    assert "QUALITY METRICS" in content or "Checklist" in content
