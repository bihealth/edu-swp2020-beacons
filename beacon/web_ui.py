from flask import Flask, jsonify, request, render_template, url_for, json
from . import common
from . import settings
from . import database
import requests
import webbrowser
import base64
import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plot
matplotlib.use('Agg')
import io


app = Flask(__name__)

@app.route("/", methods=["POST","GET"]) #put some information on this site?
def home():
    """
    Input: /
    Output: Home-Page with input fields and submit button
    """
    return render_template("home.html") #need to change home.html to  send data as json

@app.route("/results", methods=["POST","GET"])  # possible with GET??
def handle():
    """
    Input: request.form Object
    Output: HTML-Page with the results
    """
    if len(request.form['token']) > 0:
        token = request.form['token']

        con = database.ConnectDatabase(settings.PATH_LOGIN)
        sql = "SELECT authorization FROM login WHERE token = ?"
        auth =  con.parse_statement(sql, [token])
        if auth[0][0] > 1:
            atable = True
        else:
            atable = False

    else:
        token = None
        atable = False
    jform = {
        "chr": request.form['chr'],
        "pos": request.form['pos'],
        "ref": request.form['ref'],
        "alt": request.form['alt']
    }
    rep = requests.post("http://localhost:5000/query", json=jform, headers = {'token': token})
    res = rep.json()
    if res['statistic']:
        stat_byte = res['statistic'].encode('ascii')
        figure = base64.b64decode(stat_byte)
        img = mpimg.imread(io.BytesIO(figure))
        imgplot = plot.imshow(img)
        plot.savefig('stat_population_'+res['chr']+'_'+str(res['pos'])+'_'+res['ref']+'_'+res['alt']+ '.png')
        st = 'stat_population_'+res['chr']+'_'+str(res['pos'])+'_'+res['ref']+'_'+res['alt']+ '.png'
    return render_template("output.html", title="Results", **locals())

@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Input: token
    Output: Home-Page with input fields and submit button
    """
    if request.method == 'POST':
        token = request.form['token']
        resp = requests.post("http://localhost:5000/api/verify", headers = {'token': token})
        if resp.json()['verified']:
            con = database.ConnectDatabase(settings.PATH_LOGIN)
            sql = "SELECT name FROM login WHERE token = ?"
            username =  con.parse_statement(sql, [token])
            return render_template('home.html', token = token, user = username[0][0])
        else:
            error = "This is not a valid token"
            return render_template('login.html', title="Login",error = error)
    else:
        return render_template('login.html', title="Login")



if __name__ == "__main__":
    webbrowser.open_new("http://localhost:4000/")
    app.run(debug=True,port = "4000")
