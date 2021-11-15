import json
import threading
import time
from uuid import uuid4

import requests

from flask import (Flask, Response, flash, json, make_response,
                   render_template, request, url_for)

app = Flask(__name__)
app.secret_key = uuid4().hex

@app.context_processor
def injectVariables():
    def firstLetterCap(s):
        return s.capitalize()
    return dict(loggedIn=True if request.cookies.get("jwt") else False, firstLetterCap=firstLetterCap)

# def refresh():
#     threading.Timer(5, refresh).start()
#     dataBase = requests.get('https://pno3cwa2.student.cs.kuleuven.be/api/scheduler/status/beveren').json()
#     global statusBeveren
#     statusBeveren = dataBase['beveren']

@app.after_request
def securityHeaders(response):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5000")
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:11000")
    response.headers.add("Access-Control-Allow-Origin", "https://pno3cwa1.student.cs.kuleuven.be")
    return response

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/')
@app.route('/openfoam')
def openfoam():
    return render_template('openfoam.html')

@app.route('/maths/differentiation')
def maths():
    return render_template('maths/differentiation.html')

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", title="404")

@app.route('/robots.txt')
def robots():
    return Response("User-agent: *\nDisallow: /", mimetype="text/plain")


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
            return render_template('maths/function.html')
        else:
            if request.cookies.get('jwt'):
                r = requests.post('https://pno3cwa2.student.cs.kuleuven.be/api/task/add', json={1: [X1,Y1], 2: [X2,Y2], 3: [X3,Y3], 4: [X4,Y4]},headers={'Authorization': 'Bearer '+request.cookies.get('jwt')})
            else:
                r = requests.post('https://pno3cwa2.student.cs.kuleuven.be/api/task/add',json={1: [X1, Y1], 2: [X2, Y2], 3: [X3, Y3], 4: [X4, Y4]})
            if r.ok:
                n = r.json()
                start = time.time_ns()
                while True:
                    if request.cookies.get('jwt'):
                        jsonData=requests.get(f'https://pno3cwa2.student.cs.kuleuven.be/api/task/status/{[i for i in n][0]}',headers={'Authorization': 'Bearer '+request.cookies.get('jwt')}).json()
                    else:
                        jsonData=requests.get(f'https://pno3cwa2.student.cs.kuleuven.be/api/task/status/{[i for i in n][0]}').json()
                    state = jsonData[[i for i in n][0]]['status']
                    if state==1:
                        break
                    if time.time_ns() - start < 30*1e9:
                        time.sleep(0.35)
                    else:
                        time.sleep(1)
                a, b, c, d = [round(num, 3) for num in json.loads(jsonData[[i for i in n][0]]['result'])]
            return render_template('results/result.html', avar=a, bvar=b, cvar=c, dvar=d)
    return render_template('maths/function.html')

@app.route('/math/integral',methods=['POST','GET'])
def integral():
    if request.method == 'POST':
        function = request.form['f']
        bg = request.form['bovengrens']
        og = request.form['ondergrens']
        if request.cookies.get('jwt'):
            r = requests.post('http://eeklo.cs.kotnet.kuleuven.be:12000/num_math/integration', json={'operation': 'int', 'options': {'f': function, 'b': bg, 'a': og}},headers={'Authorization': 'Bearer '+request.cookies.get('jwt')})
        else:
            r = requests.post('http://eeklo.cs.kotnet.kuleuven.be:12000/num_math/integration', json={'operation': 'int', 'options': {'f': function, 'b': bg, 'a': og}})
        if r.ok:
            n = r.json()
            result = n['result']
            error = n['error']
            #lol
            return render_template('results/resultintegral.html', result=result, error=error)
    return render_template('maths/integration.html')


@app.route('/gif')
def gif():
    return render_template('giftest.html')
# Dit is een test

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email=request.form['email']
        pswd=request.form['password']
        r = requests.post('https://pno3cwa2.student.cs.kuleuven.be/api/user/auth', json={'email': email, 'password': pswd})
        if r.ok:
            n = r.json()
            if 'error' in n:
                flash(n['error'], 'error')
                return render_template('login.html')
            else:
                resp = make_response()
                resp.set_cookie('jwt',value=n['jwt'])
                resp.headers.add('location', url_for('home'))
                return resp, 302
    return render_template('login.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        pswd = request.form['password']
        r = requests.post('https://pno3cwa2.student.cs.kuleuven.be/api/user/add', json={'email': email, 'password': pswd})
        if r.ok:
            n = r.json()
            if 'error' in n:
                flash(n['error'], 'error')
                return render_template('register.html')
            else:
                resp = make_response()
                resp.set_cookie('jwt', value=n['jwt'])
                resp.headers.add('location', url_for('home'))
                return resp, 302
    return render_template('register.html')

@app.route('/logout')
def logout():
    resp = make_response()
    resp.set_cookie('jwt', '', expires=0)
    resp.headers.add('location', url_for('home'))
    return resp, 302

app.run(debug=True)