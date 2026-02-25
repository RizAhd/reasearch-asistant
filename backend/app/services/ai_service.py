from openai import OpenAI
from typing import List, Dict
import json
from ..config import settings

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
    
    def generate_answer(self, query: str, sources: List[Dict]) -> Dict:
        """Generate comprehensive answer from sources"""
        
        if not sources:
            return {
                "answer": "I couldn't find enough relevant sources to answer your question. Please try rephrasing or try a different query.",
                "tokens_used": 0
            }
        
        
        formatted_sources = self._format_sources(sources)
        
        system_prompt = """You are a helpful research assistant. Your task is to:
1. Provide a comprehensive answer to the user's question
2. Use ONLY information from the provided sources
3. Cite sources clearly using numbers like [1], [2], [3] after relevant statements
4. If sources contradict each other, acknowledge this
5. If information is missing from sources, say so honestly
6. Structure your answer with clear paragraphs
7. Keep the answer informative but concise"""

        user_prompt = f"""QUESTION: {query}

AVAILABLE SOURCES:
{formatted_sources}

Please provide a well-researched answer with proper citations:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=False
            )
            
            answer = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            return {
                "answer": answer,
                "tokens_used": tokens_used
            }
            
        except Exception as e:
            print(f"OpenAI service error: {e}")
            return {
                "answer": f"I encountered an error while generating the answer. Please try again. Error: {str(e)[:100]}",
                "tokens_used": 0
            }
    
    def _format_sources(self, sources: List[Dict]) -> str:
        """Format sources for the prompt"""
        formatted = []
        for i, source in enumerate(sources, 1):
            source_text = f"--- SOURCE {i} ---\n"
            source_text += f"TITLE: {source.get('title', 'No title')}\n"
            source_text += f"TYPE: {source.get('source_type', 'unknown')}\n"
            source_text += f"CONTENT: {source.get('content', 'No content available')}\n"
            
            if source.get('metadata'):
                meta = source['metadata']
                if meta.get('authors'):
                    source_text += f"AUTHORS: {', '.join(meta['authors'][:3])}\n"
                if meta.get('published'):
                    source_text += f"DATE: {meta['published']}\n"
                if meta.get('source'):
                    source_text += f"NEWS SOURCE: {meta['source']}\n"
            
            formatted.append(source_text)
        
        return "\n\n".join(formatted)

ai_service = AIService()