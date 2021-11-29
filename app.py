from uuid import uuid4

from flask import Flask, Response, render_template, request

app = Flask(__name__)
app.secret_key = uuid4().hex

@app.context_processor
def injectVariables():
    def firstLetterCap(s):
        return s.capitalize()
    return dict(loggedIn=True if request.cookies.get("jwt") else False, firstLetterCap=firstLetterCap)

db_url = "https://pno3cwa2.student.cs.kuleuven.be/api/task/add"

@app.after_request
def securityHeaders(response):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5000")
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:11000")
    response.headers.add("Access-Control-Allow-Origin", "https://pno3cwa1.student.cs.kuleuven.be")
    return response

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", title="404")

@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nDisallow: /", mimetype="text/plain")

@app.route('/math/integration',methods=['POST','GET'])
def integration():
    if request.method == 'POST':
        function = request.form['f']
        bg = request.form['bg']
        og = request.form['og']
        print(function,bg,og)
        if request.cookies.get('jwt'):
            r = requests.post(db_url, json={'operation': 'int', 'options': {'f': function, 'b': bg, 'a': og}},headers={'Authorization': 'Bearer '+request.cookies.get('jwt')})
        else:
            r = requests.post(db_url, json={'operation': 'int', 'options': {'f': function, 'b': bg, 'a': og}})
        n = r.json()
        taskid = n['task_id']
        return render_template('results/resultloading.html', taskid = taskid)
    return render_template('maths/integration.html')


@app.route('/math/differentiation',methods=['POST','GET'])
def differentiation():
    if request.method == 'POST':
        function = request.form['f']
        punt = request.form['og']
        orde = request.form['orde']
        if request.cookies.get('jwt'):
            r = requests.post(db_url, json={'operation': 'diff', 'options': {'f': function, 'a': punt, 'order': orde}},headers={'Authorization': 'Bearer '+request.cookies.get('jwt')})
        else:
            r = requests.post(db_url, json={'operation': 'diff', 'options': {'f': function, 'a': punt, 'order': orde}})
        n = r.json()
        taskid = n['task_id']
        return render_template('results/resultloading.html', taskid = taskid)
    return render_template('maths/differentiation.html')

@app.route('/math/optimization',methods=['POST','GET'])
def optimization():
    if request.method == 'POST':
        xlower = request.form['xl']
        xupper = request.form['xu']
        ylower = request.form['yl']
        yupper = request.form['yu']
        function = request.form['f']
        if xlower > xupper or ylower > yupper:
            flash('Lower X or Y limit was greater than upper X or Y limit! ')
            return redirect(url_for('optimization'))
        if request.cookies.get('jwt'):
            r = requests.post(db_url, json={'operation': 'opt', 'options': {'f': function, 'xu': xupper, 'xl': xlower, 'yu': yupper, 'yl': ylower}},headers={'Authorization': 'Bearer '+request.cookies.get('jwt')})
        else:
            r = requests.post(db_url, json={'operation': 'opt', 'options': {'f': function, 'xu': xupper, 'xl': xlower, 'yu': yupper, 'yl': ylower}})
        n = r.json()
        taskid = n['task_id']
        return render_template('results/resultloading.html', taskid = taskid)
    return render_template('maths/optimization.html')

@app.route('/math/lagrange_interpolation',methods=['POST','GET'])
def lagrange_interpolation():
    if request.method == 'POST':
        vectora = loads("[" + request.form['xval'] + "]")
        vectorb = loads("[" + request.form['yval'] + "]")
        print(vectora, vectorb)
        if request.cookies.get('jwt'):
            r = requests.post(db_url, json={'operation': 'lint', 'options': {'a': vectora, 'b': vectorb}},headers={'Authorization': 'Bearer '+request.cookies.get('jwt')})
        else:
            r = requests.post(db_url, json={'operation': 'lint', 'options': {'a': vectora, 'b': vectorb}})
        n = r.json()
        taskid = n['task_id']
        return render_template('results/resultloading.html', taskid = taskid)
    return render_template('maths/lagrange_interpolation.html')

