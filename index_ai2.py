import os
import json
import pinecone
from pinecone import ServerlessSpec
from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


pinecone_api_key = os.getenv('PINECONE_API_KEY')


def generate_pinecone_embeddings(file_path='papers_data.json'):
    # Initialize Pinecone 
    pc = pinecone.Pinecone(api_key=pinecone_api_key)

    # Define index name and specifications
    index_name = "machine-learning-index2"
    spec = ServerlessSpec(
        cloud='aws',
        region='us-east-1'
    )

    # Connect to the Pinecone index
    index = pc.Index(index_name)

    # Load data from JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Initialize the SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Prepare texts for embedding generation
    texts = [article['title'] + ' ' + ' '.join(article['author']) + ' ' + article['abstract'] for article in data]

    # Generate embeddings for the articles
    embeddings = model.encode(texts)

    # Prepare metadata and IDs
    ids = [str(i) for i in range(len(data))]
    metadatas = [
        {
            'title': article['title'], 
            'author': article['author'], 
            'abstract': article['abstract'],
            'year': article.get('year', ''), 
            'url': article.get('url', '')
        } for article in data
    ]

    # Store embeddings in Pinecone
    index.upsert(vectors=zip(ids, embeddings, metadatas))

    print("Data successfully inserted into Pinecone!")

if __name__ == "__main__":
    generate_pinecone_embeddings()