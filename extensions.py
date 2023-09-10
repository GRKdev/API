from flask import Flask, request
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.before_request
def log_request_info():
    logging.info(f"Petición recibida: {request.method} {request.url}")

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.chatnext

db.Articulos.create_index([("NombreArticulo", "text")], default_language='spanish')
db.Clientes.create_index([("NombreCliente", "text")], default_language='spanish')
db.CabeceraAlbaran.create_index([("NombreCliente", "text")], default_language='spanish')
