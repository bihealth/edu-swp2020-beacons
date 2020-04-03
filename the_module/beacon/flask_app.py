import beacon.common
import beacon.database
import beacon.user_cli
from flask import Flask, render_template, url_for, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    """
Input: /
    Output: render_template(home.html)
    home with input field and submit button
"""
    pass

@app.route("/results")
def handle():
    """
    Input: request.form Object
    Output: render_template(result.html, **locals()),
    takes string from home.html, uses VariantStringParser to convert the input
string into Variant object and uses form database imported function
“handle_variant” and uses from common function var_str to convert AnnotatedVariant to string
    """
    pass

@app.route("/api/<var_str>",methods =['GET'])
def get_api(var_str) :
	pass
