# Scholarly+

**Scholarly+** is an intelligent academic research assistant that combines semantic search capabilities with AI-driven analysis to help users navigate the vast landscape of machine learning research.

## Features

- **Advanced Semantic Search**: Search through machine learning publications using natural language queries.
- **AI-Powered Analysis**: Get AI-generated insights and explanations about research papers.
- **Interactive Chat Interface**: Engage in research discussions with the AI assistant.
- **Automatic Citation Tracking**: Keep track of your sources automatically.
- **Source Management**: Access and organize your research materials efficiently.

## Technology Stack

- **Frontend**: Streamlit
- **AI/ML**:
  - Google Gemini 1.5 Flash for text generation
  - SentenceTransformer for embedding generation
- **Database**:
  - MongoDB for caching and chat history
  - Pinecone for vector search
- **Other**: Python 3.8+

## Prerequisites

Before running this project, make sure you have the following:

- Python 3.8 or higher
- A Google Gemini API key
- A Pinecone account and API key
- A MongoDB and connection URI

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Firdaous01/Scholarly.git

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
3. Create a `.env` file in the root directory with your API keys:

   ```env
   GENAI_API_KEY=your_gemini_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   MONGODB_URI=your_mongodb_uri

## Running the Application

To run the application:

```bash
streamlit run main.py
