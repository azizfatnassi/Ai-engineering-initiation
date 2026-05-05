


from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from torch import chunk
from langchain_core.prompts import PromptTemplate


def load_vectorstore():
    embedding_fn= OllamaEmbeddings( model="mistral")
    vectorestore= Chroma(
        persist_directory="./vectorestore",
        embedding_function= embedding_fn
    )
    return vectorestore

def ask(question: str):
    vectorestore= load_vectorstore()
    retriever= vectorestore.as_retriever(search_kwargs={"k":3})
    relevant_chunks=retriever.invoke(question)

    print(f"Retrieved {len(relevant_chunks)} chunks  : ")
    for i, chunk in enumerate (relevant_chunks):
        print(f"[{i+1}] {chunk.page_content}")

    context = "\n".join([chunk.page_content for chunk in relevant_chunks])
    print(f"\n📋 CONTEXT SENT TO MISTRAL:\n{context}\n")
    template = """You are a helpful assistant. Answer the question based on the context below.
    Use the information in the context to reason and infer your answer.
    Only if the context contains absolutely no relevant information, say "I don't know based on the provided documents."
   
    Context :
    {context}

    Question: {question}


    Answer: """

    prompt = PromptTemplate(
       input_variables=["context","question"],
       template=template
      )
       
    formatted_prompt= prompt.format(context=context, question=question)

    print ("Thinking")
    llm= OllamaLLM(model="mistral")
    answer= llm.invoke(formatted_prompt)

    print(f"\n Answer : {answer}")
    return answer

if __name__ == "__main__":
    ask("What is the difference between AI and Machine Learning?")







