from . import common
from . import database
#import user_cli
#import rest_api
import webbrowser
import os
from flask import Flask, render_template, url_for, request, jsonify
from threading import Timer
from . import settings
app = Flask(__name__)

# Windows:
# # set PATH_DATABASE=XXX.sqlite3
# # python beacon/flask_app.py
# Mac/Linux
# # PATH_DABASE=XXX.sqlite3 python beacon/flask_app.py


@app.route("/")
def home():
    """
    Input: /
    Output: render_template(home.html)
    home with input field and submit button
    """
    return render_template("home.html")

@app.route("/results", methods=['POST']) #possible with GET??
def handle():
    """
    Input: request.form Object
    Output: render_template(result.html, **locals()),
    takes string from home.html, uses VariantStringParser to convert the input
    string into Variant object and uses form database imported function
    “handle_variant” and uses from common function var_str to convert AnnotatedVariant to string
    """
    connectDb = database.ConnectDatabase(settings.PATH_DATABASE)

    req = request.form
    inp = req["var"]     
    var = common.parse_var(inp)
    #ann_var = database.handle_variant(var)
    #unann_var = common.parse_var(ann_var)
    occ = connectDb.handle_variant(var)
    print(occ)
    if isinstance(occ, bool):
        return render_template("output.html", title='Results', **locals()) 
    else:
        occ = False
        return render_template("output.html", title='Results', **locals())

 
"""
@app.teardown_appcontext
def close_connection():
    connectDb.connection.close()
"""

if __name__== "__main__":
    webbrowser.open_new('http://localhost:5000/')
    app.run(debug=True, use_reloader=False)
