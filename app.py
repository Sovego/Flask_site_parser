from parser_1 import parse

from flask import Flask, render_template, request, send_file


app = Flask(__name__, template_folder='templates')


@app.route('/download')
def download():
    return send_file('result.csv', as_attachment=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method != 'POST':
        return render_template('index.html')
    data = request.form['input_data']
    return process_data(data)


def process_data(data):
    parse(data)
    return download()


if __name__ == '__main__':
    app.run(host="0.0.0.0")
