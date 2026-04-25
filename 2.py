from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = genai.Client()
history = []

@app.route('/', methods=['GET', 'POST'])
def hello():
    answer = None
    if request.method == 'POST':
        p = request.form['prompt']
        history.append({"role": "user", "parts": [{"text": p}]})

        response = client.models.generate_content(
            model="gemini-3-flash-preview", contents=history
        )
        answer = response.text
        history.append({"role": "model", "parts": [{"text": answer}]})

    return render_template('index.html', answer=answer)

if __name__ == '__main__':
    app.run(debug=True)