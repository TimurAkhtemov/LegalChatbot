from chromadb import Client
from google import generativeai as genai
import os
from gemini_embed_function import GeminiEmbeddingFunction

# Configure the Gemini API with your API key
# You should set this as an environment variable: export GOOGLE_API_KEY='your-api-key-here'
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

import chromadb
from chromadb.utils import embedding_functions

# Use the exact same initialization as in your notebook
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# If using custom embedding function (e.g., Gemini), include it
collection = chroma_client.get_collection(
    name="nj_statutes_test_chunks",
    embedding_function=GeminiEmbeddingFunction()
)

def get_statute_context(question, n_results=3):
    results = collection.query(query_texts=[question], n_results=n_results)
    context_chunks = results['documents'][0]
    metadatas = results['metadatas'][0]
    return context_chunks, metadatas

def build_prompt(context, question):
    return f"""
You are a legal assistant. Answer based only on the legal context below.

Context:
{context}

User Question:
{question}

Instructions:
- Use only the context provided.
- If the answer is not found, say so.
"""

def generate_gemini_response(prompt):
    # Create a GenerativeModel using the Gemini 1.5 Flash model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Generate content with the prompt
    response = model.generate_content(prompt)
    
    # Return the text response
    return response.text

def get_answer(question):
    chunks, metadatas = get_statute_context(question)
    context = "\n\n".join(chunks)
    prompt = build_prompt(context, question)
    answer = generate_gemini_response(prompt)
    return answer, metadatas