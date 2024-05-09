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


@app.route('/agregarProductos', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        producto = {
            'codigo': request.form['codigo'],
            'nombre': request.form['nombre'],
            'precio': request.form['precio'],
            'categoria': request.form['categoria']
        }
        productos.insert_one(producto)
        return redirect(url_for('home'))
    return render_template('listarProductos.html')

@app.route("/eliminar_producto/<id>", methods=["GET"])
def eliminar_producto(id):
    if "correo" in session:
        try:
            productos.delete_one({"_id": ObjectId(id)})
            
            return redirect(url_for("home"))
        except pymongo.errors.PyMongoError as error:
      
            return render_template("falso.html", mensaje="No se pudo eliminar el producto")
    else:
        
        mensaje = "Por favor inicia sesión para continuar."
        return render_template("login.html", mensaje=mensaje)
    
    
    
@app.route('/editarProducto/<id>', methods=['GET', 'POST'])
def editar_producto(id):
    if "correo" in session:
        try:
            producto = productos.find_one({'_id': ObjectId(id)})
            if producto:
                listaCategorias = categoria.find()
                if request.method == 'POST':
                    
                    codigo = request.form['codigo']
                    nombre = request.form['nombre']
                    precio = request.form['precio']
                    categoria_id = request.form['categoria']
                    

                    
                    productos.update_one({'_id': producto['_id']},
                                        {'$set': {'codigo': codigo,
                                                  'nombre': nombre,
                                                  'precio': precio,
                                                  'categoria': categoria_id}})

                    
                    return redirect(url_for('home'))
                else:
                    return render_template("editar.html", producto=producto, categorias=listaCategorias)
            else:
                return redirect(url_for('home'))
        except pymongo.errors.PyMongoError as error:
            return render_template("falso.html", mensaje="No se pudo encontrar el producto")
    else:
        mensaje = "Por favor inicia sesión para continuar."
        return render_template("login.html", mensaje=mensaje)




    
     