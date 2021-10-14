# Importing Flask
from flask import Flask, render_template, redirect, url_for, request,session, flash
from datetime import timedelta
from flask_socketio import SocketIO, emit, send
# Defining different Flask-folders and names

app = Flask(__name__, template_folder='HTML_Templates',static_folder='Style')
app.secret_key = 'PNOISFUCKINGAWESOME'
app.permanent_session_lifetime = timedelta(days=0,hours=0,minutes=5)
TEMPLATES_AUTO_RELOAD = True
socketio = SocketIO(app)
# Defining different HTML pages with their corresponding app routes

# Main page
@app.route('/')
def home():
    return render_template('home.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

#Redirecting 'admin' page via a window with fixed variable
@app.route('/admin')
def admin():
    return redirect(url_for('user',variable='Admin'))

# Trying to make a functional button
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

# SocketIO implementation
@socketio.on('message')
def handle_message(msg):
    print('received message: ' + msg)


# Trying multiple scripts using Blueprint

# Making sure the app runs on startup
if __name__ == '__main__':
    socketio.run(app,debug=True)
