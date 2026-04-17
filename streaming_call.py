import requests
import json

def stream_call(prompt):
    url="http://localhost:11434/api/generate"

    payload= {
        "model": "mistral",
        "prompt": prompt,
        "stream": True
    }

    response= requests.post(url,json=payload,stream=True)
    #print("Mistral:",end="",flush=True)

    for line in response.iter_lines():
      if line:
         chunk= json.loads(line)
         print(chunk["response"],end="",flush=True)

         if chunk.get("done"):
            break
         
    print()

stream_call("Explain what an API is in 3 sentences.")