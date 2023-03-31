#!/usr/bin/python3
"""
    Methods
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": ["0.0.0.0"]}})


@app.errorhandler(404)
def page_not_found(e):
    """404 handler"""
    return (jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def tear_down(exception):
    """Closes the current session"""
    storage.close()


if __name__ == "__main__":
    app_host = os.getenv('HBNB_API_HOST')
    app_port = os.getenv('HBNB_API_PORT')
    if (app_host is None):
        app_host = '0.0.0.0'

    if (app_port is None):
        app_port = 5000

    app.run(host=app_host, port=int(app_port), threaded=True)
