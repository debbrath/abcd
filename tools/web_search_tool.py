# tools/web_search_tool.py
import os
import requests
try:
    from serpapi import GoogleSearch
except Exception:
    GoogleSearch = None




class MedicalWebSearchTool:
    """Simple wrapper to fetch and summarize web search results.


    Prefer SerpAPI (clean JSON). If you provide BING_API_KEY it can use Bing as fallback.
    """


    def __init__(self, serpapi_key: str = None, bing_api_key: str = None):
        self.serpapi_key = serpapi_key or os.getenv("SERPAPI_API_KEY")
        self.bing_api_key = bing_api_key or os.getenv("BING_API_KEY")


    def search(self, query: str, num_results: int = 5) -> str:
        if self.serpapi_key and GoogleSearch is not None:
            params = {"engine": "google", "q": query, "api_key": self.serpapi_key, "num": num_results}
            search = GoogleSearch(params)
            res = search.get_dict()
            items = []
            for r in res.get("organic_results", [])[:num_results]:
                title = r.get("title")
                snippet = r.get("snippet") or r.get("snippet_highlighted_words")
                link = r.get("link")
                items.append(f"- {title}\n {snippet}\n {link}")
            summary = f"Top search results for: {query}\n\n" + "\n\n".join(items)
            return summary


    # Bing Web Search fallback (requires a valid BING_API_KEY and the Bing Web Search endpoint)
        if self.bing_api_key:
            headers = {"Ocp-Apim-Subscription-Key": self.bing_api_key}
            params = {"q": query, "count": num_results}
            endpoint = "https://api.bing.microsoft.com/v7.0/search"
            r = requests.get(endpoint, headers=headers, params=params, timeout=15)
            r.raise_for_status()
            jr = r.json()
            items = []
            for v in jr.get("webPages", {}).get("value", [])[:num_results]:
                items.append(f"- {v.get('name')}\n {v.get('snippet')}\n {v.get('url')}")
            return f"Top search results for: {query}\n\n" + "\n\n".join(items)


    raise ValueError("No search API key configured. Set SERPAPI_API_KEY or BING_API_KEY in .env")