@app.route('/math/taylor_approximation',methods=['POST','GET'])
def taylor_approximation():
    if request.method == 'POST':
        function = request.form['f']
        x0 = request.form['x']
        order = request.form['order']
        if request.cookies.get('jwt'):
            r = requests.post(db_url, json={'operation': 'taprox', 'options': {'f': function, 'x0': x0, 'order': order}},headers={'Authorization': 'Bearer '+request.cookies.get('jwt')})
        else:
            r = requests.post(db_url, json={'operation': 'taprox', 'options': {'f': function, 'x0': x0, 'order': order}})
        n = r.json()
        taskid = n['task_id']
        return render_template('results/resultloading.html', taskid = taskid)
    return render_template('maths/taylor_approximation.html')

@app.route('/status/<task_id>')
def status(task_id):
    if request.cookies.get('jwt'):
        r = requests.get("https://pno3cwa2.student.cs.kuleuven.be/api/task/status?task_id="+task_id, headers={'Authorization': 'Bearer '+request.cookies.get('jwt')})
    else:
        r = requests.get("https://pno3cwa2.student.cs.kuleuven.be/api/task/status?task_id="+task_id)
    n = r.json()
    operation = n['input_values']['operation']
    options = n['input_values']['options']
    result = n['result']
    if 'error' in n['result']:
        return 'There was an error running your task, No result found.'
    if operation == 'int':
        return render_template('results/resultintegral.html', options = options, result = result)
    if operation == 'diff':
        return render_template('results/resultdifferentiation.html', options = options, result = result)
    if operation == 'opt':
        return render_template('results/resultoptimization.html', options = options, result = result)
    if operation == 'lint':
        return render_template('results/resultlagrange_interpolation.html', options = options, result = result)
    if operation == 'taprox':
        return render_template('results/resulttaylor_approximation.html', options = options, result = result)
    if operation == 'heateq':
        return render_template('results/resultheat_equation.html', options = options, result = result)

@app.route('/math/heat_equation',methods=['POST','GET'])
def heat_equation():
    if request.method == 'POST':
        L_X = request.form['L_X']
        L_Y = request.form['L_Y']
        H = request.form['H']
        ALPHA = request.form['ALPHA']
        T = request.form['T']
        FPS = request.form['FPS']
        BC = request.form['BC']
        if request.cookies.get('jwt'):
            r = requests.post(db_url, json={'operation': 'heateq', 'options': {'L_X': L_X, 'L_Y': L_Y, 'H': H, 'ALPHA': ALPHA, 'T': T, 'FPS': FPS, 'BOUNDARY_CONDITION': BC}},headers={'Authorization': 'Bearer '+request.cookies.get('jwt')})
        else:
            r = requests.post(db_url, json={'operation': 'heateq', 'options': {'L_X': L_X, 'L_Y': L_Y, 'H': H, 'ALPHA': ALPHA, 'T': T, 'FPS': FPS, 'BOUNDARY_CONDITION': BC}})
        n = r.json()
        taskid = n['task_id']
        return render_template('results/resultloading.html', taskid = taskid)
    return render_template('maths/heat_equation.html')

@app.route('/user/history')
def history():
    if request.cookies.get('jwt'):
        r = requests.get('https://pno3cwa2.student.cs.kuleuven.be/api/user/tasks', headers={'Authorization': 'Bearer '+request.cookies.get('jwt')})
        n = r.json()
        if 'error' in n or 'detail' in n:
            flash(n['error'] if 'error' in n else n['detail'], 'error')
            return redirect(url_for('login'))
        return render_template('history.html', tasks=n['tasks'])
    return redirect(url_for('login'))

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

@app.route("/try_it")
def mogelijkheden():
    return render_template("mogelijkheden.html")

import routers.math, routers.users

if __name__ == '__main__':
    app.run()