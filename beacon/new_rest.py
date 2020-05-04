from flask import Flask, jsonify, request, render_template, url_for, json
from . import common
from . import settings
from . import database
import requests
import webbrowser

app = Flask(__name__)


#def annVar_ls(var, occ):
#    """Input: common.AnnotatedVariant
#    Output: ls with api values and AnnotatedVariant class  variables
#    function transformes AnnotatedVariant to ls
#    api =[{“chr”:str,“pos”:int,“res”:chr,“alt”:chr,“occ”:bool}]"""
#    var_ls = list(var.__dict__.values())
#    if isinstance(occ, bool):
#        var_ls.append(occ)
#    else:
#        var_ls.append(occ.args[0])
#    return var_ls

# @app.route("/query", methods=["POST"]) #change user_cli to make POST instead of GET request
# def get_api(): #gets json/dict as POST request 
#     connectDb = database.ConnectDatabase(settings.PATH_DATABASE)
#     var = common.parse_var(request.json) #need to change common.parse_var to convert from dict to variant object
#     ann_var = connectDb.handle_variant(var) #change common.parse_var to get annotated variant
#     return jsonify(ann_var.__dict__) #change user_cli to take dict 

@app.route("/", methods=["GET"]) #put some information on this site?
def home():
    """
    Input: /
    Output: render_template(home.html)
    home with input field and submit button
    """
    return render_template("home.html") #need to change home.html to  send data as json

@app.route("/results", methods=["POST","GET"])  # possible with GET??
def handle():
    """
    Input: request.form Object
    Output: render_template(result.html, **locals()),
    takes string from home.html, uses VariantStringParser to convert the input
    string into Variant object and uses form database imported function
    “handle_variant” and uses from common function var_str to convert AnnotatedVariant to string
    """
    rep = requests.post("http://localhost:5000/query", data=request.json)
    res = rep.json
    return render_template("output.html", title="Results", **locals()) #need to change output.html to get information from json

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        token = request.form['token']
        resp = requests.post("http://localhost:5000/api/verify", headers = {'token': token})
        if resp.json()['verified']:
            return (True,resp.json()['user'])
        else:
            print("This is not a valid token")
            return (False,)
    else:
        return render_template('login.html')



if __name__ == "__main__":
    webbrowser.open_new("http://localhost:5000/")
    app.run(debug=True)
