import json
from typing import List, Dict, Any
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from ddgs import DDGS
    except ImportError:
        from duckduckgo_search import DDGS
from playwright.sync_api import sync_playwright

def search_web(query: str, max_results: int = 5) -> str:
    """
    Perform a free web search query using DuckDuckGo to extract relevant URLs and snippets.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return f"No web search results found for query: '{query}'."
            
            formatted = []
            for idx, r in enumerate(results, 1):
                formatted.append(f"{idx}. Title: {r.get('title')}\n   URL: {r.get('href')}\n   Snippet: {r.get('body')}\n")
            return "\n".join(formatted)
    except Exception as e:
        return f"Search execution error for query '{query}': {str(e)}"

def browse_page(url: str) -> str:
    """
    Browse a specific target URL using Playwright headless browser to extract cleaned text/table contents.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            page.set_default_timeout(15000)
            
            page.goto(url, wait_until="domcontentloaded")
            
            # Allow dynamic content to stabilize briefly
            page.wait_for_timeout(2000)
            
            # Extract basic readable text blocks and clean out massive inline whitespace/scripts
            content = page.evaluate("""() => {
                // Remove scripts, styles, nav elements to isolate financial content
                const elementsToRemove = document.querySelectorAll('script, style, nav, footer, header, iframe');
                elementsToRemove.forEach(el => el.remove());
                return document.body.innerText;
            }""")
            
            browser.close()
            
            # Clean text by reducing repeated blank lines
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            cleaned_text = "\n".join(lines[:300])  # Return first 300 meaningful lines to keep LLM context clean
            return f"--- Scraped Content from {url} ---\n" + cleaned_text
    except Exception as e:
        return f"Browser extraction failed for URL '{url}': {str(e)}"

def get_tool_schemas() -> List[Dict[str, Any]]:
    """
    Export OpenAI compatible JSON schemas mapping available autonomous skills.
    Exposes web searching (discovery) alongside Playwright browser scraping (extraction).
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "search_web",
                "description": "Perform an organic web search to discover documentation URLs, latest quarterly result links, and financial articles.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The specific query string to search on the web (e.g., 'SUNPHARMA screener financial ratios' or 'TCS Q4 FY26 investor presentation')."
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "browse_page",
                "description": "Scrape and extract isolated readable markdown text from a targeted financial or documentation web page URL using a headless browser.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The absolute URL link to open and extract content from (e.g., financial parameters documentation pages)."
                        }
                    },
                    "required": ["url"]
                }
            }
        }
    ]
