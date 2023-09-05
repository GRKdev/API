from flask import request, jsonify
from extensions import app
from functions.clientes_f import ( 
    obtener_direccion_cliente, obtener_email_cliente, obtener_por_nombre_cliente,
    obtener_telefono_cliente, obtener_por_nombre_all, obtener_por_tlf,
    obtener_albaranes_por_nombre_cliente
)

@app.route('/api/cli', methods=['GET'])

def get_clientes():
    params_mapping = {
        'info': obtener_por_nombre_cliente,
        'tlf': obtener_telefono_cliente,
        'mail': obtener_email_cliente,
        'dire': obtener_direccion_cliente,
        'all': obtener_por_nombre_all,
        'clitlf': obtener_por_tlf,
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
    if not combined_results:
        return jsonify({'error': 'Parámetro no reconocido o faltante'}), 400
    return jsonify(combined_results)

@app.route('/api/cli/alb', methods=['GET'])
def get_info_albaranes():
    nombre_cliente = request.args.get('info')
    cliente = obtener_por_nombre_cliente(nombre_cliente)

    if not cliente:
        return jsonify({'error': f'Cliente {nombre_cliente} no encontrado'}), 404

    primer_cliente = cliente[0] if isinstance(cliente, list) else cliente
    albaranes = obtener_albaranes_por_nombre_cliente(primer_cliente['NombreCliente'])

    if not albaranes:
        return jsonify({'error': f'Albaranes del cliente {nombre_cliente} no encontrados'}), 404

    detalles = ['NumeroAlbaran']
    albaranes_filtered = [{k: albaran[k] for k in detalles if k in albaran} for albaran in albaranes]

    return jsonify({"albaranes": albaranes_filtered})