import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def load_config():
    # Page config
    st.set_page_config(
        page_title="Scholarly+",
        layout="wide"
    )
    
  
    config = {
        "GENAI_API_KEY": os.getenv("GENAI_API_KEY"),
        "PINECONE_API_KEY": os.getenv("PINECONE_API_KEY"),
        "MONGODB_URI": os.getenv("MONGODB_URI")
    }
    
    if not all(config.values()):
        st.error("Missing environment variables. Please check your .env file.")
        
    return config