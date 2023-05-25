from app import app
from flask import render_template, jsonify, request, make_response,  send_file
from app import calculate


@app.route("/")
def view_home():
    return render_template("public/index.html")


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
