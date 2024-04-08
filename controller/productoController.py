from app import app, productos, categoria, baseDatos, usuarios
from flask import Flask, render_template, request, jsonify, redirect, url_for,session
import pymongo
import os
from bson.objectid import ObjectId
import base64
from io import BytesIO
from bson.json_util import dumps
from pymongo import MongoClient
from controller.usuarioController import *

# @app.route('/home')
# def home():
#     if("correo"in session):
        
#         listaProductos = productos.find()
#         todos_productos = []
#         for producto in listaProductos:
#             cat = categoria.find_one({'_id': ObjectId(producto['categoria'])})
#             if cat:
#                 producto['categoria'] = cat['nombre']
#                 todos_productos.append(producto)
#         return render_template("listarProductos.html", productos=todos_productos)
#     else:
#         mensaje ="Debe ingresar con sus datos"
#         return render_template("login.html",mensaje=mensaje)
@app.route('/home')
def home():
    if("correo"in session):
        
        listaProductos = productos.find()
        todos_productos = []
        for producto in listaProductos:
            cat = categoria.find_one({'_id': ObjectId(producto['categoria'])})
            if cat:
                producto['categoria'] = cat['nombre']
                todos_productos.append(producto)
        return render_template("listarProductos.html", productos=todos_productos)
    else:
        mensaje ="Debe ingresar con sus datos"
        return render_template("login.html",mensaje=mensaje)
        
@app.route ("/agregarProductos")
def vistaAgregarProducto():
    if("correo"in session):
        listaCategorias = categoria.find()
        return render_template("formulario.html",categorias=listaCategorias)
    else:
        mensaje ="Debe ingresar con sus datos"
        return render_template("login.html",mensaje=mensaje)

@app.route("/agregarProductos", methods=["POST"])
def agregarProducto():
    mensaje = None
    estado = False
    if("correo"in session):
        try:
            codigo =int(request.form["codigo"]) 
            nombre = request.form["nombre"]
            precio = int(request.form["precio"])
            idCategoria = request.form["categoria"]
            foto =request.files["imagen"]


            producto ={
                "codigo":codigo,
                "nombre":nombre,
                "precio":precio,
                "categoria":ObjectId(idCategoria)
            }

            resultado = productos.insert_one(producto)
            if (resultado.acknowledged):
                idProducto = resultado.inserted_id
                nombreFoto = f"{idProducto}.jpg"
                foto.save(os.path.join(app.config["UPLOAD_FOLDER"],nombreFoto))
                mensaje = "Producto Agregado Correctamente"
                estado = True
                return redirect (url_for("home"))
            else:
                mensaje="Problemas al agregar"

            return render_template ("/formulario.html",estado= estado, mensaje=mensaje,)


        except pymongo.errors as error:
            mensaje = error
            return error
    else:
        mensaje ="Debe ingresar con sus datos"
        return render_template("login.html",mensaje=mensaje)
    
@app.route('/eliminarProducto/<id>', methods=['POST'])
def eliminar_producto(id):
    productos.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('listar_productos'))

# @app.route('/editarProducto/<id>', methods=['GET', 'POST'])
# def editar_producto(id):
#     if request.method == 'GET':
#         producto = productos.find_one({'_id': ObjectId(id)})
#         return render_template('formulario.html', producto=producto)
#     else:
#         productos.update_one({'_id': ObjectId(id)}, {'$set': {
#             'codigo': request.form['codigo'],
#             'nombre': request.form['nombre'],
#             'precio': request.form['precio'],
#             'categoria': request.form['categoria']
#         }})
#         return redirect(url_for('listar_productos'))
@app.route('/editarProducto/<id>', methods=['GET', 'POST'])
def editar_producto(id):
    if request.method == 'GET':
        producto = productos.find_one({'_id': ObjectId(id)})
        return render_template('formulario.html', producto=producto)
    else:
        productos.update_one({'_id': ObjectId(id)}, {'$set': {
            'codigo': request.form['codigo'],
            'nombre': request.form['nombre'],
            'precio': request.form['precio'],
            'categoria': request.form['categoria']
        }})
        return redirect(url_for('home'))