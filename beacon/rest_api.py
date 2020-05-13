"""
Provides (flask) server for beacon.
"""
import matplotlib
from flask import Flask, jsonify, request
from . import common
from . import database
from . import settings
from io import BytesIO
import base64
import sqlite3

matplotlib.use("Agg")

app = Flask(__name__)


@app.route("/query", methods=["POST"])
def get_api():
    """
    Takes variant string, hands it over to database module and returns the answer.

    :param: POST request with json input_dict and token
    :return: json of variant and occurence
    """
    token = request.headers.get("token")
    try:
        with database.ConnectDatabase(settings.PATH_DATABASE) as con:
            auth = request_permission(request.remote_addr, token)
            var = common.parse_var(
                request.json
            )  # need to change common.parse_var to convert from dict to variant object
            if auth[0] is None:
                raise Exception(auth[1])
            if auth[0] == 0:
                un_ann = request.json
                un_ann["occ"] = None
                un_ann["error"] = None
                return jsonify(un_ann)
            else:
                ann_var = con.handle_request(var, auth[0])
                a_dict = ann_var.__dict__
                if (
                    a_dict["error"] is None
                    and len(a_dict) > 6
                    and a_dict["statistic"] is not None
                ):
                    figfile = BytesIO()
                    fig = ann_var.statistic
                    fig.figure.savefig(figfile, format="png")
                    figfile.seek(0)
                    figdata_png = base64.b64encode(figfile.getvalue())
                    a_dict["statistic"] = figdata_png.decode("ascii")
                elif a_dict["error"] is not None:  # pragma: no cover
                    a_dict["error"] = a_dict["error"].args[0]
                return jsonify(a_dict)
    except (sqlite3.Error, Exception) as e:
        un_ann = request.json
        un_ann["occ"] = None
        un_ann["error"] = e.args[0]
        return jsonify(un_ann)


def request_permission(ip_addr, token):
    """
    Takes IP address and token of user, counts and checks the number of request and returns it's authorization level.

    :param ip_addr: IP address of user
    :param token: token from login.db
    :return type: tuple
    """
    try:
        with database.ConnectDatabase(settings.PATH_LOGIN) as con:
            auth = con.parse_statement(
                "SELECT count_req FROM ip WHERE ip_addr = ?", [ip_addr]
            )
            if not auth:
                con.parse_statement(
                    "INSERT INTO ip(count_req, ip_addr) VALUES(1,?)", [ip_addr]
                )

            elif auth[0][0] > 20:
                return (0, None)
            else:
                con.parse_statement(
                    "UPDATE ip SET count_req = count_req + 1 WHERE ip_addr = ?",
                    [ip_addr],
                )
            if token == "":
                return (1, None)
            else:
                auth = con.parse_statement(
                    "SELECT authorization FROM login WHERE token = ?", [token]
                )
                return (auth[0][0], None)

    except (sqlite3.Error, Exception) as e:
        return (None, e.args[0])


@app.route("/api/verify", methods=["POST"])
def verify_user():
    """
    Takes the given token of user and checks if the user is verified.

    :param: POST request with token
    :return type: jsonify
    """
    try:
        with database.ConnectDatabase(settings.PATH_LOGIN) as con:
            token = request.headers["token"]
            exist_query = "SELECT token,name FROM login WHERE token = ?"
            exist = con.parse_statement(exist_query, [token])
            if exist:
                return jsonify({"verified": True, "user": exist[0][1], "error": None})
            else:
                return jsonify({"verified": False, "user": None, "error": None})
    except (sqlite3.Error, Exception) as e:
        return jsonify({"verified": None, "user": None, "error": e.args[0]})


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True)
