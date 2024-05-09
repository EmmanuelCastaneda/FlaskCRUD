from flask import Flask
import pymongo

app = Flask(__name__)
app.config["UPLOAD_FOLDER"]="./static/img"

app.secret_key = 'fjurueu44582ij'

miConexion= pymongo.MongoClient("mongodb://localhost:27017")

baseDatos = miConexion["GestionProductos"]

productos = baseDatos["productos"]
categoria = baseDatos["categorias"]
usuarios = baseDatos["usuarios"]


from controller.usuarioController import *
from controller.productoController import *



if __name__ == "__main__":
    app.run(debug=True, port=4000)
    
# from flask import Flask
# from flask_mongoengine import MongoEngine

# app = Flask(__name__)
# app.secret_key = 'jdjdjdjbej'

# app.config['MONGODB_SETTINGS'] = {
#     'db': 'Mongo1',
#     'host': 'mongodb://localhost:27017/Mongo1'
# }
# db = MongoEngine(app)

# from controller.usuarioController import *
# from controller.productoController import *


# if _name_ == "_main_":
#     app.run(port=5000, debug=True)