
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
    if auth == 0:
        un_ann = request.json
        un_ann['occ'] = None
        return jsonify(un_ann)
    elif auth == 1:
        ann_var = connectDb.handle_request(var) #change common.parse_var to get annotated variant
        
        return jsonify(ann_var.__dict__) #change user_cli to take dict 
    else:
        ann_var = connectDb.handle_request(var, True)
        return jsonify(ann_var.__dict__)


def request_permission(ip_addr,token):
    con = database.ConnectDatabase(settings.PATH_LOGIN)
    if token == None:
        auth = con.parse_statement("SELECT authorization,count_req FROM login WHERE ip_addr = ?", [ip_addr])
        if not auth:
            con.parse_statement("INSERT INTO login(name, token, authorization, count_req, ip_addr) VALUES('user', 'user',1,1,?)", [ip_addr]) 
            return 1
        elif auth[0][1] > 10:
            return 0
        else:
            con.parse_statement("UPDATE login SET count_req = count_req + 1 WHERE ip_addr = ?",[ip_addr])
            return auth[0]
    else:
        auth = con.parse_statement("SELECT authorization,count_req FROM login WHERE token = ?", [token])
        if auth[0][1] > 10:
            return 0
        else:
            con.parse_statement("UPDATE login SET count_req = count_req + 1 WHERE token = ?",[token])
            return auth[0]

@app.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    authorization = request.json.get('autorization')
    if username is None or password is None or autorization is None:
        abort(400)
    conn = test_db.create_connection(settings.PATH_LOGIN)
    user = (username, password, authorization)
    test_db.create_user(conn, user)



@app.route('/api/verify', methods = ['POST'])
def verify_user():
    con = database.ConnectDatabase(settings.PATH_LOGIN)
    token = request.headers['token']
    exist_query = "SELECT token,name FROM login WHERE token = ?"
    exist = con.parse_statement(exist_query, [token])
    if exist:
        return jsonify({'verified': True, 'user': exist[0][1]})
    else:
        return jsonify({'verified': False, 'user': None})




if __name__ == "__main__":
    app.run(debug=True)
