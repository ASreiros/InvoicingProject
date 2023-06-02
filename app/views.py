from app import app
from flask import render_template, jsonify, request, make_response, redirect
from app import calculate
from app import db_operations
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


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
    hashed_password = generate_password_hash(request.form["r_password"])
    print(request.form)
    if request.form["r_name"] == "":
        error += "Vardas/pavadinimas neįrašytas. "
    elif len(request.form["r_name"]) > 100:
        error += "Vardas/pavadinimas per ilgas. "
    if request.form["r_login"] == "":
        error += "Prisijungimo vardas neįrašytas. "
    elif len(request.form["r_login"]) > 80:
        error += "Prisijungimo vardas per ilgas. "
    if request.form["r_email"] == "":
        error += "El. paštas neįrašytas neįrašytas. "
    elif len(request.form["r_email"]) > 100:
        error += "El. paštas per ilgas. "
    if request.form["r_password"] == "":
        error += "Slaptažodis neįrašytas. "
    elif not request.form["r_password"] == request.form["r_password_repeat"]:
        error += "Slaptažodžiai neatitinka. "
    elif len(hashed_password) > 200:
        error += "Slaptažodis per ilgas."
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
        data['r_password'] = hashed_password
        result = db_operations.add_user(data)
        if result == 1:
            return "User registered"
        else:
            data['r_password'] == ""
            if "UNIQUE" in str(result) and 'user.username' in str(result):
                data['r_error'] = "Neunikalus prisijungimo vardas"
            elif "UNIQUE" in str(result):
                data['r_error'] = "Neunikalus el. paštas"
            else:
                data['r_error'] = "Nepavyko užregistruoti vartuotoją"
            return render_template("public/index.html", data=data)


@app.route("/login", methods=["POST"])
def login():
    error = ""
    if request.form["s_login"] == "":
        error += "Prisijungimo vardas neįrašytas. "
    elif len(request.form["s_login"]) > 80:
        error += "Prisijungimo vardas per ilgas. "
    if request.form["s_password"] == "":
        error += "Slaptažodis neįrašytas. "
    data = {'r_error': "",
            's_error': error,
            's_login': request.form["s_login"],
            'r_name': "",
            'r_email': "",
            's_password': "",
            }
    if not error == "":
        return render_template("public/index.html", data=data)
    else:
        data['s_password'] = request.form["s_password"]
        result = db_operations.check_user(data)
        if result:
            print(result)
            return f'User: {result.username}, {result.name}, {result.email}, {result.id}'
        else:
            error = "Prisijungti nepavyko"
            data['s_error'] = error
            return render_template("public/index.html", data=data)

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
