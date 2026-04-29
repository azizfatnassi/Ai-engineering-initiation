
import chromadb
from sentence_transformers import SentenceTransformer

model=SentenceTransformer("all-MiniLM-L6-v2")

client=chromadb.PersistentClient("./chromadb")

collection=client.get_or_create_collection(name="knowledge_base")

documents=[
    "Tunisia is a country in North Africa, bordered by Algeria to the west and Libya to the east.",
    "Tunis is the capital and largest city of Tunisia, home to over 2 million people.",
    "Tunisia has a Mediterranean climate with hot summers and mild winters.",
    
    # Chunk 4-6: About Python
    "Python is a high-level programming language known for its simplicity and readability.",
    "Python supports multiple programming paradigms including procedural, object-oriented, and functional programming.",
    "Python is widely used in data science, machine learning, and web development.",
    
    # Chunk 7-9: About AI
    "Artificial intelligence is the simulation of human intelligence by computer systems.",
    "Machine learning is a subset of AI that enables systems to learn from data without being explicitly programmed.",
    "Large language models like GPT and Mistral are trained on massive amounts of text data.",
]


metadatas = [
    {"topic": "tunisia", "chunk": 1},
    {"topic": "tunisia", "chunk": 2},
    {"topic": "tunisia", "chunk": 3},
    {"topic": "python", "chunk": 1},
    {"topic": "python", "chunk": 2},
    {"topic": "python", "chunk": 3},
    {"topic": "ai", "chunk": 1},
    {"topic": "ai", "chunk": 2},
    {"topic": "ai", "chunk": 3},
]

if collection.count()== 0:
    embeddings=model.encode(documents).tolist()
    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=[f"doc_{i}" for i in range(len(documents))]
    )

    print(f"Added{len(documents)} documents to ChromaDB")

else: 
    print(f"Collection already has {collection.count()} documents — skipping add")

print()

def search(query: str, n: int = 3):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n
    )
    print(f"Query: '{query}'")
    for i, doc in enumerate(results["documents"][0]):
        distance = results["distances"][0][i]
        metadata = results["metadatas"][0][i]
        print(f"  {i+1}. [{metadata['topic']}] {doc} (distance: {distance:.3f})")
    print()

search("What is the capital of Tunisia?")
search("How is Python used in AI?")
search("What are large language models?")

# Search 2 — filter by metadata
print("--- Filtered search: only AI topic ---")
query_embedding = model.encode("tell me about machine learning").tolist()
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
    where={"topic": "ai"}  # ← only search within AI documents
)
for i, doc in enumerate(results["documents"][0]):
    print(f"  {i+1}. {doc}")