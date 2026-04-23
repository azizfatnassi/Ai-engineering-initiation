
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm= ChatOllama(model="mistral",base_url="http://localhost:11434")

prompt= ChatPromptTemplate.from_messages([
    ("system","you are an expert in {domain}. Answer clearly and concisely."),
    ("human","{question}")
 ])
chain= prompt | llm | StrOutputParser()

response= chain.invoke({
        "domain": "machine learning",
    "question": "What is overfitting and how do you fix it?"
    })

print(response)
