from flask import Flask, render_template, request, send_file
from parser_1 import *
app = Flask(__name__,template_folder='templates')


@app.route('/download')
def download():
    filename = 'result.csv'
    return send_file(filename, as_attachment=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['input_data']
        processed_data = process_data(data)
        return processed_data
    else:
        return render_template('index.html')

def process_data(data):
    # здесь обрабатывайте данные
    parse(data)
    return download()

if __name__ == '__main__':
    app.run(host="0.0.0.0")