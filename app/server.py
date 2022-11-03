import json
from datetime import datetime
from fileinput import filename

from flask import Flask, request, send_file, redirect
from cripto import CriptoServer, SymmetricCripto
from http import HTTPStatus

app = Flask(__name__)

key_path = './keys'
cripto = CriptoServer(key_path)

@app.route('/')
def echo():
    return redirect('https://github.com/Impact-Plataform/ingress-test', code=302)
           

@app.route('/apply', methods=['POST'])
def post_apply():
    try:
        id = request.headers['id']

        info = json.loads(request.json['info'])
        info['name'] = cripto.decrypt(info['name'])
        info['email'] = cripto.decrypt(info['email'])
        info['phone'] = cripto.decrypt(info['phone'])
        info['essay'] = SymmetricCripto.decrypt(id, info['essay'])

        now = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f"./etc/apply_{id}_{now}"
        with open(file_name, 'w') as f:
            f.write(json.dumps(info))

    except Exception as e:
        print(f"/apply -> Exception: {str(e)}")
        return {
                   'msg': str(e),
                   'timestamp': datetime.now()
               }, HTTPStatus.UNPROCESSABLE_ENTITY

    return {
               'msg': 'accepted!',
               'timestamp': datetime.now()
           }, HTTPStatus.OK


@app.route('/key', methods=['GET', 'POST'])
def get_pub_key():
    try:
        return send_file(f"../{cripto.get_public_path()}", as_attachment=True)
    except FileNotFoundError as e:
        print(f"/key -> Exception: {str(e)}")
        return {
                   'msg': e,
                   'timestamp': datetime.now()
               }, HTTPStatus.NOT_FOUND
