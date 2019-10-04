from flask import Flask, request
from flask_json import FlaskJSON, as_json
from core.base_api import base_blueprint
import json as j
import os

from social_tracker_library import collection as col

app: Flask = Flask(__name__)
app.register_blueprint(base_blueprint)
json: FlaskJSON = FlaskJSON(app)

conf_json = os.path.dirname(os.path.abspath(__file__)) + "/conf.json"


@app.route("/ds-api/collections/list_collections", methods=['GET'])
def list_collections():
    col.conf_json = conf_json
    collections = col.list_collections(print_res=False)

    if collections is None:
        return app.response_class(status=404, mimetype='application/json')

    return app.response_class(
        response=j.dumps([col for col in collections]),
        status=200,
        mimetype='application/json'
    )
