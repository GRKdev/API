from extensions import  db
from utils import serialize_mongo_object
import json


def obtener_por_nombre_cliente(nombrecliente): #http://localhost:5000/api/cli?info=alvarez,soto
    collection = db['Clientes']
    search_terms = nombrecliente.split(',')
    search_string = " ".join(['"' + term + '"' for term in search_terms]) 

    fields = {"NombreCliente": 1, "Telefono": 1, "EMail1": 1}
    results = collection.find({"$text": {"$search": search_string}}, fields)

    serialized_results = []
    for r in results:
        serialized = json.loads(json.dumps(r, default=serialize_mongo_object))
        serialized.pop('_id', None)
        cleaned_serialized = {k: v for k, v in serialized.items() if v and str(v).strip()}
        serialized_results.append(cleaned_serialized)

    return serialized_results


def obtener_telefono_cliente(nombrecliente): #http://localhost:5000/api/cli?tlf=alvarez,soto
    collection = db['Clientes']
    search_terms = nombrecliente.split(',')
    search_string = " ".join(['"' + term + '"' for term in search_terms]) 
    results = collection.find({"$text": {"$search": search_string}}, 
                              {"NombreCliente": 1, "Telefono": 1, "Telefono2": 1, "Telefono3": 1})

    serialized_results = []
    for r in results:
        serialized = json.loads(json.dumps(r, default=serialize_mongo_object))
        serialized.pop('_id', None)

        cleaned_serialized = {k: v for k, v in serialized.items() if v and (isinstance(v, int) or v.strip())}
        serialized_results.append(cleaned_serialized)
    
    return serialized_results

def obtener_email_cliente(nombrecliente): #http://localhost:5000/api/cli?mail=alvarez,soto
    collection = db['Clientes']
    search_terms = nombrecliente.split(',')
    search_string = " ".join(['"' + term + '"' for term in search_terms]) 
    results = collection.find({"$text": {"$search": search_string}}, 
                              {"NombreCliente": 1, "EMail1": 1, "EMail2": 1})

    serialized_results = []
    for r in results:
        serialized = json.loads(json.dumps(r, default=serialize_mongo_object))
        serialized.pop('_id', None)

        cleaned_serialized = {k: v for k, v in serialized.items() if v and (isinstance(v, int) or v.strip())}
        serialized_results.append(cleaned_serialized)
    
    return serialized_results

def obtener_direccion_cliente(nombrecliente): #http://localhost:5000/api/cli?dire=alvarez,soto
    collection = db['Clientes']
    search_terms = nombrecliente.split(',')
    search_string = " ".join(['"' + term + '"' for term in search_terms]) 
    results = collection.find({"$text": {"$search": search_string}}, 
                              {"NombreCliente": 1, "Domicilio": 1, "Localidad": 1, "Municipio": 1, "ComunidadAutonoma":1})

    serialized_results = []
    for r in results:
        serialized = json.loads(json.dumps(r, default=serialize_mongo_object))
        serialized.pop('_id', None)

        cleaned_serialized = {k: v for k, v in serialized.items() if v and (isinstance(v, int) or v.strip())}
        serialized_results.append(cleaned_serialized)
    
    return serialized_results

def obtener_por_nombre_all(nombrecliente): #http://localhost:5000/api/cli?all=alvarez,soto
    collection = db['Clientes']
    search_terms = nombrecliente.split(',')
    search_string = " ".join(['"' + term + '"' for term in search_terms]) 
    results = collection.find({"$text": {"$search": search_string}})
    serialized_results = []
    for r in results:
        serialized = json.loads(json.dumps(r, default=serialize_mongo_object))
        serialized.pop('_id', None)
        cleaned_serialized = {k: v for k, v in serialized.items() if v and v.strip()}
        serialized_results.append(cleaned_serialized)
    return serialized_results

def obtener_por_tlf(telefono): #http://localhost:5000/api/cli?clitlf=123456789
    collection = db['Clientes']
    query = {
        "$or": [
            {"Telefono": {"$regex": f".*{telefono}$"}},
            {"Telefono2": {"$regex": f".*{telefono}$"}},
            {"Telefono3": {"$regex": f".*{telefono}$"}}
        ]
    }
    projection_fields = {
        "NombreCliente": 1,
        "Telefono": 1,
        "Telefono2": 1,
        "Telefono3": 1,
        "EMail1": 1,
        "_id": 0
    }
    results = collection.find(query, projection=projection_fields)
    serialized_results = []
    for r in results:
        serialized = json.loads(json.dumps(r, default=serialize_mongo_object))
        cleaned_serialized = {k: v for k, v in serialized.items() if v and (isinstance(v, int) or v.strip())}
        serialized_results.append(cleaned_serialized)

    return serialized_results
