from json import loads

from app import *
from app import app
from flask import flash, redirect, render_template, request, url_for
from modules.environment import DB_URL, WS_URL
from requests import get, post

from routers.users import *

@app.route("/math/differentiation", methods=["POST","GET"])
def differentiation():
    if request.method == "POST":
        payload = {
            "operation": "diff",
            "options": {
                "f": request.form["f"],
                "a": request.form["og"],
                "order": request.form["orde"]
            }
        }
        r = post(f"{DB_URL}/api/task/add", json=payload, headers={"Authorization": "Bearer " + request.cookies.get("jwt")} if request.cookies.get("jwt") else {}).json()
        return render_template("loading.html", taskid=r["task_id"], ws_url=WS_URL)
    return render_template("math/differentiation.html")

@app.route("/math/integration", methods=["POST","GET"])
def integration():
    if request.method == "POST":
        payload = {
            "operation": "int",
            "options": {
                "f": request.form["f"],
                "a": request.form["og"],
                "b": request.form["bg"]
            }
        }
        r = post(f"{DB_URL}/api/task/add", json=payload, headers={"Authorization": "Bearer " + request.cookies.get("jwt")} if request.cookies.get("jwt") else {}).json()
        return render_template("loading.html", taskid=r["task_id"], ws_url=WS_URL)
    return render_template("math/integration.html")

@app.route("/math/optimization", methods=["POST","GET"])
def optimization():
    if request.method == "POST":
        payload = {
            "operation": "opt",
            "options": {
                "f": request.form["f"],
                "xl": request.form["xl"],
                "xu": request.form["xu"],
                "yl": request.form["yl"],
                "yu": request.form["yu"]
            }
        }
        if float(payload["options"]["xl"]) > float(payload["options"]["xu"]) or float(payload["options"]["yl"]) > float(payload["options"]["yu"]):
            flash("Lower X or Y limit was greater than upper X or Y limit!")
            return redirect(url_for("optimization"))
        r = post(f"{DB_URL}/api/task/add", json=payload, headers={"Authorization": "Bearer " + request.cookies.get("jwt")} if request.cookies.get("jwt") else {}).json()
        return render_template("loading.html", taskid=r["task_id"], ws_url=WS_URL)
    return render_template("math/optimization.html")

@app.route("/math/lagrange_interpolation", methods=["POST","GET"])
def lagrange_interpolation():
    if request.method == "POST":
        payload = {
            "operation": "lint",
            "options": {
                "a": loads("[" + request.form["xval"] + "]"),
                "b": loads("[" + request.form["yval"] + "]")
            }
        }
        if len(payload["options"]["a"]) != len(payload["options"]["b"]):
            flash("Length of X- and Y-values must be equal!")
            return redirect(url_for("lagrange_interpolation"))
        r = post(f"{DB_URL}/api/task/add", json=payload, headers={"Authorization": "Bearer " + request.cookies.get("jwt")} if request.cookies.get("jwt") else {}).json()
        return render_template("loading.html", taskid=r["task_id"], ws_url=WS_URL)
    return render_template("math/lagrange_interpolation.html")

@app.route("/math/taylor_approximation", methods=["POST","GET"])
def taylor_approximation():
    if request.method == "POST":
        payload = {
            "operation": "taprox",
            "options": {
                "f": request.form["f"],
                "x0": request.form["x"],
                "order": request.form["order"]
            }
        }
        r = post(f"{DB_URL}/api/task/add", json=payload, headers={"Authorization": "Bearer " + request.cookies.get("jwt")} if request.cookies.get("jwt") else {}).json()
        return render_template("loading.html", taskid=r["task_id"], ws_url=WS_URL)
    return render_template("math/taylor_approximation.html")

@app.route("/math/heat_equation", methods=["POST","GET"])
def heat_equation():
    if request.method == "POST":
        payload = {
            "operation": "heateq",
            "options": {
                "L_X": request.form["L_X"],
                "L_Y": request.form["L_Y"],
                "H": request.form["H"],
                "T": request.form["T"],
                "FPS": request.form["FPS"],
                "BOUNDARY_CONDITION": request.form["BC"],
            }
        }
        r = post(f"{DB_URL}/api/task/add", json=payload, headers={"Authorization": "Bearer " + request.cookies.get("jwt")} if request.cookies.get("jwt") else {}).json()
        return render_template("loading.html", taskid=r["task_id"], ws_url=WS_URL)
    return render_template("math/heat_equation.html")

@app.route("/math/symdifferentiation", methods=["POST","GET"])
def symdifferentiation():
    if request.method == "POST":
        payload = {
            "operation": "symdiff",
            "options": {
                "f": request.form["f"],
                "o": request.form["orde"]
            }
        }
        r = post(f"{DB_URL}/api/task/add", json=payload, headers={"Authorization": "Bearer " + request.cookies.get("jwt")} if request.cookies.get("jwt") else {}).json()
        return render_template("loading.html", taskid=r["task_id"], ws_url=WS_URL)
    return render_template("math/symdifferentiation.html")

@app.route("/math/symintegration", methods=["POST","GET"])
def symintegration():
    if request.method == "POST":
        payload = {
            "operation": "symint",
            "options": {
                "f": request.form["f"]
            }
        }
        r = post(f"{DB_URL}/api/task/add", json=payload, headers={"Authorization": "Bearer " + request.cookies.get("jwt")} if request.cookies.get("jwt") else {}).json()
        return render_template("loading.html", taskid=r["task_id"], ws_url=WS_URL)
    return render_template("math/symintegration.html")

