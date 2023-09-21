from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging
import jwt

load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

SECRET_KEY = os.getenv("SECRET_KEY")


@app.before_request
def before_request_func():
    log_request_info()

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Acceso no autorizado"}), 403

    token = auth_header.split(" ")[1]

    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expirado"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token inválido"}), 403


def log_request_info():
    logging.info(f"Petición recibida: {request.method} {request.url}")
    auth_header = request.headers.get("Authorization")
    logging.info(f"Cabecera de Autorización: {auth_header}")


MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.chatnext

db.Articulos.create_index([("NombreArticulo", "text")], default_language="spanish")
db.Clientes.create_index([("NombreCliente", "text")], default_language="spanish")
db.CabeceraAlbaran.create_index([("NombreCliente", "text")], default_language="spanish")
