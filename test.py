# Importing Flask
from flask import Flask, render_template, redirect, url_for

# Defining different Flask-folders and names
app = Flask(__name__, template_folder='HTML_Templates',static_folder='Style')

# Defining different HTML pages with their corresponding app routes
# Main page
@app.route('/')
def home():
    return render_template('home.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

#Redirecting 'admin' page
@app.route('/admin')
def admin():
    return redirect(url_for('home'))

# Making sure the app runs on startup
if __name__ == '__main__':
    app.run()
