from app import app
from flask import render_template, jsonify, request, make_response, redirect, url_for
from app import calculate
from app import db_operations
from app import validation
from app import invoice_validation
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime



@app.route("/", methods=["GET"])
def view_home():
    if current_user.is_authenticated:
        return redirect('/list')
    data = {'r_error': "",
            's_error': "",
            's_login': "",
            'r_name': "",
            'r_email': "",
            }
    return render_template("public/index.html", data=data)


@app.route("/register", methods=["POST"])
def register():
    if current_user.is_authenticated:
        return redirect('/list')
    if request.method == 'GET':
        return redirect('/')
    error = ""
    if not request.cookies.get('cookie_consent'):
        error += "Prisijungimui reikalingas slapukų leidimas apačioje"
    error += validation.validate_password(request.form["r_password"], request.form["r_password_repeat"])
    error += validation.validate_name(request.form["r_name"])
    error += validation.validate_login(request.form["r_login"])
    error += validation.validate_email(request.form["r_email"])

    data = {
            'r_error': error,
            's_error': "",
            'r_login': request.form["r_login"],
            'r_name': request.form["r_name"],
            'r_email': request.form["r_email"],
            }
    if not error == "":
        return render_template("public/index.html", data=data)
    else:
        data['r_password'] = request.form["r_password"]
        result = db_operations.add_user(data)
        if result[0]:
            login_user(result[1], remember=False)
            return redirect(url_for('list_route'))
        else:
            data['r_password'] == ""
            if "UNIQUE" in str(result[1]) and 'user.username' in str(result[1]):
                data['r_error'] = "Neunikalus prisijungimo vardas"
            elif "UNIQUE" in str(result[1]):
                data['r_error'] = "Neunikalus el. paštas"
            else:
                data['r_error'] = "Nepavyko užregistruoti vartuotoją"
            return render_template("public/index.html", data=data)


@app.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect('/list')
    if request.method == 'GET':
        return redirect('/')
    error = ""
    if not request.cookies.get('cookie_consent'):
        error += "Prisijungimui reikalingas slapukų leidimas apačioje"
    error += validation.validate_login(request.form["s_login"])
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
            login_user(result, remember=False)
            return redirect(url_for('list_route'))
        else:
            error = "Prisijungti nepavyko"
            data['s_error'] = error
            return render_template("public/index.html", data=data)


@app.route("/list", methods=["GET"])
@login_required
def list_route():
    data = validation.validate_user_data(current_user)
    return render_template("registered/list.html", data=data)


@app.route("/user-settings", methods=["POST"])
@login_required
def user_settings():
    print(request.form)
    print(request.form['submit-button'])
    if request.form['submit-button'] == 'cancel':
        return redirect("/list")
    error = ""
    error += validation.validate_name(request.form['c_name'])
    error += validation.validate_tax(request.form['s-vat'])
    error += validation.validate_tax(request.form['c-tax'])
    error += validation.validate_email(request.form['s-address'])

    if error:
        data = validation.validate_user_data(current_user)
        data['error'] = error
        return render_template("registered/list.html", data=data)
    else:
        user_id = current_user.id
        data = {
            'name': request.form['c_name'],
            'vat': request.form['s-vat'],
            'tax': request.form['c-tax'],
            'address': request.form['s-address']
        }
        result = db_operations.edit_user(user_id, data)
        if result:
            return redirect("/list")
        else:
            data = validation.validate_user_data(current_user)
            data['error'] = "Nepavyko pakoreguoti duomenys"
            return render_template("registered/list.html", data=data)


@app.route("/change-password", methods=["POST"])
@login_required
def change_password():
    if request.form['submit-button'] == 'cancel':
        return redirect("/list")
    error = ""
    error += validation.validate_password(request.form["new_password"], request.form["new_password_repeat"])
    if not error:
        result = db_operations.update_password(current_user.id, request.form["old_password"])
        if not result:
            error += "Senas slaptažodis neteisingas. "
    if error:
        data = validation.validate_user_data(current_user)
        data['p_error'] = error
        return render_template("registered/list.html", data=data)
    else:
        return redirect('/list')



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route("/invoice")
@login_required
def new_invoice():
    user_data = {
        'name': current_user.name,
        'vat_code': current_user.vat_code,
        'tax_code': current_user.tax_code,
        'address': current_user.address
    }

    buyer_data = {
        'name': "",
        'vat_code': "",
        'tax_code': "",
        'address': ""
    }

    invoice_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'number': 1,
        'series': 'INV',
        'type': 'pvm sąskaita-faktūra',
        "vat_setting": '21',
        'sum_before_vat': 0,
        'vat': 0,
        'sum_after_vat': 0,

    }

    for key in user_data:
        if user_data[key] == None:
            user_data[key] = ""

    return render_template("registered/invoice.html", user_data=user_data, invoice_data=invoice_data, buyer_data=buyer_data)


@app.route("/calculate_lines", methods=["POST"])
@login_required
def calculate_lines():
    req = request.get_json()
    data = {
        'data': calculate.calculate_invoice_lines(req)
    }
    answer = make_response(jsonify(data, 200))
    return answer

@app.route("/save-invoice", methods=["POST"])
@login_required
def save_new_invoice():
    req = request.get_json()
    error = invoice_validation.unique_invoice_name_check(req)
    error += invoice_validation.invoice_validation(req)
    flag = False
    if error == "":
        flag = True
        if not db_operations.save_invoice_to_db(req, current_user.id):
            error += "Išsauguoti nepavyko \n"
            flag = False
    print(error)
    answer = make_response(jsonify(error, flag, 200))
    return answer

@app.context_processor
def inject_template_scope():
    injections = dict()

    def cookies_check():
        value = request.cookies.get('cookie_consent')
        return value == 'true'
    injections.update(cookies_check=cookies_check)

    return injections



