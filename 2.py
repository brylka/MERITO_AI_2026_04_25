from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = genai.Client()

@app.route('/', methods=['GET', 'POST'])
def hello():
    answer = None
    if request.method == 'POST':
        p = request.form['prompt']

        response = client.models.generate_content(
            model="gemini-3-flash-preview", contents=p
        )
        answer = response.text

    return render_template('index.html', answer=answer)

if __name__ == '__main__':
    app.run(debug=True)