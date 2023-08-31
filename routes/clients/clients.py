from flask import request, jsonify
from extensions import app
from functions.clientes_f import obtener_direccion_cliente, obtener_email_cliente, obtener_por_nombre_cliente, obtener_telefono_cliente, obtener_por_nombre_all, obtener_por_tlf


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
