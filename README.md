Legal Q&A Chatbot

Project Overview

The Legal Q&A Chatbot is designed to retrieve and analyze New Jersey state statutes using a Retrieval-Augmented Generation (RAG) approach. It processes legal texts, indexes them in a ChromaDB vector database, and uses a large language model (LLM) (Mistral-7B) to generate responses based on user queries.

Features

- Statute Processing: Parses raw legal text and converts it into structured JSON format.
- Vector Indexing: Stores legal texts as embeddings in ChromaDB for efficient retrieval.
- Query Retrieval: Allows users to search statutes based on natural language queries.
- LLM Integration: Uses Mistral-7B for generating answers based on retrieved statutes.
- Filtering & Preprocessing: Removes duplicate statutes and excludes sections with no meaningful content.

Installation

Prerequisites
- Python 3.8+
- Virtual environment (recommended)
- Required dependencies in requirements.txt

Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your-repo/legal-chatbot-project.git
cd legal-chatbot-project
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up ChromaDB storage (optional):
```bash
mkdir -p data/chromadb
```

Usage

1. Processing Statutes  
Convert raw legal text (STATUTES.txt) into structured JSON.
```bash
python utils/process_statutes.py
```

2. Indexing Processed Statutes  
Store processed statutes in ChromaDB for retrieval.
```bash
python utils/index_nj_statutes.py
```

3. Querying Statutes  
Retrieve relevant statutes based on a natural language query.
```bash
python utils/query_test.py
```


Development Notes

Filtering Criteria
- Sections with empty text fields are excluded from indexing.
- Legal sections with terms like "repealed," "superseded," or "reallocated" are only excluded if they have no text.
- The test file (STATUTES_TEST.txt) includes edge cases to verify processing behavior.

Free RAG Deployment Options
- Hugging Face Inference API (for quick cloud-based LLM queries)
- Google Colab (for free GPU-based inference)
- Hugging Face Spaces (for persistent chatbot deployment)

Next Steps
- Implement full LLM integration for answer generation.
- Explore chunking long statutes for improved retrieval.
- Optimize query filtering based on metadata (e.g., title-based filtering).
