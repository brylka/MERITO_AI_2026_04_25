from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        p = request.form['prompt']
        print(f"Użytkownik wpisał: {p}")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)