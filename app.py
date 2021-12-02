from datetime import datetime
from uuid import uuid4

from requests import get

from flask import Flask, Response, render_template, request
from modules.environment import DB_URL

app = Flask(__name__)
app.secret_key = uuid4().hex

@app.context_processor
def injectVariables():
    def humanReadableTime(nanotime):
        dt = datetime.fromtimestamp(nanotime // 1000000000)
        s = dt.strftime('%Y-%m-%d %H:%M:%S')
        return s
    return dict(loggedIn=True if request.cookies.get("jwt") else False, humanReadableTime=humanReadableTime)

@app.after_request
def securityHeaders(response):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5000")
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:11000")
    response.headers.add("Access-Control-Allow-Origin", "https://pno3cwa1.student.cs.kuleuven.be")
    return response

@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nDisallow: /", mimetype="text/plain")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logs')
def logs():
    log_list = get(f"{DB_URL}/api/logs/view").json()
    return render_template('logs.html', log_list=log_list)

@app.route("/try_it")
def mogelijkheden():
    return render_template("mogelijkheden.html")

from routers.math import *
from routers.users import *

if __name__ == '__main__':
    app.run()
