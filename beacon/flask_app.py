from . import common
from . import database
import webbrowser
from flask import Flask, render_template, request
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
    Starts home.html with input field and submit button.

    :param "/":
    :return: render_template(home.html)
    """
    return render_template("home.html")


@app.route("/results", methods=["POST"])
def handle():
    """
    Takes string from home.html, uses parse_var to convert the input
    string into Variant object and pases Variant request to database
    and gives "answer" to output.hmtl back.

    :param "/results":
    :param methods=["POST"]: request.form Object
    :return: render_template(result.html, **locals())
    """
    connectDb = database.ConnectDatabase(settings.PATH_DATABASE)
    req = request.form
    inp = req["var"]
    var = common.parse_var(inp)
    occ = connectDb.handle_variant(var)
    if isinstance(occ, bool):
        return render_template("output.html", title="Results", **locals())
    else:
        return render_template("output.html", title="Results", **locals())   # pragma nocover


if __name__ == "__main__":  # pragma nocover
    webbrowser.open_new("http://localhost:5000/")
    app.run(debug=True, use_reloader=False)
