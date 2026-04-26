import json
from flask import Flask, render_template, request, jsonify
from google import genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = genai.Client()
openai = OpenAI()


@app.route('/gpt')
def gpt():
    return render_template('gpt.html')

@app.route('/gpt', methods=['POST'])
def gpt_post():
    question = request.form['question']
    answer = request.form['answer']
    prompt = f"""Oceń, czy podana odpowiedź na pytanie jest poprawna.
Odpowiedź WYŁĄCZNIE poprawnym JSON-em, o strukturze: 
{{ "poprawna": true/false, "poprawna_odpowiedz": "..." lub null, "uzasadnienie": "..." }}
poprawna = true jeśli odpowiedź jest poprawna, lub false gdy niepoprawna,
poprawna_odpowiedz = prawidłowa odpowiedź jeśli była niepoprawna, w przeciwnym razie null,
uzasadnienie = krótkie wyjaśnienie w języku polskim.

Pytanie: {question}
Odpowiedź: {answer}
"""
    response = openai.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    data = json.loads(response.output_text)


    return render_template('gpt_result.html', question=question, answer=answer, data=data)

@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    history = data['history']
    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=history
    )
    return jsonify(answer=response.text)


@app.route('/old', methods=['GET', 'POST'])
def hello():
    answer = None
    history = []
    if request.method == 'POST':
        prompt = request.form['prompt']
        history = json.loads(request.form['history'])
        history.append({"role": "user", "parts": [{"text": prompt}]})

        response = client.models.generate_content(
            model="gemini-3-flash-preview", contents=history
        )
        answer = response.text
        history.append({"role": "model", "parts": [{"text": answer}]})

    return render_template('index.html', answer=answer,
                           history=history, history_json=json.dumps(history))

if __name__ == '__main__':
    app.run(debug=True)