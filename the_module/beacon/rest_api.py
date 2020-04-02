from flask import Flask
"""import beacon.database
import beacon.user_cli
import beacon.common
"""
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

class Api:
    def __init__(self):

        pass

    def annVar_ls():
        """Input: common.AnnotatedVariant
                   	        Output: ls with api values and AnnotatedVariant class  variables
                   	        function transformes AnnotatedVariant to ls
                   	        api =[{“chr”:str,“pos”:int,“res”:chr,“alt”:chr,“occ”:bool}]"""
        pass

@app.route("/api/<var_str>",methods =['GET'])
def get_api(var_str) :
	pass