@app.route("/math/symlimit", methods=["POST","GET"])
def symlimit():
    if request.method == "POST":
        payload = {
            "operation": "symlimit",
            "options": {
                "f": request.form["f"],
                "x0": request.form["x0"],
                "dir": request.form["dir"]
            }
        }
        r = post(f"{DB_URL}/api/task/add", json=payload, headers={"Authorization": "Bearer " + request.cookies.get("jwt")} if request.cookies.get("jwt") else {}).json()
        return render_template("loading.html", taskid=r["task_id"], ws_url=WS_URL)
    return render_template("math/symlimit.html")

@app.route("/math/symsolve", methods=["POST","GET"])
def symsolve():
    if request.method == "POST":
        payload = {
            "operation": "symsolve",
            "options": {
                "f": request.form["f"]
            }
        }
        r = post(f"{DB_URL}/api/task/add", json=payload, headers={"Authorization": "Bearer " + request.cookies.get("jwt")} if request.cookies.get("jwt") else {}).json()
        return render_template("loading.html", taskid=r["task_id"], ws_url=WS_URL)
    return render_template("math/symsolve.html")

@app.route("/status/<task_id>")
def status(task_id):
    r = get(f"{DB_URL}/api/task/status?task_id="+task_id, headers={"Authorization": "Bearer "+request.cookies.get("jwt")} if request.cookies.get("jwt") else {})
    if r.ok:
        n = r.json()
        operation = n["input_values"]["operation"]
        options = n["input_values"]["options"]
        result = n["result"]
        if "error" in n["result"]:
            return "There was an error running your task, no result found."
        if operation == "diff":
            return render_template("result.html", operation="Differentiation",
            blocks={"Function": f"\({result['pstring']}\)", "Point": f"\({options['a']}\)", "Order": f"\({options['order']}\)", "Result": f"\({result['result']}\)", "Plot": f"<img src='{result['link']}' alt='Plot of the derivative' height='500' width='500'>"})
        if operation == "int":
            return render_template("result.html", operation="Integration",
            blocks={"Function": f"\({result['pstring']}\)", "Lower bound": f"\({options['a']}\)", "Upper bound": f"\({options['b']}\)", "Result": f"\({result['result']}\)", "Max error on result": f"\({result['err']}\)", "Plot": f"<img src='{result['link']}' alt='Integration of the given function' height='500' width='500'>"})
        if operation == "opt":
            return render_template("result.html", operation="Optimization",
            blocks={"Function": f"\({result['pstring']}\)", "Lower bound for x": f"\({options['xl']}\)", "Upper bound for x": f"\({options['xu']}\)", "Lower bound for y": f"\({options['yl']}\)", "Upper bound for y": f"\({options['yu']}\)", "Result coordinates": f"\(({result['vector'][0]}, {result['vector'][1]})\)", "Function evaluation at result": f"\({result['vector'][2]}\)"})
        if operation == "lint":
            return render_template("result.html", operation="Lagrange interpolation",
            blocks={"X-values": f"\({options['a']}\)", "Y-values": f"\({options['b']}\)", "Result": f"\({result['result']}\)", "Plot": f"<img src='{result['link']}' alt='Interpolation of the given function' height='500' width='500'>"})
        if operation == "taprox":
            return render_template("result.html", operation="Taylor approximation",
            blocks={"Function": f"\({result['pstring']}\)", "Point": f"\({options['x0']}\)", "Order": f"\({options['order']}\)", "Result": f"\({result['result']}\)", "Plot": f"<img src='{result['link']}' alt='Approximation of the Taylor polynomial' height='500' width='500'>"})
        if operation == "heateq":
            return render_template("result.html", operation="Heat equation",
            blocks={"Horizontal length": f"\({options['L_X']}\)", "Vertical length": f"\({options['L_Y']}\)", "Meshgrid step size": f"\({options['H']}\)", "Animation duration": f"\({options['T']}\)", "Animation FPS": f"\({options['FPS']}\)", "Boundary condition": options['BOUNDARY_CONDITION'], "Animation": f"<img src='{result['link']}' alt='Animation of the heat distribution' height='500' width='500'>"})
        if operation == "symdiff":
            return render_template("result.html", operation="Differentiation",
            blocks={"Function": f"\({result['pstring']}\)", "Order": f"\({options['o']}\)", "Result": f"\({result['result']}\)"})
        if operation == "symint":
            return render_template("result.html", operation="Integration",
            blocks={"Function": f"\({result['pstring']}\)", "Result": f"\({result['result']}\)"})
        if operation == "symlimit":
            return render_template("result.html", operation="Limits",
            blocks={"Function": f"\({result['pstring']}\)", "X0": f"\({options['x0']}\)", "Direction": f"\({options['dir']}\)", "Result": f"\({result['result']}\)"})
        if operation == "symsolve":
            return render_template("result.html", operation="Roots",
            blocks={"Function": f"\({result['pstring']}\)", "Result": "<li>\(" + "\)</li><li>\(".join(result['result']) + "\)</li>"})
    return "Unauthorized"
