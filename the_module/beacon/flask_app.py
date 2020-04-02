import beacon.common
import beacon.database
from flask import Flask, render_template, url_for, request

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
