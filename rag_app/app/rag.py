


from typing import Generator

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM

from langchain_core.prompts import PromptTemplate


VECTORSTORE_DIR="./vectorstore"
EMBED_MODEL="mistral"
LLM_MODEL="mistral"


PROMPT_TEMPLATE = """You are a helpful assistant. Answer the question based on the context below.
    Use the information in the context to reason and infer your answer.
    Only if the context contains absolutely no relevant information, say "I don't know based on the provided documents."

    
Context :
    {context}

Question: {question}


Answer: """



def load_vectorstore() -> Chroma:
    embedding_fn= OllamaEmbeddings( model=EMBED_MODEL)
    return  Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function= embedding_fn
    )
    

def load_llm() -> OllamaLLM:
    return OllamaLLM(model=LLM_MODEL)

def ask(question: str, vectorstore: Chroma, llm:OllamaLLM) :
    
    retriever= vectorstore.as_retriever(search_kwargs={"k":3})
    relevant_chunks= retriever.invoke(question)

    print(f"Retrieved {len(relevant_chunks)} chunks  : ")
    for i, chunk in enumerate (relevant_chunks):
        print(f"[{i+1}] {chunk.page_content}")

    context = "\n\n".join([chunk.page_content for chunk in relevant_chunks])
    
    print(f"\n📋 CONTEXT SENT TO MISTRAL:\n{context}\n")
    

    prompt = PromptTemplate(
       input_variables=["context","question"],
       template=PROMPT_TEMPLATE
      )
       
    formatted_prompt= prompt.format(context=context, question=question)

    print ("Thinking")
    
    answer= llm.invoke(formatted_prompt)

    sources = [
        {
            "content": chunk.page_content,
            "source": chunk.metadata.get("source", "unknown"),
            "page": chunk.metadata.get("page", None)
        }
        for chunk in relevant_chunks
    ]

    return {"answer": answer, "sources": sources}



def ask_stream(question: str , vectorstore: Chroma, llm: OllamaLLM) -> Generator :
    retriever=vectorstore.as_retriever(search_kwargs={"k":3})
    relevant_chunks = retriever.invoke(question)

    print(f" stream retrieved {len(relevant_chunks)} chunks")
    for i, chunk in enumerate(relevant_chunks):                   # ADD
        print(f"  [{i+1}] {chunk.page_content[:150]}") 

        
    context="\n\n".join([chunk.page_content for chunk in relevant_chunks])
    prompt= PromptTemplate(
        input_variables=["context","question"],
        template= PROMPT_TEMPLATE
    )

    formatted_prompt=prompt.format(context=context , question=question)

    print("Streaming ..")
    for token in llm.stream(formatted_prompt):
        yield token


if __name__ == "__main__":
    
    vs = load_vectorstore()
    llm = load_llm()
    result = ask("What is the difference between AI and Machine Learning?", vs, llm)
    print(result["answer"])






