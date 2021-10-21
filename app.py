from os import environ
from flask import Flask, json, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
import requests, environment
import time
import threading
import json


app = Flask(__name__, template_folder='html_templates',static_folder='static')
app.secret_key = 'PNOISFUCKINGAWESOME'
app.permanent_session_lifetime = timedelta(days=0,hours=0,minutes=5)
TEMPLATES_AUTO_RELOAD = True
dataBase = {}

def refresh():
    threading.Timer(5, refresh).start()
    dataBase = requests.get('https://pno3cwa2.student.cs.kuleuven.be/api/scheduler/status/beveren').json()
    global statusBeveren
    statusBeveren = dataBase['beveren']



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/status')
def status():
    return render_template('status.html',status_beveren=statusBeveren)

@app.route('/function',methods=['POST','GET'])
def function():
    if request.method == 'POST':
        X1 = request.form['X1']
        Y1 = request.form['Y1']
        X2 = request.form['X2']
        Y2 = request.form['Y2']
        X3 = request.form['X3']
        Y3 = request.form['Y3']
        X4 = request.form['X4']
        Y4 = request.form['Y4']
        print(X1,X2,X3,X4,Y1,Y2,Y3,Y4)
        if X1==X2 or X1==X3 or X1==X4 or X2==X3 or X2==X4 or X3==X4:
            flash('Wrong input! (2 or more points have same X-value)','error')
            return render_template('function.html')
        else:
            r = requests.post('https://pno3cwa2.student.cs.kuleuven.be/api/task/add', json={1: [X1,Y1], 2: [X2,Y2], 3: [X3,Y3], 4: [X4,Y4]})
            if r.ok:
                n = r.json()
                start = time.time_ns()
                while True:
                    jsonData = requests.get(f'https://pno3cwa2.student.cs.kuleuven.be/api/task/status/{[i for i in n][0]}').json()
                    state = jsonData[[i for i in n][0]]['status']
                    if state==1:
                        break
                    if time.time_ns() - start > 30000000000:
                        time.sleep(0.4)
                    else:
                        time.sleep(1)
                a, b, c, d = [round(num, 3) for num in json.loads(jsonData[[i for i in n][0]]['result'])]
            return render_template('functionresult.html',avar=a,bvar=b,cvar=c,dvar=d)
    return render_template('function.html')





@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    return redirect(url_for('user',variable='Admin'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = False
        user = request.form['username']
        session['user'] =user
        flash('Login succesful!')
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            flash('Already logged In!')
            return redirect(url_for('user'))
        else:
            flash('You are not logged in!')
            return render_template('login.html')

@app.route('/user', methods=['POST','GET'])
def user():
    email = None
    if 'user' in session:
        user = session['user']
        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email
        else:
            if 'email' in session:
                email = session['email']
        return render_template('user.html', email = email)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        flash('You have been logged out!', 'info')
    session.pop('user', None)
    session.pop('email', None)
    return redirect(url_for('login'))
