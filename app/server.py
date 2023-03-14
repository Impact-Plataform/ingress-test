import sqlite3
import json
from datetime import datetime
from flask import Flask, request, send_file, redirect, render_template
from cripto import CriptoServer, SymmetricCripto
from http import HTTPStatus
from flask_mail import Mail, Message
import os
from os.path import dirname, abspath


app = Flask(__name__, template_folder='templates')

key_path = './keys'
cripto = CriptoServer(key_path)


@app.route('/')
def echo():
    return redirect('https://github.com/Impact-Plataform/ingress-test', code=302)


@app.route('/apply', methods=['POST'])
def post_apply():
    try:
        connection = sqlite3.connect('applications.db')
        c = connection.cursor()

        apply_id = request.headers['id']
        info = {
            'name': cripto.decrypt(request.json['name']),
            'email': cripto.decrypt(request.json['email']),
            'phone': cripto.decrypt(request.json['phone']),
            'essay': SymmetricCripto.decrypt(apply_id, request.json['essay'])
        }

        print(f"/apply -> Receved: {json.dumps(info)}")

        now = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f"./etc/apply_{apply_id}_{now}"
        with open(file_name, 'w') as f:
            f.write(json.dumps(info))
        print(f"/apply -> Saved: {file_name}")
        print("Inseting into database")
        c.execute('''
                   INSERT INTO applications (apply_id, name, email, phone, essay)
                   VALUES (?, ?, ?, ?, ?)
               ''', (apply_id, info['name'], info['email'], info['phone'], info['essay']))
        connection.commit()
        connection.close()
        print("Finished!")

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


@app.route('/list', methods=['GET'])
def get_list():
    try:
        conn = sqlite3.connect('applications.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM applications')
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data = []
        for row in rows:
            data.append(dict(zip(columns, row)))
        conn.close()
        return render_template('list.html', data=data)
    except Exception as e:
        print(f"/list -> Exception: {str(e)}")
        return {
            'msg': str(e),
            'timestamp': datetime.now()
        }, HTTPStatus.UNPROCESSABLE_ENTITY


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
