from os import environ
from flask import Flask, json, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
import requests, environment

app = Flask(__name__, template_folder='HTML_Templates',static_folder='Style')
app.secret_key = 'PNOISFUCKINGAWESOME'
app.permanent_session_lifetime = timedelta(days=0,hours=0,minutes=5)
TEMPLATES_AUTO_RELOAD = True

@app.route('/')
def home():
    return render_template('home.html')

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