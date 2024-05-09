from app import app, usuarios
from flask import Flask, render_template, request, redirect, session,url_for
import pymongo
@app.route("/")
def Login():
    return render_template ("login.html")

@app.route("/", methods=["POST"])
def login ():
    mensaje=None
    estado=None
    try:
        correo  = request.form["correo"]
        contraseña = request.form["contraseña"]
        consulta = {"correo":correo, "contraseña":contraseña}
        user = usuarios.find_one(consulta)
        if (user):
            session["correo"]=correo
            return redirect (url_for("home"))
        else:
            mensaje = "Datos no validos"   
    except pymongo.errors as error:
        mensaje = error
    return render_template("login.html",estado=estado,mensaje=mensaje)

@app.route("/salir")
def salir():
    session.clear()
    mensaje="Se ha cerrado sesion"
    return render_template("login.html",mensaje=mensaje)