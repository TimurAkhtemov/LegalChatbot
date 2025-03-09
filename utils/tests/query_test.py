import chromadb

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="data/chromadb")
collection = chroma_client.get_collection("nj_statutes")

# Run a test query
query_text = "punishments for crime"
results = collection.query(
    query_texts=[query_text],
    n_results=3
)

# Print results
for i, doc in enumerate(results["metadatas"][0]):
    print(f"Result {i+1}: {doc['section']} - {doc['heading']}\nText: {doc['text'][:300]}...\n")


