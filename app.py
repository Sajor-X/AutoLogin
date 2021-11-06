import json

from flask import Flask
from flask_cors import CORS
from flask import request

from captcha.verify import Verify

app = Flask(__name__)
CORS(app)


@app.route('/login_url', methods=['GET', 'POST'])
def login_url():
    v = Verify()
    if request.method == 'POST':
        url = request.form['url']
        return v.get_captcha_code(url)


@app.route('/login_base', methods=['GET', 'POST'])
def login_base():
    v = Verify()
    if request.method == 'POST':
        request_data = request.get_data().decode('utf-8')
        data = json.loads(request_data)
        file = v.get_file(data.get("base64"))
        count = 1 if not data.get("count") else data.get("count")
        threshold = 240 if not data.get("threshold") else data.get("threshold")
        return v.denoising_ocr(file, threshold, count)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

