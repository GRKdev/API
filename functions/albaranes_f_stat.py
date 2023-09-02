from extensions import db
from datetime import datetime

def obtener_importe_por_mes(nombre_cliente):  # http://localhost:5000/api/alb_stat?cli_mes=grk
    current_year = datetime.now().year  
    collection = db['CabeceraAlbaran']
    search_terms = nombre_cliente.split(',')
    search_string = " ".join(['"' + term + '"' for term in search_terms])

    nombre_real_cliente = collection.find_one({"$text": {"$search": search_string}}, {"NombreCliente": 1})
    if nombre_real_cliente:
        nombre_real_cliente = nombre_real_cliente.get("NombreCliente", "")
    else:
        nombre_real_cliente = "Desconocido"

    pipeline = [
        {"$match": {"$text": {"$search": search_string}}},
        {"$match": {"FechaAlbaran": {"$gte": datetime(current_year, 1, 1), "$lt": datetime(current_year + 1, 1, 1)}}},
        {
            "$group": {
                "_id": {"month": {"$month": "$FechaAlbaran"}},
                "ImporteTotal": {"$sum": "$ImporteFactura"}
            }
        },
        {"$sort": {"_id.month": 1}}
    ]

    results = collection.aggregate(pipeline)
    meses = [
        'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
    ]

    output_dict = {mes: "0 €" for mes in meses}

    for r in results:
        month = r["_id"]["month"]
        importe = r["ImporteTotal"]
        output_dict[meses[month - 1]] = f"{importe} €"

    return {
        "NombreCliente": nombre_real_cliente, 
        "Año": current_year,
        "IngresosMensuales": output_dict
    }

def obtener_totales_anuales(_=None): #http://localhost:5000/api/alb_stat?total=true
    collection = db['CabeceraAlbaran']
    pipeline = [
        {
            "$group": {
                "_id": {"year": {"$year": "$FechaAlbaran"}},
                "ImporteTotal": {"$sum": "$ImporteFactura"}
            }
        },
        {"$sort": {"_id.year": 1}}
    ]
    results = collection.aggregate(pipeline)
    output_list = []

    for r in results:
        year = r["_id"]["year"]
        importe = r["ImporteTotal"]
        output_list.append({"Año": year, "Cantidad": f"{importe} €"})
    return {
        "IngresosAnuales": output_list
    }

def obtener_meses_currentyear(value=None):    #http://localhost:5000/api/alb_stat?t_m_cy=true
    current_year = datetime.now().year 
    collection = db['CabeceraAlbaran']
    pipeline = [
        {"$match": {"FechaAlbaran": {"$gte": datetime(current_year, 1, 1), "$lt": datetime(current_year + 1, 1, 1)}}},
        {
            "$group": {
                "_id": {"month": {"$month": "$FechaAlbaran"}},
                "ImporteTotal": {"$sum": "$ImporteFactura"}
            }
        },
        {"$sort": {"_id.month": 1}}
    ]
    results = collection.aggregate(pipeline)
    meses = [
        'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
    ]
    output_dict = {mes: "0 €" for mes in meses}
    for r in results:
        month = r["_id"]["month"]
        importe = r["ImporteTotal"]
        output_dict[meses[month - 1]] = f"{importe} €"

    return {
        "IngresosMensuales": output_dict,
        "Año": current_year
    }

def obtener_meses_selectedyear(year):  # http://localhost:5000/api/alb_stat?t_m_y=2022
    selected_year = int(year)
    collection = db['CabeceraAlbaran']
    pipeline = [
        {"$match": {"FechaAlbaran": {"$gte": datetime(selected_year, 1, 1), "$lt": datetime(selected_year + 1, 1, 1)}}},
        {
            "$group": {
                "_id": {"month": {"$month": "$FechaAlbaran"}},
                "ImporteTotal": {"$sum": "$ImporteFactura"}
            }
        },
        {"$sort": {"_id.month": 1}}
    ]
    results = collection.aggregate(pipeline)
    meses = [
        'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
    ]
    output_dict = {mes: "0 €" for mes in meses}
    for r in results:
        month = r["_id"]["month"]
        importe = r["ImporteTotal"]
        output_dict[meses[month - 1]] = f"{importe} €"

    return {
        "IngresosMensuales": output_dict,
        "Año": selected_year

    }
