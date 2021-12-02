from json import loads

from app import *
from app import app
from flask import flash, redirect, render_template, request, url_for
from modules.environment import DB_URL, WS_URL
from requests import get, post

from routers.users import *

@app.route("/math/differentiation",methods=["POST","GET"])
def differentiation():
    if request.method == "POST":
        function = request.form["f"]
        punt = request.form["og"]
        orde = request.form["orde"]
        if request.cookies.get("jwt"):
            r = post(f"{DB_URL}/api/task/add", json={"operation": "diff", "options": {"f": function, "a": punt, "order": orde}},headers={"Authorization": "Bearer "+request.cookies.get("jwt")})
        else:
            r = post(f"{DB_URL}/api/task/add", json={"operation": "diff", "options": {"f": function, "a": punt, "order": orde}})
        n = r.json()
        taskid = n["task_id"]
        return render_template("result/loading.html", taskid = taskid, ws_url = WS_URL)
    return render_template("math/differentiation.html")

@app.route("/math/integration",methods=["POST","GET"])
def integration():
    if request.method == "POST":
        function = request.form["f"]
        bg = request.form["bg"]
        og = request.form["og"]
        if request.cookies.get("jwt"):
            r = post(f"{DB_URL}/api/task/add", json={"operation": "int", "options": {"f": function, "b": bg, "a": og}},headers={"Authorization": "Bearer "+request.cookies.get("jwt")})
        else:
            r = post(f"{DB_URL}/api/task/add", json={"operation": "int", "options": {"f": function, "b": bg, "a": og}})
        n = r.json()
        taskid = n["task_id"]
        return render_template("result/loading.html", taskid = taskid, ws_url = WS_URL)
    return render_template("math/integration.html")

@app.route("/math/optimization",methods=["POST","GET"])
def optimization():
    if request.method == "POST":
        xlower = request.form["xl"]
        xupper = request.form["xu"]
        ylower = request.form["yl"]
        yupper = request.form["yu"]
        function = request.form["f"]
        print(xlower,xupper,ylower,yupper,function)
        if float(xlower) > float(xupper) or float(ylower) > float(yupper):
            flash("Lower X or Y limit was greater than upper X or Y limit! ")
            return redirect(url_for("optimization"))
        if request.cookies.get("jwt"):
            r = post(f"{DB_URL}/api/task/add", json={"operation": "opt", "options": {"f": function, "xu": xupper, "xl": xlower, "yu": yupper, "yl": ylower}},headers={"Authorization": "Bearer "+request.cookies.get("jwt")})
        else:
            r = post(f"{DB_URL}/api/task/add", json={"operation": "opt", "options": {"f": function, "xu": xupper, "xl": xlower, "yu": yupper, "yl": ylower}})
        n = r.json()
        taskid = n["task_id"]
        return render_template("result/loading.html", taskid = taskid, ws_url = WS_URL)
    return render_template("math/optimization.html")

@app.route("/math/lagrange_interpolation",methods=["POST","GET"])
def lagrange_interpolation():
    if request.method == "POST":
        vectora = loads("[" + request.form["xval"] + "]")
        vectorb = loads("[" + request.form["yval"] + "]")
        print(vectora, vectorb)
        if request.cookies.get("jwt"):
            r = post(f"{DB_URL}/api/task/add", json={"operation": "lint", "options": {"a": vectora, "b": vectorb}},headers={"Authorization": "Bearer "+request.cookies.get("jwt")})
        else:
            r = post(f"{DB_URL}/api/task/add", json={"operation": "lint", "options": {"a": vectora, "b": vectorb}})
        n = r.json()
        taskid = n["task_id"]
        return render_template("result/loading.html", taskid = taskid, ws_url = WS_URL)
    return render_template("math/lagrange_interpolation.html")

@app.route("/math/taylor_approximation",methods=["POST","GET"])
def taylor_approximation():
    if request.method == "POST":
        function = request.form["f"]
        x0 = request.form["x"]
        order = request.form["order"]
        if request.cookies.get("jwt"):
            r = post(f"{DB_URL}/api/task/add", json={"operation": "taprox", "options": {"f": function, "x0": x0, "order": order}},headers={"Authorization": "Bearer "+request.cookies.get("jwt")})
        else:
            r = post(f"{DB_URL}/api/task/add", json={"operation": "taprox", "options": {"f": function, "x0": x0, "order": order}})
        n = r.json()
        taskid = n["task_id"]
        return render_template("result/loading.html", taskid = taskid, ws_url = WS_URL)
    return render_template("math/taylor_approximation.html")

@app.route("/math/heat_equation",methods=["POST","GET"])
def heat_equation():
    if request.method == "POST":
        L_X = request.form["L_X"]
        L_Y = request.form["L_Y"]
        H = request.form["H"]
        T = request.form["T"]
        FPS = request.form["FPS"]
        BC = request.form["BC"]
        if request.cookies.get("jwt"):
            r = post(f"{DB_URL}/api/task/add", json={"operation": "heateq", "options": {"L_X": L_X, "L_Y": L_Y, "H": H, "T": T, "FPS": FPS, "BOUNDARY_CONDITION": BC}},headers={"Authorization": "Bearer "+request.cookies.get("jwt")})
        else:
            r = post(f"{DB_URL}/api/task/add", json={"operation": "heateq", "options": {"L_X": L_X, "L_Y": L_Y, "H": H, "T": T, "FPS": FPS, "BOUNDARY_CONDITION": BC}})
        n = r.json()
        taskid = n["task_id"]
        return render_template("result/loading.html", taskid = taskid, ws_url = WS_URL)
    return render_template("math/heat_equation.html")

@app.route("/status/<task_id>")
def status(task_id):
    if request.cookies.get("jwt"):
        r = get(f"{DB_URL}/api/task/status?task_id="+task_id, headers={"Authorization": "Bearer "+request.cookies.get("jwt")})
    else:
        r = get(f"{DB_URL}/api/task/status?task_id="+task_id)
    n = r.json()
    operation = n["input_values"]["operation"]
    options = n["input_values"]["options"]
    result = n["result"]
    if "error" in n["result"]:
        return "There was an error running your task, no result found."
    if operation == "diff":
        return render_template("result/differentiation.html", options = options, result = result)
    if operation == "int":
        return render_template("result/integration.html", options = options, result = result)
    if operation == "opt":
        return render_template("result/optimization.html", options = options, result = result)
    if operation == "lint":
        return render_template("result/lagrange_interpolation.html", options = options, result = result)
    if operation == "taprox":
        return render_template("result/taylor_approximation.html", options = options, result = result)
    if operation == "heateq":
        return render_template("result/heat_equation.html", options = options, result = result)