import aiohttp
import xml.etree.ElementTree as ET
from typing import List, Dict
from datetime import datetime
from ..config import settings

class ArxivService:
    def __init__(self):
        self.base_url = "https://export.arxiv.org/api/query"
        self.ns = {"atom": "http://www.w3.org/2005/Atom"}
    
    async def search(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search arXiv for academic papers"""
        try:
            params = {
                "search_query": f"all:{query}",
                "start": 0,
                "max_results": max_results,
                "sortBy": "relevance",
                "sortOrder": "descending"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    response.raise_for_status()
                    content = await response.text()

            root = ET.fromstring(content)
            results = []

            for entry in root.findall("atom:entry", self.ns):
                # Parse summary
                summary = entry.find("atom:summary", self.ns).text or ""
                summary = " ".join(summary.split())  # collapse all whitespace
                if len(summary) > 300:
                    summary = summary[:300] + "..."

                # Parse published date
                published_raw = entry.find("atom:published", self.ns).text or ""
                try:
                    published = datetime.fromisoformat(published_raw.replace("Z", "+00:00")).strftime("%Y-%m-%d")
                except ValueError:
                    published = published_raw[:10]

                # Parse authors
                authors = [
                    a.find("atom:name", self.ns).text
                    for a in entry.findall("atom:author", self.ns)
                ][:3]

                # Parse categories
                categories = [
                    tag.get("term", "")
                    for tag in entry.findall("{http://arxiv.org/schemas/atom}primary_category", self.ns)
                ]
                # Fallback: grab all category tags
                if not categories:
                    categories = [
                        tag.get("term", "")
                        for tag in entry.findall("category")
                    ]

                entry_id = entry.find("atom:id", self.ns).text or ""

                results.append({
                    "title": (entry.find("atom:title", self.ns).text or "").strip(),
                    "content": summary,
                    "url": entry_id,
                    "source_type": "arxiv",
                    "metadata": {
                        "authors": authors,
                        "published": published,
                        "categories": categories
                    }
                })

            return results

        except Exception as e:
            print(f"arXiv service error: {e}")
            return []


arxiv_service = ArxivService()