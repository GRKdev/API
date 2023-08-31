from flask import request, jsonify
from extensions import app
from functions.albaranes_f import obtener_por_numero_albaran
from functions.clientes_f import obtener_por_nombre_cliente


@app.route('/api/alb_stat', methods=['GET'])

def get_albaranes_stat():
    detalle_cliente = request.args.get('detalle_cliente')
    combined_results = []

    i = 1
    while True:
        numero_albaran_key = f'all{i}' if i > 1 else 'all'
        numero_albaran = request.args.get(numero_albaran_key)

        if not numero_albaran:
            break

        albaran = obtener_por_numero_albaran(numero_albaran)
        if not albaran:
            return jsonify({'error': f'Albarán {numero_albaran} no encontrado'}), 404

        if detalle_cliente:
            detalles = detalle_cliente.split(',')
            cliente = obtener_por_nombre_cliente(albaran['NombreCliente'])
            if not cliente:
                return jsonify({'error': f'Cliente del albarán {numero_albaran} no encontrado'}), 404

            cliente_filtered = {k: cliente[k] for k in detalles if k in cliente}
            combined_albaran = {**albaran, "cliente": cliente_filtered}
            combined_results.append(combined_albaran)
        else:
            combined_results.append(albaran)

        i += 1

    if not combined_results:
        return jsonify({'error': 'No se han proporcionado parámetros válidos'}), 400

    return jsonify(combined_results)
