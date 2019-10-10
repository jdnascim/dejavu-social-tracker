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
col.conf_json = conf_json


@app.route("/dsapi/collections/list_collections", methods=['GET'])
def list_collections():
    collections = col.list_collections(print_res=False)

    if collections is None:
        return app.response_class(status=404, mimetype='application/json')

    return app.response_class(
        response=j.dumps([col for col in collections]),
        status=200,
        mimetype='application/json'
    )


@app.route("/dsapi/collections/create", methods=['POST'])
@as_json
def create_collection():
    try:
        content = request.get_json()

        title = content['title']
        ownerId = content['ownerId']
        keywords = list(content['keywords'])
        start_date = content['start_date']

        col(title, ownerId, start_date).create(keywords)

        return app.response_class(status=200, mimetype='application/json')
    except Exception:
        return app.response_class(status=404)


@app.route("/dsapi/collection/itemCount")
@as_json
def item_count():
    try:
        content = request.get_json()

        title = content['title']
        ownerId = content['ownerId']
        start_date = content['start_date']
        end_date = content['end_date']
        original = content['original']

        col(title, ownerId, start_date, end_date, original).item_count()
    except Exception:
        return app.response_class(status=404)
