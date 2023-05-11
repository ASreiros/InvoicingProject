from app import app
from flask import render_template, jsonify, request, make_response,  send_file


@app.route("/")
def home():
    return render_template("public/index.html")
