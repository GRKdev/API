from flask import request, jsonify
from extensions import app
from functions.articulos_f import (obtener_por_nombre_articulo, obtener_por_codigo_articulo, 
                                 obtener_por_codigo_barra, obtener_precio_articulo_nombre, 
                                 obtener_precio_articulo_codigo, obtener_por_nombre_all, 
                                 obtener_por_code_all)
from functions.albaranes_f import obtener_por_numero_albaran
from functions.clientes_f import obtener_por_nombre_cliente

@app.route('/api/art', methods=['GET'])
def get_articulos():
    params_mapping = {
        'info': obtener_por_nombre_articulo,
        'code': obtener_por_codigo_articulo,
        'barra': obtener_por_codigo_barra,
        'preuart': obtener_precio_articulo_nombre,
        "codepreu": obtener_precio_articulo_codigo,
        "all": obtener_por_nombre_all,
        "allcode": obtener_por_code_all,        
    }
    combined_results = []
    for param, function in params_mapping.items():
        i = 1
        while True:
            value = request.args.get(f'{param}{i}' if i > 1 else param)
            if not value:
                break
            results = function(value)
            if isinstance(results, dict):
                results = [results]
            combined_results.extend(results)
            i += 1
    for articulo in combined_results:
        detalle_albaran = request.args.get('detalle_albaran')
        if detalle_albaran:
            albaran = obtener_por_numero_albaran(articulo['NumeroAlbaran'])
            if albaran:
                detalles = detalle_albaran.split(',')
                albaran_filtered = {k: albaran[k] for k in detalles if k in albaran}
                articulo['detalle_albaran'] = albaran_filtered
        detalle_cliente = request.args.get('detalle_cliente')
        if detalle_cliente:
            cliente = obtener_por_nombre_cliente(articulo['NombreCliente'])
            if cliente:
                detalles = detalle_cliente.split(',')
                cliente_filtered = {k: cliente[k] for k in detalles if k in cliente}
                articulo['detalle_cliente'] = cliente_filtered
    if not combined_results:
        return jsonify({'error': 'Parámetro no reconocido o faltante'}), 400
    
    return jsonify(combined_results)