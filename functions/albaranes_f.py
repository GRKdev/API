from extensions import db
from utils import mongo_to_json


def obtener_por_numero_albaran(numero):
    collection = db['CabeceraAlbaran']
    
    try:
        num_albaran = int(numero)
    except ValueError:
        return None

    albaran = collection.find_one({"NumeroAlbaran": num_albaran})
    if albaran:
        return mongo_to_json(albaran)
    else:
        return None
    
def obtener_por_nombre_cliente(nombre):
    collection = db['Clientes']
    cliente = collection.find_one({"NombreCliente": nombre})
    if cliente:
        return mongo_to_json(cliente)
    else:
        return None
