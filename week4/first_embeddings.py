from sentence_transformers import SentenceTransformer

# Load a free local embedding model
# Downloads automatically on first run (~90MB)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Embed some sentences
sentences = [
    "I love playing football",
    "Soccer is my favorite sport",
    "I enjoy cooking pasta",
    "Machine learning is fascinating",
    "Deep learning is a subset of ML"
]

embeddings = model.encode(sentences)

print(f"Number of sentences: {len(sentences)}")
print(f"Embedding shape: {embeddings.shape}")
print(f"Each sentence becomes {embeddings.shape[1]} numbers")
print()

# Now measure similarity between sentences
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

similarity_matrix = cosine_similarity(embeddings)

print("Similarity scores (1.0 = identical meaning, 0.0 = completely different):")
print()
for i in range(len(sentences)):
    for j in range(i+1, len(sentences)):
        score = similarity_matrix[i][j]
        print(f"{score:.2f} | '{sentences[i]}' ↔ '{sentences[j]}'")