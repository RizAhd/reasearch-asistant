import arxiv
from typing import List, Dict
from ..config import settings

class ArxivService:
    def __init__(self):
        self.client = arxiv.Client()
    
    async def search(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search arXiv for academic papers"""
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = []
            async for paper in self.client.results(search):
                
                summary = paper.summary
                summary = summary.replace('\n', ' ').strip()
                
            
                while '  ' in summary:
                    summary = summary.replace('  ', ' ')
                

                if len(summary) > 300:
                    summary = summary[:300] + "..."
                
                results.append({
                    "title": paper.title,
                    "content": summary,
                    "url": paper.entry_id,
                    "source_type": "arxiv",
                    "metadata": {
                        "authors": [str(author) for author in paper.authors[:3]],
                        "published": paper.published.strftime("%Y-%m-%d"),
                        "categories": paper.categories
                    }
                })
            
            return results
            
        except Exception as e:
            print(f"arXiv service error: {e}")
            return []


arxiv_service = ArxivService()