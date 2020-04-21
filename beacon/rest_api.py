from flask import Flask, jsonify
from . import common
from . import settings
from . import database


app = Flask(__name__)


def annVar_ls(var, occ):
    """
    Makes list from variant object and occurence
    :param var: variant object
    :param occ: bool for occurence of variant in database
    :return: list of variant class attributes and occurence bool
    """
    var_ls = list(var.__dict__.values())
    if isinstance(occ, bool):
        var_ls.append(occ)
    else:
        var_ls.append(occ.args[0])
    return var_ls


@app.route("/api/<var_str>", methods=["GET"])
def get_api(var_str):
    """
    Takes variant string, hands it over to database module and returns the answer
    :param var_str:
    :return: json of variant and occurence
    """
    connectDb = database.ConnectDatabase(settings.PATH_DATABASE)
    var = common.parse_var(var_str)
    occ = connectDb.handle_variant(var)
    return jsonify(results=annVar_ls(var, occ))


if __name__ == "__main__":  # pragma nocover
    app.run(debug=True)
