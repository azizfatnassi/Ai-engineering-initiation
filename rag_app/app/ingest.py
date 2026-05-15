import os 
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings 
from langchain_chroma import Chroma 


VECTORSTORE_DIR = "./vectorstore"
EMBED_MODEL = "mistral"

def load_file(file_path:str):
    """Load a file based on its extention."""
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext ==".pdf":
        print(f"Loading PDF: {file_path}")
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        print(f"loading text file :{file_path}")
        loader=TextLoader(file_path,encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    return loader.load() 

def ingest_documents(file_path: str):


    documents= load_file(file_path)
    print(f"Loaded{len(documents)} documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80

    )

    chunks= splitter.split_documents(documents)
    print(f"split into {len(chunks)} chunks")

    embedding_fn=OllamaEmbeddings(model="mistral")

    #import shutil
    #if os.path.exists(VECTORSTORE_DIR):
       # shutil.rmtree(VECTORSTORE_DIR)
       # print("cleared old vectorstore")

    #vectorstore = Chroma.from_documents(
      #  documents= chunks,
       # embedding= embedding_fn,
       # persist_directory=VECTORSTORE_DIR
  #  )

   # print(f" Done. {len(chunks)} chunks saved to vectorstore.")
   # return vectorstore 

   # Load existing vectorstore and clear it instead of deleting the folder
    vectorstore = Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embedding_fn
    )
    
    # Delete all existing documents
    existing = vectorstore.get()
    if existing["ids"]:
        vectorstore.delete(ids=existing["ids"])
        print(f"🗑️  Cleared {len(existing['ids'])} old chunks")

    # Add new chunks
    vectorstore.add_documents(chunks)
    print(f"✅ Done. {len(chunks)} chunks saved to vectorstore.")
    
    return vectorstore


if __name__ == "__main__":
    ingest_documents("./data/sample.txt")






