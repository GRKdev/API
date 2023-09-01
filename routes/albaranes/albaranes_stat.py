from flask import request, jsonify
from extensions import app
from functions.albaranes_f_stat import obtener_importe_por_mes

@app.route('/api/alb_stat', methods=['GET'])
def get_albaran_stat():
    params_mapping = {
        'cli_mes': obtener_importe_por_mes,
    }
    combined_results = []
    for param, function in params_mapping.items():
        value = request.args.get(param)
        if value:
            results = function(value)
            if isinstance(results, dict):
                results = [results]
            combined_results.extend(results)
    
    if not combined_results:
        return jsonify({'error': 'Parámetro no reconocido o faltante'}), 400
    
    return jsonify(combined_results)
