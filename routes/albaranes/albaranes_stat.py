from flask import request, jsonify
from extensions import app
from functions.albaranes_f_stat import (
    obtener_importe_por_mes, obtener_totales_anuales_fact, obtener_meses_currentyear_fact,
    obtener_meses_selectedyear_fact, obtener_anos_meses_fact, obtener_anos_meses_ing
)

@app.route('/api/alb_stat', methods=['GET'])
def get_albaran_stat():
    params_mapping = {
        'cli_mes': obtener_importe_por_mes,
        'fact_total': obtener_totales_anuales_fact,
        'fact_cy': obtener_meses_currentyear_fact,
        'fact_sy': obtener_meses_selectedyear_fact,
        'fact_totalgroup': obtener_anos_meses_fact,
        'ing_totalgroup': obtener_anos_meses_ing

    }
    combined_results = []
    for param, function in params_mapping.items():
        value = request.args.get(param)
        if value or (param in ['fact_totalgroup', 'ing_totalgroup'] and param in request.args):
            if param in ['fact_totalgroup', 'ing_totalgroup']:
                results = function()
            else:
                results = function(value)
                
            if isinstance(results, dict):
                results = [results]
            combined_results.extend(results)

    if not combined_results:
        return jsonify({'error': 'Parámetro no reconocido o faltante'}), 400

    return jsonify(combined_results)
