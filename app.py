"""FQA REST API (CRUD)"""

import argparse
import os
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from routes import topics_api, users_api

api = Flask(__name__)

# Init Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "faq-api"
    }
)

# Register API blueprints
api.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
api.register_blueprint(topics_api.get_blueprint())
api.register_blueprint(users_api.get_blueprint())

# Default error handlers
@api.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)

@api.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)

@api.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)

@api.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)

# Default handler
if __name__ == '__main__':
    # parse inbound args
    parser = argparse.ArgumentParser(
        description="faq-api")
    parser.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    args = parser.parse_args()

    # get Flask server config
    port = int(os.environ.get('PORT', 5000))

    # check for debug mode and launch
    if args.debug:
        print("Running in debug mode")
        cors = CORS(api)
        api.run(host='0.0.0.0', port=port, debug=True)
    else:
        api.run(host='0.0.0.0', port=port, debug=False)