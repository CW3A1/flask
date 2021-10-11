from flask import Blueprint, render_template

second = Blueprint('second', __name__, template_folder='HTML_Templates', static_folder='Style')

@second.route('/osso')
@second.route('/')
def home():
    return render_template('home.html')