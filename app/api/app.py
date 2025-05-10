from flask import Flask, request, jsonify, send_file, render_template
import sys
import os

# Add the parent directory to the Python path so we can import operations_handler
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.operations_handler import create_or_update_aspect, create_or_update_aspect_type

app = Flask(__name__)

@app.route('/create_aspect')
def create_aspect_route():
    return send_file('templates/aspect.html')

@app.route('/api/aspect', methods=['POST', 'PUT'])
def aspect_api():
    app.logger.info("Received request at /api/aspect")
    data = request.get_json()
    if not data or 'data_product_id' not in data or 'aspect_type_id' not in data or 'aspect_data' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    app.logger.info(f"JSON fields - {data['data_product_id']} : {data['aspect_type_id']} : {data['aspect_data']}")
    create_or_update_aspect(data['data_product_id'], data['aspect_type_id'], data['aspect_data'])
    return jsonify({'status': 'Aspect updated successfully'})

@app.route('/create_aspect_type')
def create_aspect_type_route():
    return send_file('templates/aspect_type.html')

@app.route('/api/aspect_type', methods=['POST'])
def aspect_type_api():
    app.logger.info("Received request at /api/aspect_type")
    data = request.get_json()
    if not data or 'project_id' not in data or 'aspect_type_id' not in data or 'aspect_type_location' not in data or 'aspect_type_name' not in data or 'metadata_template' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    create_or_update_aspect_type(data['project_id'], data['aspect_type_id'], data['aspect_type_location'], data['aspect_type_name'], data['aspect_type_description'], data['metadata_template'])
    return jsonify({'status': 'Aspect type created successfully'})

if __name__ == '__main__':
    app.run(debug=True)