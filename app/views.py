from app import app
from flask import render_template, jsonify, request, make_response,  send_file


@app.route("/")
def view_invoice():
    return render_template("public/invoice.html")
