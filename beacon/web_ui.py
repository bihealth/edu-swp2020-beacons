from . import settings
from . import database
from flask import Flask, request, render_template, url_for #json
import requests
import webbrowser
import base64
import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plot
import io

matplotlib.use("Agg")


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    """
    Input: /
    Output: Home-Page with input fields and submit button
    """
    return render_template("home.html")


@app.route("/results", methods=["POST", "GET"])
def handle():
    """
    Input: request.form Object
    Output: HTML-Page with the results
    """
    token = request.form["token"]
    jform = {
        "chr": request.form["chr"],
        "pos": request.form["pos"],
        "ref": request.form["ref"],
        "alt": request.form["alt"],
    }
    rep = requests.post(
        "http://localhost:5000/query", json=jform, headers={"token": token}
    )
    res = rep.json()
    if  len(res) > 6:
        atable = True
        if res["statistic"] is None:
            static = False
        else:
            static = True
    else:
        atable = False
        static = False
    if res["occ"] is False or res["occ"] is None:
        return render_template("output.html", title="Results", **locals())
    if static:
        stat_byte = res["statistic"].encode("ascii")
        figure = base64.b64decode(stat_byte)
        img = mpimg.imread(io.BytesIO(figure))
        imgplot = plot.imshow(img)
        plot.savefig(
            "stat_population_"
            + res["chr"]
            + "_"
            + str(res["pos"])
            + "_"
            + res["ref"]
            + "_"
            + res["alt"]
            + ".png"
        )
        st = (
            "stat_population_"
            + res["chr"]
            + "_"
            + str(res["pos"])
            + "_"
            + res["ref"]
            + "_"
            + res["alt"]
            + ".png"
        )
    return render_template("output.html", title="Results", **locals())

@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Input: token
    Output: Home-Page with input fields and submit button
    """
    if request.method == "POST":
        token = request.form["token"]
        resp = requests.post(
            "http://localhost:5000/api/verify", headers={"token": token}
        )
        if resp.json()["verified"]:
            username = resp.json()["user"]
            return render_template("home.html", token=token, user=username)
        else:
            error = "This is not a valid token"
            return render_template("login.html", title="Login", error=error)
    else:
        return render_template("login.html", title="Login")


if __name__ == "__main__":
    webbrowser.open_new("http://localhost:4000/")
    app.run(debug=True, port="4000")
