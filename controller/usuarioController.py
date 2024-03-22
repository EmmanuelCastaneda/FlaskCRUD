from app import app, usuarios
from flask import Flask, render_template, request, redirect, session, url_for
import pymongo

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template ("listarProductos.html")

@app.route("/", methods=["POST"])
def login():
    mensaje = None
    estado = None
    try:
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]
        consulta = {"correo": correo, "contraseña": contraseña}
        user = usuarios.find_one(consulta)
        if user:
            session["correo"] = correo
            return redirect(url_for("home"))
        else:
            mensaje = "Datos no válidos"
    except pymongo.errors.PyMongoError as error:
        mensaje = "Error en la base de datos: " + str(error)
    except Exception as error:
        mensaje = "Error desconocido: " + str(error)
    return render_template("login.html", estado=estado, mensaje=mensaje)

# Asumiendo que tienes una ruta llamada "home" definida en otro lugar de tu aplicación.
# Si no es el caso, necesitas definir la función para la ruta "/home".

