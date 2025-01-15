import streamlit as st
from typing import List, Dict
import datetime

def format_context(articles_metadata: List[Dict]) -> str:
    context = ""
    for article in articles_metadata:
        context += f"Title: {article['title']}\n"
        context += f"Abstract: {article['abstract']}\n"
        context += f"Authors: {', '.join(article['authors'])}\n"
        context += f"Year: {article['year']}\n"
        context += f"URL: {article.get('url', 'N/A')}\n\n"
    return context

def render_welcome():
    st.title("Scholarly+")
    st.markdown("""
    Welcome to Scholarly+, your intelligent academic research assistant. This platform combines 
    the power of semantic search with AI-driven analysis to help you navigate the vast landscape 
    of machine learning research.

    Scholarly+ offers:
    - Advanced semantic search across machine learning publications
    - AI-powered research synthesis and explanations
    - Interactive chat interface for research discussions
    - Automatic citation tracking and source management
    """)

def render_search_tab(research_service):
    st.header("Article Search")
    search_query = st.text_input("Search", key="search", placeholder="Enter keywords...")
    
    if st.button("Search", key="search_btn"):
        if search_query:
            # Check cache
            cached = research_service.models.article_cache.find_one({"query": search_query})
            
            if cached:
                results = cached["results"]
                st.success("Found in cache")
            else:
                results = research_service.search_articles(search_query)
                
                if results:
                    # Format results
                    formatted_results = []
                    for r in results:
                        formatted_results.append({
                            "title": r['metadata']['title'],
                            "abstract": r['metadata']['abstract'],
                            "authors": r['metadata']['authors'],
                            "year": r['metadata']['year'],
                            "score": r['score'],
                            "url": r['metadata'].get('url', '')
                        })
                    
                    # Cache results
                    research_service.models.article_cache.update_one(
                        {"query": search_query},
                        {
                            "$set": {
                                "results": formatted_results,
                                "timestamp": datetime.datetime.utcnow()
                            }
                        },
                        upsert=True
                    )
                    
                    results = formatted_results
            
            # Store results in session state
            st.session_state.current_search_results = results
            
            # Display results
            if results:
                for r in results:
                    with st.expander(f" 📄 {r['title']}", expanded=False):
                        st.write(f"**Abstract:** {r['abstract']}")
                        st.write(f"**Authors:** {', '.join(r['authors'])}")
                        st.write(f"**Year:** {r['year']}")
                        st.write(f"**Link:** [Read More]({r.get('url', '')})")
            else:
                st.warning("No results found")
        else:
            st.warning("Enter a search query")

def render_chat_tab(research_service):
    st.header("Research Assistant")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "articles" in message:
                with st.expander("📚 Sources"):
                    for article in message["articles"]:
                        st.write(f"- {article['title']} ({article['year']})")
                        st.write(f"  Authors: {', '.join(article['authors'])}")
                        if article.get('url'):
                            st.write(f"  [Read More]({article['url']})")
    
    handle_chat_input(research_service)

def handle_chat_input(research_service):
    if prompt := st.chat_input("Ask about ML research..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Use current search results if available, otherwise perform new search
        if st.session_state.current_search_results:
            articles_metadata = st.session_state.current_search_results
        else:
            search_results = research_service.search_articles(prompt)
            articles_metadata = []
            if search_results:
                for r in search_results:
                    metadata = r['metadata']
                    articles_metadata.append({
                        'title': metadata['title'],
                        'abstract': metadata['abstract'],
                        'authors': metadata['authors'],
                        'year': metadata['year'],
                        'url': metadata.get('url', '')
                    })
        
        if articles_metadata:
            # Generate response
            context = format_context(articles_metadata)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing research..."):
                    response = research_service.generate_response(prompt, context)
                    st.write(response)
                    
                    with st.expander("📚 Sources"):
                        for article in articles_metadata:
                            st.write(f"- {article['title']} ({article['year']})")
                            st.write(f"  Authors: {', '.join(article['authors'])}")
                            if article.get('url'):
                                st.write(f"  [Read More]({article['url']})")
            
            # Update chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "articles": articles_metadata
            })
            
            # Save chat
            research_service.save_chat(prompt, response, articles_metadata)
        else:
            with st.chat_message("assistant"):
                st.write("No relevant articles found. Try searching for some articles first in the Search tab.")

def render_sidebar(research_service):
    with st.sidebar:
        st.header("Statistics")
        try:
            total_chats = research_service.models.chat_history.count_documents({})
            today_chats = research_service.models.chat_history.count_documents({
                "timestamp": {
                    "$gte": datetime.datetime.now().replace(hour=0, minute=0, second=0)
                }
            })
            st.write(f"Total chats: {total_chats}")
            st.write(f"Today: {today_chats}")
            
            if st.button("Clear Chat"):
                st.session_state.messages = []
                st.session_state.current_search_results = []
                st.rerun()
        except Exception as e:
            st.error(f"Stats Error: {e}")