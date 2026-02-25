import asyncio
import time
from typing import List, Dict
from datetime import datetime
from ..schemas.response import ResearchResponse, Source
from .wikipedia_service import wikipedia_service
from .arxiv_service import arxiv_service
from .news_service import news_service
from .ai_service import ai_service

class ResearchService:
    def __init__(self):
        self.services = {
            "wikipedia": wikipedia_service,
            "arxiv": arxiv_service,
            "news": news_service
        }
    
    async def research(self, query: str, include_sources: List[str] = None, max_sources: int = 5) -> ResearchResponse:
        """Main research orchestration function"""
        start_time = time.time()
        
        if include_sources is None:
            include_sources = ["wikipedia", "arxiv", "news"]
        
        print(f"🔍 Researching: {query}")
        print(f"📚 Including sources: {include_sources}")
        
    
        tasks = []
        
        if "wikipedia" in include_sources:
            
            wiki_task = asyncio.to_thread(wikipedia_service.search, query)
            tasks.append(wiki_task)
        
        if "arxiv" in include_sources:
            arxiv_task = arxiv_service.search(query, max_results=2)
            tasks.append(arxiv_task)
        
        if "news" in include_sources:
        
            news_task = asyncio.to_thread(news_service.search, query, max_results=2)
            tasks.append(news_task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        
        all_sources = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Error fetching from source {i}: {result}")
                continue
            
            if result:
                if isinstance(result, list):
                    all_sources.extend(result[:max_sources])
                elif isinstance(result, dict):
                    all_sources.append(result)
        
        
        seen_urls = set()
        unique_sources = []
        for source in all_sources:
            if source.get('url') not in seen_urls:
                seen_urls.add(source.get('url'))
                unique_sources.append(source)
        
        final_sources = unique_sources[:max_sources]
        
        print(f"✅ Found {len(final_sources)} unique sources")
        

        ai_result = ai_service.generate_answer(query, final_sources)
        processing_time = time.time() - start_time
        
        
        source_objects = []
        for src in final_sources:
            source_objects.append(Source(
                title=src.get('title', 'Unknown'),
                content=src.get('content', ''),
                url=src.get('url', '#'),
                source_type=src.get('source_type', 'unknown'),
                metadata=src.get('metadata', {})
            ))
        
        return ResearchResponse(
            answer=ai_result['answer'],
            sources=source_objects,
            query=query,
            tokens_used=ai_result['tokens_used'],
            processing_time=round(processing_time, 2),
            timestamp=datetime.now()
        )

research_service = ResearchService()