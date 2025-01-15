import streamlit as st
from config import load_config
from models import Models
from services import ResearchService
from components import (
    render_welcome,
    render_search_tab,
    render_chat_tab,
    render_sidebar
)

def main():
    
    config = load_config()
    
    
    models = Models(config)
    research_service = ResearchService(models)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_search_results" not in st.session_state:
        st.session_state.current_search_results = []
    
    # Render components
    render_welcome()
    
    # Tabs
    tab1, tab2 = st.tabs(["🔍 Search", "💬 Research Assistant"])
    
    with tab1:
        render_search_tab(research_service)
    
    with tab2:
        render_chat_tab(research_service)
    
    render_sidebar(research_service)

if __name__ == "__main__":
    main()