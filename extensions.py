from flask import Flask
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.chatnext

db.Articulos.create_index([("NombreArticulo", "text")], default_language='spanish')
db.Clientes.create_index([("NombreCliente", "text")], default_language='spanish')
db.CabezeraAlbaran.create_index([("NombreCliente", "text")], default_language='spanish')
