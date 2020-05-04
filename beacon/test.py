import os
import webbrowser
from flask import Flask, abort, request, jsonify, g, url_for
from flask import Flask, render_template, url_for, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from passlib.apps import custom_app_context as pwd_context
import secrets

import settings
import database
import admin_tools_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "hallo"
auth = HTTPBasicAuth


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/results", methods=["GET", "POST"])
def handle():
    json = request.form
    # return json
    # return json['chr]
    return render_template("output.html", title="Results", **locals())


@app.route("/registration")
def registration():
    return render_template("registration.html")


@app.route("/login")
def login():
    error = None
    if request.method == "POST":
        json = request.form
        if valid_login(json["user"], json["password"]):
            return login_user(json["user"])  # return token
            # token =jwt.encode({'user': json['user'], 'time': hsdhbs, app.conig['SECRET_KEY']})
            # return jsonify({'token': token.decode(UTF-8)})
        else:
            error = "Invalid username/password"
    return render_template("login.html", error=error)


def hash_password(password):
    password_hash = pwd_context.encrypt(password)
    return password_hash


def verify_password(password):
    return pwd_context.verify(password, password_hash)


@app.route("/api/users/", methods=["POST"])
def new_user():
    if request.method == "POST":
        conn = database.ConnectDatabase(settings.PATH_User_DATABASE)
        json = request.form
        username = json["user"]
        password = json["password"]
        dup = admin_tools_user.SearchDuplicatesCommand()
        userdup = dup.find_dup(conn, username)
        if userdup is True:
            error = "Username already exists"
            return render_template("registration.html", error=error)
            # abort(400) # existing user
        token = secrets.token_urlsafe()
        password_hash = hash_password(password)
        parameters = (username, password_hash, token)
        adduser = admin_tools_user.AddUser()
        addu = adduser.addusers(parameters, conn)
        return jsonify({"token": token})


if __name__ == "__main__":
    webbrowser.open_new("http://localhost:5000/home")
    app.run(debug=True)
