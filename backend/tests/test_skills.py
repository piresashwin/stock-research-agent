from backend.agent.skills import get_tool_schemas, search_web, browse_page

def test_get_tool_schemas():
    schemas = get_tool_schemas()
    assert len(schemas) == 2
    names = [s["function"]["name"] for s in schemas]
    assert "search_web" in names
    assert "browse_page" in names

def test_search_web_empty_query():
    # Searching with completely empty/invalid syntax returns formatted execution error or empty message
    res = search_web("")
    assert isinstance(res, str)
    assert len(res) > 0

def test_browse_page_invalid_url():
    # Scraping invalid target URL catches browser exceptions cleanly
    res = browse_page("http://invalid.local.domain.test")
    assert "Browser extraction failed" in res or "error" in res.lower() or "failed" in res.lower()
