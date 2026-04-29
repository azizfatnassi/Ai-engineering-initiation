import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create a local ChromaDB (stores data in memory for now)
client = chromadb.Client()

# Create a collection — think of it like a table in a normal database
collection = client.create_collection(name="my_first_collection")

# Our documents
documents = [
    "I love playing football",
    "Soccer is my favorite sport",
    "I enjoy cooking pasta",
    "Machine learning is fascinating",
    "Deep learning is a subset of ML",
    "Python is the best programming language",
    "Neural networks are inspired by the human brain",
    "I like watching cooking shows on TV"
]

# Embed all documents
embeddings = model.encode(documents).tolist()

# Store in ChromaDB
# Each document needs: an embedding, the text, and a unique ID
collection.add(
    embeddings=embeddings,
    documents=documents,
    ids=[f"doc_{i}" for i in range(len(documents))]
)

print(f"Stored {collection.count()} documents in ChromaDB")
print()

# Now search with a natural language query
query = "what sports do you like?"
query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3  # return top 3 most similar documents
)

print(f"Query: '{query}'")
print("Top 3 results:")
for i, doc in enumerate(results["documents"][0]):
    distance = results["distances"][0][i]
    print(f"  {i+1}. {doc} (distance: {distance:.3f})")

print()

# Try another query
query2 = "tell me about artificial intelligence"
query_embedding2 = model.encode(query2).tolist()

results2 = collection.query(
    query_embeddings=[query_embedding2],
    n_results=3
)

print(f"Query: '{query2}'")
print("Top 3 results:")
for i, doc in enumerate(results2["documents"][0]):
    distance = results2["distances"][0][i]
    print(f"  {i+1}. {doc} (distance: {distance:.3f})")