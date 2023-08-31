from extensions import db
from utils import serialize_mongo_object
import json

def obtener_por_nombre_articulo(nombre_articulo): #http://localhost:5000/api/art?info=mouse
    collection = db['Articulos']
    search_terms = nombre_articulo.split(',')
    search_string = " ".join(['"' + term + '"' for term in search_terms])

    fields = {"NombreArticulo": 1, "Descripcion": 1, "Producto": 1, "PrecioVenta": 1, "Stock": 1,}
    results = collection.find({"$text": {"$search": search_string}, "CodigoEmpresa": "99"}, fields)

    serialized_results = []
    for r in results:
        serialized = json.loads(json.dumps(r, default=serialize_mongo_object))
        serialized.pop('_id', None)
        filtered_serialized = {k: v for k, v in serialized.items() if v and str(v).strip()}
        serialized_results.append(filtered_serialized)
    
    return serialized_results

    
def obtener_por_codigo_articulo(codigo):         #http://localhost:5000/api/art?code=1007
    collection = db['Articulos']    
    if codigo:
        try:
            codigo = int(codigo)
        except ValueError:
            pass  
    else:
        return {} 

    result = collection.find_one({"CodigoArticulo": codigo}, 
                                  projection={
                                      "_id": 0,
                                      "NombreArticulo": 1,
                                      "Descripcion": 1,
                                      "PrecioVenta": 1,
                                      "Stock": 1
                                  })
    if result:
        return json.loads(json.dumps(result, default=serialize_mongo_object))
    else:
        return {}
    
def obtener_por_codigo_barra(codigo):  # http://localhost:5000/api/art?barra=193134010546
    collection = db['Articulos']
    if not codigo:
        return []
    try:
        codigo_int = int(codigo)
    except ValueError:
        return []

    queries = [
        {"CodigoBarras": codigo_int},
        {"CodigoAlternativo2": codigo_int},
        {"CodigoBarras": codigo_int},
        {"CodigoAlternativo": int("0" + codigo)},
        {"CodigoAlternativo2": int("0" + codigo)},
        {"CodigoAlternativo3": int("0" + codigo)},
    ]
    results = collection.find({"$and": [{"$or": queries}, {"CodigoEmpresa": "99"}]})
    
    serialized_results = []
    for r in results:
        serialized = json.loads(json.dumps(r, default=serialize_mongo_object))
        serialized.pop('_id', None)
        serialized_results.append(serialized)
    
    return serialized_results

def obtener_precio_articulo_nombre(nombre_articulo): #http://localhost:5000/api/art?preuart=mouse
    collection = db['Articulos']
    search_terms = nombre_articulo.split(',')
    search_string = " ".join(['"' + term + '"' for term in search_terms])

    fields = {"NombreArticulo": 1, "PrecioVenta": 1, "CodigoArticulo": 1}
    results = collection.find({"$text": {"$search": search_string}}, fields)

    serialized_results = []
    for r in results:
        serialized = json.loads(json.dumps(r, default=serialize_mongo_object))
        serialized.pop('_id', None)
        serialized_results.append(serialized)
    
    return serialized_results

def obtener_precio_articulo_codigo(codigo):         #http://localhost:5000/api/art?codepreu=1007
    collection = db['Articulos']    
    if codigo:
        try:
            codigo = int(codigo)
        except ValueError:
            pass  
    else:
        return {} 

    fields = {"NombreArticulo": 1, "CodigoArticulo": 1, "PrecioVenta": 1, "_id": 0}
    result = collection.find_one({"CodigoArticulo": codigo, "CodigoEmpresa": "99"}, projection=fields)

    if result:
        return json.loads(json.dumps(result, default=serialize_mongo_object))
    else:
        return {}

def obtener_por_nombre_all(nombre_articulo): #http://localhost:5000/api/art?all=mouse
    collection = db['Articulos']
    search_terms = nombre_articulo.split(',')
    search_string = " ".join(['"' + term + '"' for term in search_terms])

    results = collection.find({"$text": {"$search": search_string}, "CodigoEmpresa": "99"})

    serialized_results = []
    for r in results:
        serialized = json.loads(json.dumps(r, default=serialize_mongo_object))
        serialized.pop('_id', None)
        filtered_serialized = {k: v for k, v in serialized.items() if v and str(v).strip()}
        serialized_results.append(filtered_serialized)
    
    return serialized_results

def obtener_por_code_all(codigo):         #http://localhost:5000/api/art?allcode=1007
    collection = db['Articulos']    
    if codigo:
        try:
            codigo = int(codigo)
        except ValueError:
            pass  
    else:
        return {} 

    result = collection.find_one({"CodigoArticulo": codigo, "CodigoEmpresa": "99"}, projection={"_id": 0})

    if result:
        return json.loads(json.dumps(result, default=serialize_mongo_object))
    else:
        return {}