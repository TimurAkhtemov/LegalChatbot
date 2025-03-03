import json
import chromadb
from sentence_transformers import SentenceTransformer

# Paths
data_file = "data/processed/processed_nj_statutes.json"

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="data/chromadb")
collection = chroma_client.get_or_create_collection(name="nj_statutes")

# Load embedding model (lightweight & efficient)
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def index_statutes():
    with open(data_file, "r", encoding="utf-8") as f:
        statutes = json.load(f)

    for title_obj in statutes:
        title = title_obj["title"]
        
        for section in title_obj["sections"]:
            section_id = section["section"]
            heading = section["heading"]
            text = section["text"]
            
            # Create text for embedding
            doc_text = f"{heading}: {text}"
            embedding = embedding_model.encode(doc_text).tolist()
            
            # Store in ChromaDB
            collection.add(
                ids=[section_id],
                embeddings=[embedding],
                metadatas=[{"title": title, "section": section_id, "heading": heading, "text": text}]
            )
            print(f"Indexed: {section_id}")

if __name__ == "__main__":
    index_statutes()
    print("Indexing complete!")
