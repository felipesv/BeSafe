#!/usr/bin/python3
''' Run app
'''
from flask import Flask, render_template, flash, redirect, request, url_for,\
    jsonify, abort, session
from flask_bcrypt import Bcrypt
from uuid import uuid4
from models.user import User
from models.role import Role
from models.alert_type import Alerttype
from models.stadistics import Stadistics
from models.aggressor import Aggressor
from models.collective_group import Collectivegroup
from models.neighborhood import Neighborhood
from models.notification import Notification
from models.alerts import Alert
from models.stage import Stage
from models.reports import Reports
from models.mapping import Mapping
from models.contact import Contact
from public.forms import SignUp, LogIn, Report
import json
import os


app = Flask(__name__)
app.config.from_object('public.config')
app.secret_key = bytes(str(os.getenv('BESAFE_SECRETKEY')), encoding='utf-8')
app.url_map.strict_slashes = False
bcrypt = Bcrypt(app)


urlfor = os.getenv('BESAFE_URL')

@app.route('/')
@app.route('/index')
def index():
    ''' render index.html '''
    cache = str(uuid4())
    signUp = SignUp(request.form)
    logIn = LogIn(request.form)
    session['message'] = ''
    return render_template('index.html', cache=cache, signUp=signUp, logIn=logIn)


@app.route('/sign_up', methods=['POST'])
def sign_up():
    ''' 
    '''
    signUp = SignUp(request.form)
    if request.method == 'POST' and signUp.validate():
        role = Role.readAll()
        idRole = ''.join([rol['idRol'] for rol in role.values() 
                          if rol['description'] == 'Usuario'])
        password = bcrypt.generate_password_hash(request.form['password'], 10).decode('utf-8')
        data = [
            idRole,
            request.form['name'],
            request.form['email'],
            password
        ]
        user = User(*data)
        user.write()
        return redirect(request.referrer)
    # TODO: Handler errors
    """ 
    Implement here
    """
    return render_template('index.html', signUp=signUp)


@app.route('/emails', methods=['POST', 'GET'])
def email_validation():
    if request.method == 'GET':
        return redirect(urlfor +  'index')
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    if len(data) == 0:
        emails = [email['email'] for email in User.readAll().values()]
        return jsonify(emails)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = LogIn(request.form)
    if request.method == 'POST' and login.validate():
        user = User.getUser(login.email.data)
        if user is False:
            flash('Usuario no registrado')
            return redirect(request.referrer)
        confirm = bcrypt.check_password_hash(user['password'],\
            request.form['password'])
        if confirm == False:
            flash('Email y/o contraseña invalidos')
            # TODO: Handler errors
            return redirect(request.referrer)
        session['user'] = user['idUser']
        session['name'] = user['name'].upper()
    return redirect(request.referrer)


@app.route('/logout', methods=['GET'])
def logout():
    if request.referrer == None:
        return redirect(urlfor + 'index')
    [session.pop(key) for key in list(session.keys())]
    return redirect(request.referrer)


@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if 'user' not in session:
        return redirect(urlfor + 'index')
    signUp = SignUp(request.form)
    logIn = LogIn(request.form)
    report = Report(request.form)
    cache = str(uuid4())
    violences = Alerttype.readAll()
    aggressors = Aggressor.readAll()
    collectives = Collectivegroup.readAll()
    stages = Stage.readAll()
    return render_template('reports.html', signUp=signUp, logIn=logIn, report=report, cache=cache,
    violences=violences, aggressors=aggressors, collectives=collectives, stages=stages)


@app.route('/create_report', methods=['POST'])
def create_report():
    userid = session['user']
    if not User.validUserId(userid):
        session['message']='invalid-user'
        return redirect(urlfor + 'reports')
    try:
        notification = Notification('Sin notificacion')
        notification.write()
        alert = Alert('Sin alerta', notification.idNotification)
        alert.write()
        report = Reports(
            alert.idAlert,
            request.form['description'],
            request.form['neighborhood'],
            request.form['stage'],
            request.form['aggressor'],
            request.form['complaint'],
            request.form['collective'],
            userid
        )
        report.write()
        mapping = Mapping(
            report.idReport,
            request.form['alertType'],
            float(request.form['latitude']),
            float(request.form['longitude']),
            userid
        )
        mapping.write()
    except Exception:
        session['message']='error'
        return redirect(urlfor + 'reports')
    session['message']='success'
    return redirect(urlfor + 'reports')


@app.route('/map', methods=['GET', 'POST'])
def map():
    signUp = SignUp(request.form)
    logIn = LogIn(request.form)
    cache = str(uuid4())
    dataAlertType = Alerttype.readAll()
    session['message'] = ''
    return render_template('map.html', signUp=signUp, logIn=logIn, cache=cache, dataAlertType=dataAlertType)


@app.route('/about', methods=['GET', 'POST'])
def about():
    signUp = SignUp(request.form)
    logIn = LogIn(request.form)
    cache = str(uuid4())
    return render_template('about.html', signUp=signUp, logIn=logIn, cache=cache)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    signUp = SignUp(request.form)
    logIn = LogIn(request.form)
    cache = str(uuid4())
    return render_template('contact.html', signUp=signUp, logIn=logIn, cache=cache)


@app.route('/help', methods=['GET', 'POST'])
def help():
    signUp = SignUp(request.form)
    logIn = LogIn(request.form)
    cache = str(uuid4())
    return render_template('help.html', signUp=signUp, logIn=logIn, cache=cache)


@app.route('/help_form', methods=['POST'])
def help_form():
    newContact = Contact(
        request.form['name'],
        request.form['city'],
        request.form['email'],
        request.form['message']
    )
    newContact.write()
    return redirect(urlfor + 'index')

@app.route('/stadistic', methods=['POST'])
def stadistic_comuna():
    return jsonify(Stadistics.stadisticsByComuna(request.form.get("idComuna")))


@app.errorhandler(404)
def page_404(e):
    ''' 404 error
    '''
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
