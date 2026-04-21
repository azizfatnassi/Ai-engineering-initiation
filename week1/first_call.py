import requests
import json


def ask_mistral(prompt):
    response = requests.post(
    "http://localhost:11434/api/generate",


    json={
       "model": "mistral",
       "prompt": prompt,
       "stream": False
       }
    )

    data= response.json()
    return data["response"]
answer= ask_mistral("hello who are you?")
print(answer)

