# NJ Legal Q&A Chatbot

## Project Overview

The NJ Legal Q&A Chatbot is designed to retrieve and analyze New Jersey state statutes using a Retrieval-Augmented Generation (RAG) approach. It processes legal texts, indexes them in a ChromaDB vector database, and uses Google's Gemini models to generate accurate, grounded responses based on user queries.

## Features

- **Statute Processing**: Parses raw legal text and converts it into structured JSON format for indexing
- **Vector Indexing**: Stores legal texts as embeddings in ChromaDB using Gemini embeddings for efficient retrieval
- **Interactive Web Interface**: Streamlit-based UI that allows users to ask legal questions
- **RAG Implementation**: Uses ChromaDB for retrieval and Gemini 1.5 Flash for generating answers
- **Custom Embedding**: Uses Google's Gemini embedding model for semantic search
- **Fine-tuned Model**: Includes a fine-tuned Qwen 2.5 1.5B model for specialized legal reasoning

## Installation

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)
- Google API key for Gemini access

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your-repo/legal-chatbot-project.git
cd legal-chatbot-project
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
```bash
export GOOGLE_API_KEY='your-api-key-here'  # For Gemini API
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Access the web interface at http://localhost:8501

3. Enter your legal question about New Jersey law in the search box

4. The system will:
   - Retrieve relevant statutes from ChromaDB
   - Generate a response using the Gemini model
   - Display both the answer and the source statutes

## Project Components

- `app.py`: Streamlit web interface
- `rag_pipeline.py`: Core RAG implementation connecting ChromaDB with Gemini
- `gemini_embed_function.py`: Custom embedding function for ChromaDB
- `utils/`: Directory containing statute processing utilities
- `chroma_db/`: Persistent storage for ChromaDB vector database
- `qwen2.5-1.5b-finetuned/`: WORK IN PROGRESS (fine tuning model to retrieve citations from the text)

## Development Notes

### Data Processing
- The system processes raw NJ statute texts into structured data for indexing
- Filtering removes empty sections while preserving meaningful content
- Citations are extracted and processed to enhance context

### Model Selection
- Gemini 1.5 Flash provides efficient response generation
- Custom embedding function enhances retrieval quality

## Future Enhancements
- Implement additional filtering options based on statute metadata
- Add citation linking between related statutes
- Improve handling of complex legal questions with multiple statute references
- Enhance UI with legal citation formatting and explanation features
