import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..config import settings

class NewsService:
    def __init__(self):
        self.api_key = settings.NEWS_API_KEY
        self.base_url = settings.NEWS_API
    
    def search(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search for news articles"""
        if not self.api_key:
            print("NewsAPI key not configured")
            return []
        
        try:
        
            from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            
            params = {
                "q": query,
                "apiKey": self.api_key,
                "pageSize": max_results,
                "sortBy": "relevancy",
                "language": "en",
                "from": from_date
            }
            
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                results = []
                for article in articles:
                
                    if (article.get('title') and 
                        article.get('title') != "[Removed]" and 
                        article.get('description')):
                        
                        content = article.get('description') or article.get('content') or ""
                        
                        if content:
                            content = content.strip()
                            if len(content) > 250:
                                content = content[:250] + "..."
                        
                        results.append({
                            "title": article['title'],
                            "content": content,
                            "url": article.get('url', '#'),
                            "source_type": "news",
                            "metadata": {
                                "source": article.get('source', {}).get('name', 'Unknown'),
                                "published": article.get('publishedAt', '')[:10],
                                "author": article.get('author')
                            }
                        })
                
                return results
            else:
                print(f"NewsAPI error: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"News service error: {e}")
            return []
news_service = NewsService()