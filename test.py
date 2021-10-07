from flask import Flask, render_template

app = Flask(__name__, template_folder='HTML_Templates',static_folder='Style')
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run()
