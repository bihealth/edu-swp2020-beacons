
"""
Provides (flask) server for beacon.
"""
from flask import Flask, jsonify, request
from . import common
from . import database
import requests
from . import settings
app = Flask(__name__)


@app.route("/query", methods=["POST"]) #change user_cli to make POST instead of GET request : done
def get_api(): #gets json/dict as POST request : done
    """
    Takes variant string, hands it over to database module and returns the answer
    :param var_str:
    :return: json of variant and occurence
    """

    token = request.headers.get('token')
    auth = request_permission(request.remote_addr,token)
    connectDb = database.ConnectDatabase(settings.PATH_DATABASE)
    var = common.parse_var(request.json) #need to change common.parse_var to convert from dict to variant object
    print( "auth is: ", auth)
    if auth == 0:
        un_ann = request.json
        un_ann['occ'] = None
        un_ann['error'] = None
        return jsonify(un_ann)
    else:
        ann_var = connectDb.handle_request(var, auth)
        a_dict = ann_var.__dict__
        out = {x: a_dict[x] for x in a_dict if x is not 'statistic'}
        print(out)
        return jsonify(out)


def request_permission(ip_addr,token):   
    con_login = database.ConnectDatabase(settings.PATH_LOGIN)
    auth = con_login.parse_statement("SELECT count_req FROM ip WHERE ip_addr = ?", [ip_addr])
    if not auth:
        con_login.parse_statement("INSERT INTO ip(count_req, ip_addr) VALUES(1,?)", [ip_addr]) 
    elif auth[0][0] > 10:
        return 0
    else:
        con_login.parse_statement("UPDATE ip SET count_req = count_req + 1 WHERE ip_addr = ?",[ip_addr])
    
    if token == None:
        return 1
    else:
        auth = con_login.parse_statement("SELECT authorization FROM login WHERE token = ?", [token])
        return auth[0][0]



@app.route('/api/verify', methods = ['POST'])
def verify_user():
    con_login = database.ConnectDatabase(settings.PATH_LOGIN)
    token = request.headers['token']
    exist_query = "SELECT token,name FROM login WHERE token = ?"
    exist = con_login.parse_statement(exist_query, [token])
    if exist:
        return jsonify({'verified': True, 'user': exist[0][1]})
    else:
        return jsonify({'verified': False, 'user': None})




if __name__ == "__main__":
    app.run(debug=True)
