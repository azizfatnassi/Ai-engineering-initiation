
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="mistral", base_url="http://localhost:11434")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])

chain = prompt | llm | StrOutputParser()

for chunk in chain.stream({"question": "Count from 1 to 5 and explain each number."}):
    print(chunk, end="", flush=True)

print()