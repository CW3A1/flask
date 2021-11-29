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

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/try_it")
def mogelijkheden():
    return render_template("mogelijkheden.html")

from routers.math import *
from routers.users import *

if __name__ == '__main__':
    app.run()