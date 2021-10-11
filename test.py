# Importing Flask
from flask import Flask, render_template, redirect, url_for, request,session
from datetime import timedelta
# Defining different Flask-folders and names
app = Flask(__name__, template_folder='HTML_Templates',static_folder='Style')
app.secret_key = 'PNOISFUCKINGAWESOME'
app.permanent_session_lifetime = timedelta(days=0,hours=0,minutes=5)
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
        session.permanent = True
        user = request.form['naam']
        session['user'] =user
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            return redirect(url_for('user'))
        else:
            return render_template('login.html')
@app.route('/user')
def user():
    if 'user' in session:
        user = session['user']
        return f'<h1>{user}</h1>'
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
# Making sure the app runs on startup
if __name__ == '__main__':
    app.run(debug=True)
