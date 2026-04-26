import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

question = input("Wprowadź putanie: ")
answer = input("Wprowadź odpowiedź: ")

prompt = f"""Oceń, czy podana odpowiedź na pytanie jest poprawna.
Odpowiedź WYŁĄCZNIE poprawnym JSON-em, o strukturze: 
{{ "poprawna": true/false, "poprawna_odpowiedz": "..." lub null, "uzasadnienie": "..." }}
poprawna = true jeśli odpowiedź jest poprawna, lub false gdy niepoprawna,
poprawna_odpowiedz = prawidłowa odpowiedź jeśli była niepoprawna, w przeciwnym razie null,
uzasadnienie = krótkie wyjaśnienie w języku polskim.
 
Pytanie: {question}
Odpowiedź: {answer}
"""

response = client.responses.create(
    model="gpt-5.5",
    input=prompt
)

#print(response.output_text)

data = json.loads(response.output_text)
if data["poprawna"]:
    print("Odpowiedź poprawna.")
else:
    print("Odpowiedź błędna.")
    print(f"Poprawna odpowiedź: {data['poprawna_odpowiedz']}")
print(f"Uzasadnienie: {data['uzasadnienie']}")