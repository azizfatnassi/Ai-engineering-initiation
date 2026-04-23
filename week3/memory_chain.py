
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage


llm = ChatOllama(model="mistral", base_url="http://localhost:11434")

prompt= ChatPromptTemplate.from_messages([
    ("systems","Youa re a good assitant"),
    MessagesPlaceholder(variable_name="history"),
    ("human","{question}")
])

chain = prompt | llm | StrOutputParser()

history=[]

def chat(question:str)->str:
        response= chain.invoke({
        "history":history,
        "question": question
          })
    
        history.append(HumanMessage(content=question))
        history.append(AIMessage(content=response))
        return response
    

print(chat("My name is Aziz and I am from Tunisia."))
print(chat("What is my name and where am I from?"))
print(chat("What did I tell you first?"))