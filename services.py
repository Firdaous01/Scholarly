import datetime
from typing import List, Dict
import streamlit as st

class ResearchService:
    def __init__(self, models):
        self.models = models
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate response using Gemini Flash."""
        prompt = f"""You are an ML research expert. Answer based on these articles:
        {context}
        Question: {query}
        Answer:"""
        
        try:
            response = self.models.gemini.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def search_articles(self, query: str, top_k: int = 3) -> list:
        """Search articles using Pinecone."""
        try:
            query_embedding = self.models.encoder.encode([query])[0]
            results = self.models.index.query(
                vector=query_embedding.tolist(),
                top_k=top_k,
                include_metadata=True
            )
            return results.get('matches', [])
        except Exception as e:
            st.error(f"Search Error: {e}")
            return []
    
    def save_chat(self, query: str, response: str, articles: List[Dict]):
        """Save chat to MongoDB."""
        try:
            self.models.chat_history.insert_one({
                "timestamp": datetime.datetime.utcnow(),
                "query": query,
                "response": response,
                "articles": [
                    {
                        "title": article['title'],
                        "year": article['year'],
                        "authors": article['authors'],
                        "abstract": article['abstract'],
                        "url": article.get('url', '')
                    } for article in articles
                ]
            })
        except Exception as e:
            st.error(f"Save Error: {e}")