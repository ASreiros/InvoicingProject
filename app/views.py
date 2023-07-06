from app import app
from flask import render_template, jsonify, request, make_response, redirect, url_for, send_file, send_from_directory
from app import calculate
from app import db_operations
from app import validation
from app import invoice_validation
from app import generate_pdf
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
from fpdf import FPDF



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

@app.route("/demo-user", methods=["POST"])
def demo_user_login():
    if current_user.is_authenticated:
        return redirect('/list')
    demo_user = db_operations.get_demo_user()
    if demo_user:
        login_user(demo_user, remember=False)
        return redirect(url_for('list_route'))
    else:
        data = {'r_error': "",
                's_error': "",
                's_login': "",
                'r_name': "",
                'r_email': "",
                's_password': "",
                }
        return render_template("public/index.html", data=data)

@app.route("/list", methods=["GET"])
@login_required
def list_route():
    data = validation.validate_user_data(current_user)
    invoices = db_operations.collect_invoices(current_user.id)
    return render_template("registered/list.html", data=data, invoices=invoices, error="")


@app.route("/user-settings", methods=["POST"])
@login_required
def user_settings():
    print(request.form)
    print(request.form['submit-button'])
    if request.form['submit-button'] == 'cancel-list':
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
        'address': current_user.address,
        'error': "",
    }

    buyer_data = {
        'name': "",
        'vat_code': "",
        'tax_code': "",
        'address': ""
    }


    invoice_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'number': db_operations.get_invoice_number(current_user.id, current_user.series),
        'series': current_user.series,
        'type': 'pvm sąskaita-faktūra',
        "vat_setting": '21',
        'sum_before_vat': 0,
        'vat': 0,
        'sum_after_vat': 0,
        'id': 'noid',
        'lines': [],

    }

    for key in user_data:
        if not user_data[key]:
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
    print(req)
    error = ""
    invoice_id = req['id']
    if invoice_id == 'noid':
        error += invoice_validation.unique_invoice_name_check(req, current_user.id)
    error += invoice_validation.invoice_validation(req)
    flag = False
    if error == "":
        flag = True
        seller_info = {
            'name': req["seller-name"],
            'tax': req['seller-tax'],
            'vat': req['seller-vat-tax'],
            'address': req['seller-address']
        }
        if not db_operations.edit_user(current_user.id, seller_info):
            flag = False
            error += "Pardavėjo duomenys išsauguoti nepavyko \n"
        if req['id'] == 'noid' and flag:
            save_result = db_operations.save_invoice_to_db(req, current_user.id)
            invoice_id = save_result[1]
            if not save_result[0]:
                error += "Dokumentas nebuvo išsaugotas \n"
                flag = False
        elif flag:
            if not db_operations.edit_invoice_to_db(req, current_user.id):
                error += "Dokumentas nebuvo išsaugotas \n"
                flag = False
        else:
            error += "Dokumentas nebuvo išsaugotas \n"
    print(error)
    answer = make_response(jsonify(error, flag, invoice_id, 200))
    return answer

@app.route("/get-pdf/<invoice_id>")
@login_required
def get_pdf(invoice_id):
    user_id = current_user.id
    pdf = generate_pdf.create_pdf(current_user, invoice_id)
    return send_from_directory('invoice', pdf, as_attachment=True)
    # return send_file(pdf, download_name='invoice.pdf', as_attachment=True)


@app.route("/get_number", methods=["POST"])
@login_required
def get_number():
    req = request.get_json()
    print(req)
    number = db_operations.get_invoice_number(current_user.id, req['series']),
    answer = make_response(jsonify(number, 200))
    return answer

@app.route("/delete-invoice", methods=["POST"])
@login_required
def delete_invoice():
    req = request.get_json()
    action_flag = db_operations.delete_invoice(req['invoice_id'], current_user.id)
    data = {
        'result': action_flag,
    }

    answer = make_response(jsonify(data, 200))
    return answer


@app.route("/edit-invoice/<invoice_id>", methods=["POST"])
@login_required
def edit_invoice(invoice_id):
    invoice = db_operations.get_invoice(invoice_id, current_user.id)
    if invoice:
        user_data = {
            'name': current_user.name,
            'vat_code': current_user.vat_code,
            'tax_code': current_user.tax_code,
            'address': current_user.address,
            'error': "",
        }

        buyer_data = {
            'name': invoice.buyer_name,
            'vat_code': invoice.buyer_vat,
            'tax_code': invoice.buyer_tax,
            'address': invoice.buyer_address
        }

        invoice_data = {
            'date': invoice.date,
            'number': invoice.number,
            'series': invoice.series,
            'type': invoice.type,
            "vat_setting": invoice.vat_setting,
            'sum_before_vat': invoice.sum_before_vat,
            'vat': invoice.vat,
            'sum_after_vat': invoice.sum_after_vat,
            'id': invoice.id,
            'lines': db_operations.get_lines(invoice_id)
        }

        print(invoice_data['lines'])

        for key in user_data:
            if not user_data[key]:
                user_data[key] = ""

        return render_template("registered/invoice.html", user_data=user_data, invoice_data=invoice_data,
                               buyer_data=buyer_data)

    else:
        data = validation.validate_user_data(current_user)
        invoices = db_operations.collect_invoices(current_user.id)
        error = "Pakoreguoti pasirinkta sąskaita-faktūra nepavyko"
        return render_template("registered/list.html", data=data, invoices=invoices, error=error)

@app.context_processor
def inject_template_scope():
    injections = dict()

    def cookies_check():
        value = request.cookies.get('cookie_consent')
        return value == 'true'
    injections.update(cookies_check=cookies_check)

    return injections



