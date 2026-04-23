from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

llm=ChatOllama(model="mistral",base_url="http://localhost:11434")

messages=[SystemMessage(content="You are a helpful assistant who answers concisely."),
          HumanMessage(content="What is the difference between RAM and ROM?")]

response= llm.invoke(messages)
print(response.content)