import requests

file_path = r"C:/Users/azizf/Downloads/Muslim_Habit_Full_Specification.pdf"  # ← change this

with open(file_path, "rb") as f:
    response = requests.post(
        "http://localhost:8000/upload",
        files={"file": (file_path.split("\\")[-1], f, "application/pdf")}
    )

print("Status:", response.status_code)
print("Response:", response.json())