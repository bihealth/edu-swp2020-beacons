import common
import database
#import user_cli
#import rest_api
import webbrowser
import os
from flask import Flask, render_template, url_for, request, jsonify
from threading import Timer

app = Flask(__name__)

# Windows:
# # set PATH_DATABASE=XXX.sqlite3
# # python beacon/flask_app.py
# Mac/Linux
# # PATH_DABASE=XXX.sqlite3 python beacon/flask_app.py
connectDb = database.ConnectDatabase(os.environ.get("PATH_DATABASE"))


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
    req = request.form
    inp = req["var"]     
    var = common.parse_var(inp)
    #ann_var = database.handle_variant(var)
    #unann_var = common.parse_var(ann_var)
    occ = connectDb.handle_variant(var)
    return render_template("output.html", title='Results', **locals()) 

 
"""
@app.teardown_appcontext
def close_connection():
    connectDb.connection.close()
"""

if __name__== "__main__":
    Timer(1, webbrowser.open_new('http://localhost:5000/')).start()
    app.run(debug=True)
