from app import app
from flask import render_template, jsonify, request, make_response, redirect
from app import calculate
from app import db_operations


@app.route("/", methods=["GET"])
def view_home():
    data = {'r_error': "",
            's_error': "",
            's_login': "",
            'r_name': "",
            'r_email': "",
            }
    return render_template("public/index.html", data=data)


@app.route("/register", methods=["POST"])
def register():
    error = ""
    if request.form["r_name"] == "":
        error += "Vardas/pavadinimas neįrašytas. "
    if request.form["r_login"] == "":
        error += "Prisijungimo vardas neįrašytas. "
    if request.form["r_email"] == "":
        error += "El. paštas neįrašytas neįrašytas. "
    if request.form["r_password"] == "":
        error += "Slaptažodis neįrašytas. "
    if not request.form["r_password"] == request.form["r_password_repeat"]:
        error += "Slaptažodžiai neatitinka. "

    data = {
            'r_error': error,
            's_error': "",
            'r_login': request.form["r_login"],
            'r_name': request.form["r_name"],
            'r_email': request.form["r_email"],
            }
    print(request.form)
    if not error == "":
        return render_template("public/index.html", data=data)
    else:
        data['r_password'] = request.form["r_password"]
        result = db_operations.add_user(data)
        if result == 1:
            return "User registered"
        else:
            return f"Something went wrong: {result}"


@app.route("/login", methods=["POST"])
def login():
    error = ""
    if request.form["s_name"] == "":
        error += "Vardas neįrašytas. "
    if request.form["s_password"] == "":
        error += "Slaptažodis neįrašytas. "
    data = {'r_error': "",
            's_error': error,
            's_login': request.form["s_login"],
            'r_name': "",
            'r_email': "",
            }
    print(request.form)
    if not error == "":
        return render_template("public/index.html", data=data)
    else:
        return "Hello signin"


@app.route("/invoice")
def view_invoice():
    return render_template("public/invoice.html")


@app.route("/calculate_lines", methods=["POST"])
def calculate_lines():
    req = request.get_json()
    data = {
        'data': calculate.calculate_invoice_lines(req)
    }
    answer = make_response(jsonify(data, 200))
    return answer
