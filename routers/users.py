from app import *
from app import app
from datetime import datetime, timedelta, timezone
from flask import (flash, make_response, redirect, render_template, request,
                   url_for)
from modules.environment import db_url
from requests import get, post

from routers.math import *


@app.route("/user/history")
def history():
    if request.cookies.get("jwt"):
        r = get(f"{db_url}/api/user/tasks", headers={"Authorization": "Bearer "+request.cookies.get("jwt")})
        n = r.json()
        if "error" in n or "detail" in n:
            flash(n["error"] if "error" in n else n["detail"], "error")
            return redirect(url_for("login"))
        return render_template("history.html", tasks=n["tasks"])
    return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email=request.form["email"]
        pswd=request.form["password"]
        r = post(f"{db_url}/api/user/auth", json={"email": email, "password": pswd})
        if r.ok:
            n = r.json()
            if "error" in n:
                flash(n["error"], "error")
                return render_template("login.html")
            else:
                resp = make_response()
                resp.set_cookie("jwt",value=n["jwt"],expires= datetime.now(tz=timezone.utc) + timedelta(days=1))
                resp.headers.add("location", url_for("home"))
                return resp, 302
    return render_template("login.html")

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        pswd = request.form["password"]
        r = post(f"{db_url}/api/user/add", json={"email": email, "password": pswd})
        if r.ok:
            n = r.json()
            if "error" in n:
                flash(n["error"], "error")
                return render_template("register.html")
            else:
                resp = make_response()
                resp.set_cookie("jwt", value=n["jwt"])
                resp.headers.add("location", url_for("home"))
                return resp, 302
    return render_template("register.html")

@app.route("/logout")
def logout():
    resp = make_response()
    resp.set_cookie("jwt", "", expires=0)
    resp.headers.add("location", url_for("home"))
    return resp, 302
