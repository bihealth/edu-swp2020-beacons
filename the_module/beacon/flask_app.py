import beacon.common
import beacon.database
import beacon.user_cli
import beacon.rest_api
from flask import Flask, render_template, url_for, request, jsonify

app = Flask(__name__)

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
    inp = req["text"] #have to coordinate with home.html
    var = beacon.common.variantStringParser(inp)
    ann_var = handle variant(var)
    return render_template("output.html", **locals()) #same here

@app.route("/api/<var_str>",methods =['GET']) 
def get_api(var_str) :
    var = beacon.common.variantStringParser(var_str)
    ann_var = handle variant(var)
    return jsonify(beacon.rest_api.annVar_ls(ann_var))
     


if __name__== "__main__":
    app.run(debug=True)
