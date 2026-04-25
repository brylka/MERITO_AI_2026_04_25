import json

from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = genai.Client()


@app.route('/')
def chat():
    return render_template('chat.html')






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