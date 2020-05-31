#!/usr/bin/python3
''' Run app
'''
from flask import Flask, render_template, flash, redirect, request, url_for,\
    jsonify, abort
from datetime import datetime
from uuid import uuid4
from models.user import User
from models.role import Role
import json

app = Flask(__name__)
app.config.from_object('public.config')


@app.route('/')
def index():
   ''' render index.html '''
   cache = str(uuid4())
   emails = [email['email'] for email in User.readAll().values()]
   return render_template('index.html', cache=cache, emails=emails)


@app.route('/sign_up', methods=['POST'])
def sign_up():
    ''' 
    '''
    if request.method == 'POST':
        if request.form['password'] == request.form['verify']:
            role = Role.readAll()
            idRole = ''.join([rol['idRol'] for rol in role.values()])
            data = [
                idRole,
                request.form['username'],
                request.form['email'],
                request.form['password']
            ]
            user = User(*data)
            user.write()
        else:
            flash('The password do not equal')
    return redirect(url_for('index'))


@app.route('/emails', methods=['POST', 'GET'])
def email_validation():
    if request.method == 'GET':
        return redirect(url_for('index'))
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    if len(data) == 0:
        emails = [email['email'] for email in User.readAll().values()]
        return jsonify(emails)


@app.errorhandler(404)
def page_404(e):
    ''' 404 error
    '''
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
