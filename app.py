from flask import Flask
from flask_cors import CORS
from flask import request

from captcha.verify import Verify

app = Flask(__name__)
CORS(app)


@app.route('/login', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        url = request.form['url']
        v = Verify()
        code = v.get_captcha_code(url)
        print(code)
        return code


if __name__ == '__main__':
    app.run()