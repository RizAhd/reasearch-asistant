import requests
from typing import Optional, Dict
import html
from ..config import settings

class WikipediaService:
    def __init__(self):
        self.base_url = settings.WIKIPEDIA_API
        self.headers = {
            'User-Agent': 'ResearchAssistant/1.0 (research@example.com)'
        }
    
    def search(self, query: str, max_chars: int = 500) -> Optional[Dict]:
        """Search Wikipedia for information"""
        try:
            # Clean query
            clean_query = query.strip()
            
            # First, try to get page directly
            params = {
                "action": "query",
                "format": "json",
                "prop": "extracts|info",
                "exintro": True,
                "explaintext": True,
                "titles": clean_query,
                "inprop": "url"
            }
            
            response = requests.get(
                self.base_url, 
                params=params, 
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                pages = data.get("query", {}).get("pages", {})
                
                for page_id, page_info in pages.items():
                    if page_id != "-1":  # Valid page
                        content = page_info.get('extract', '')
                        if content:
                            # Clean and truncate
                            content = html.unescape(content)
                            if len(content) > max_chars:
                                content = content[:max_chars] + "..."
                            
                            return {
                                "title": page_info.get('title', clean_query),
                                "content": content,
                                "url": f"https://en.wikipedia.org/?curid={page_id}",
                                "source_type": "wikipedia",
                                "metadata": {
                                    "page_id": page_id
                                }
                            }
            
            # If direct page not found, search
            search_params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": query,
                "srlimit": 3
            }
            
            search_response = requests.get(
                self.base_url, 
                params=search_params, 
                headers=self.headers,
                timeout=10
            )
            
            if search_response.status_code == 200:
                search_data = search_response.json()
                search_results = search_data.get('query', {}).get('search', [])
                
                if search_results:
                    # Try the first result
                    first_result = search_results[0]
                    return self.search(first_result['title'])
            
            return None
            
        except Exception as e:
            print(f"Wikipedia service error: {e}")
            return None

# Singleton instance
wikipedia_service = WikipediaService()