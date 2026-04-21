
# system_prompt.py
import requests
import json

def ask_with_system(system_prompt, user_message, temperature=0.7):
    url = "http://localhost:11434/api/chat"  # note: /api/chat, not /api/generate
    
    payload = {
        "model": "mistral",
        "options": {
            "temperature": temperature
        },
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message}
        ],
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    return response.json()["message"]["content"]

# --- Test 3 completely different system prompts on the SAME question ---

question = "Should I learn Python or JavaScript first?"

# Persona 1: strict senior engineer
print("=== STRICT ENGINEER ===")
print(ask_with_system(
    "You are a senior software engineer with 15 years of experience. You give direct, no-nonsense advice. No fluff.",
    question
))

# Persona 2: encouraging teacher
print("\n=== ENCOURAGING TEACHER ===")
print(ask_with_system(
    "You are a patient and encouraging programming teacher. You always motivate the student and celebrate their curiosity.",
    question
))

# Persona 3: high temperature = more creative/random
print("\n=== CREATIVE MODE (high temp) ===")
print(ask_with_system(
    "You are a creative writer who explains tech concepts through metaphors and stories.",
    question,
    temperature=1.2
))