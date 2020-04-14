from flask import Flask,jsonify
from . import common
from . import settings 
from . import database


app = Flask(__name__)

def annVar_ls(var, occ):
    """Input: common.AnnotatedVariant
    Output: ls with api values and AnnotatedVariant class  variables
    function transformes AnnotatedVariant to ls
    api =[{“chr”:str,“pos”:int,“res”:chr,“alt”:chr,“occ”:bool}]"""
    var_ls = list(var.__dict__.values())
    var_ls.append(str(occ))
    return var_ls



@app.route("/api/<var_str>",methods =['GET'])
def get_api(var_str) :
    connectDb = database.ConnectDatabase(settings.PATH_DATABASE)
   
    var = common.parse_var(var_str)
    occ = connectDb.handle_variant(var)
    #if isinstance(occ,bool):
     #   print("hierher, hierher!!!!")
    return jsonify(results=annVar_ls(var,occ))
    #else:
     #   return occ

if __name__=="__main__":
    app.run(debug=True)
