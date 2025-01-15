import google.generativeai as genai
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from typing import List, Dict
import streamlit as st

class Models:
    def __init__(self, config):
        self.setup_gemini(config["GENAI_API_KEY"])
        self.setup_pinecone(config["PINECONE_API_KEY"])
        self.setup_mongodb(config["MONGODB_URI"])
        self.setup_encoder()
    
    def setup_gemini(self, api_key):
        genai.configure(api_key=api_key)
        generation_config = {
            "temperature": 0.7,
            "max_output_tokens": 2048,
            "candidate_count": 1,
            "top_k": 1,
            "top_p": 0.8
        }
        self.gemini = genai.GenerativeModel('gemini-1.5-flash',
                                          generation_config=generation_config)
    
    def setup_pinecone(self, api_key):
        try:
            pc = Pinecone(api_key=api_key)
            self.index = pc.Index("machine-learning-index2")
        except Exception as e:
            st.error(f"Pinecone Error: {e}")
    
    def setup_mongodb(self, uri):
        try:
            client = MongoClient(uri)
            db = client["ml_research"]
            self.article_cache = db["article_cache"]
            self.chat_history = db["chat_history"]
            
            # Create indexes
            self.article_cache.create_index("query")
            self.article_cache.create_index("timestamp")
            self.chat_history.create_index("timestamp")
        except Exception as e:
            st.error(f"MongoDB Error: {e}")
    
    def setup_encoder(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')