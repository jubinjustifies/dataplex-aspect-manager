from logging import basicConfig, INFO
import uuid
from flask import jsonify, g, request, Flask, abort
from werkzeug.exceptions import MethodNotAllowed, UnsupportedMediaType
from src.app.helpers.utils import *
from src.app.helpers.constant import *
from src.app.routes.aspect_routes import aspect_bp
from src.app.models.api_responses import APIError


def create_app():
    basicConfig(level=INFO, format=LOGGING_FORMAT)
    app = Flask(__name__)
    app.register_blueprint(aspect_bp)

    @app.route('/ping', methods=[GET])
    def ping():
        return jsonify({"status": "success", "message": "App is running"}), 200

    @app.route('/health', methods=[GET])
    def health():
        return jsonify({"status": "live"}), 200

    @app.before_request
    def attach_request_id():
        request.id = str(uuid.uuid4())
        app.logger.info(f"[{request.id}] {request.method} {request.path}")
        g.request_id = request.id
    
    @app.after_request
    def add_request_id_to_response(response):
        try:
            data = response.get_json()
            if isinstance(data, dict) and REQUEST_ID not in data:
                data[REQUEST_ID] = g.get(REQUEST_ID)
                response.set_data(jsonify(data).get_data(as_text=True))
            return response
        except Exception:
            return jsonify(APIError(404).to_json()), 404
        
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify(APIError(404).to_json()), 404
    
    @app.errorhandler(MethodNotAllowed)
    def handle_405(error):
        return jsonify(APIError(405).to_json()), 405
    
    @app.before_request
    def enforce_json_content_type():
        if request.method in [POST, PUT, PATCH]:
            if request.content_type != 'application/json':
                abort(415)

    @app.errorhandler(UnsupportedMediaType)
    def handle_415(e):
        return jsonify(APIError(415).to_json()), 415
    
    @app.errorhandler(500)
    def handle_500(e):
        return jsonify(APIError(500).to_json()), 500
    
    return app
