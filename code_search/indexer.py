


import chromadb
from sentence_transformers import SentenceTransformer

from code_parser import index_directory


model= SentenceTransformer("all-MiniLM-L6-v2")
client= chromadb.PersistentClient(path='./chroma_code')
collection= client.get_or_create_collection(name='code_search')

def index_codebase(directory: str):

    print(f"parsing {directory}...")

    chunks= index_directory(directory)
    print(f"found{len(chunks)} functions")
    documents=[ chunk.content for chunk in chunks]
    embeddings=model.encode(documents).tolist()

    metadatas= [
        {
            'function_name': chunk.function_name,
            'file_path': chunk.file_path,
            'line_number': chunk.line_number
        }

        for chunk in chunks
    ]

    ids = [f"{chunk.file_path}:{chunk.function_name}:{chunk.line_number}"
           for chunk in chunks]


    collection.upsert(
        documents=documents,
        embeddings=embeddings,
        metadatas= metadatas,
        ids=ids
    )

    print(f"indxed {len(chunks)} functions into ChromaDB")

if __name__ == '__main__':
    index_codebase("../rag_app")