import chromadb
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.PersistentClient(path='./chroma_code')
collection = client.get_or_create_collection(name='code_search')




def search_code(query: str, n_results: int = 3)->list[dict]:
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    output=[]
    for i in range(len(results['documents'][0])):
        metadata = results['metadatas'][0][i]
        distance = results['distances'][0][i]
        document = results['documents'][0][i]

        output.append({
            'function_name': metadata['function_name'],
            'file_path': metadata['file_path'],
            'line_number': int(metadata['line_number']),
            'score': round((2 - distance) / 2, 3),
            'code': results['documents'][0][i]
        })

    return output



if __name__ == '__main__':
    queries = [
        "handle file upload",
        "search similar documents",
        "stream tokens to client"
    ]

    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        results = search_code(query)
        for r in results:
            print(f"{'='*50}")
            print(f"Function : {r['function_name']}")
            print(f"File     : {r['file_path']}")
            print(f"Line     : {r['line_number']}")
            print(f"Score    : {r['score']}")
            print(f"Code     :\n{r['code'][:300]}")