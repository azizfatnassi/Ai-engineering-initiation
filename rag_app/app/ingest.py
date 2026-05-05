from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings 
from langchain_chroma import Chroma 

def ingest_documents(file_path: str):
    print(f"loading document: {file_path}")
    loader = TextLoader(file_path, encoding="utf-8")
    documents= loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=30

    )

    chunks= splitter.split_documents(documents)
    print(f"split into {len(chunks)} chunks")

    embedding_fn=OllamaEmbeddings(model="mistral")

    vectorestore = Chroma.from_documents(
        documents= chunks,
        embedding= embedding_fn,
        persist_directory="./vectorestore"
    )

    print("Done Vectorestore saved.")
    return vectorestore 


if __name__ == "__main__":
    ingest_documents("./data/sample.txt")

