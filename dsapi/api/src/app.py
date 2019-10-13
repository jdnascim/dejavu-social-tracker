from flask import Flask, request
from flask_json import FlaskJSON
from core.base_api import base_blueprint
import json as j
import os

from social_tracker_library import collection as col
from social_tracker_library import extractor as extr

app: Flask = Flask(__name__)
app.register_blueprint(base_blueprint)
json: FlaskJSON = FlaskJSON(app)

conf_json = os.path.dirname(os.path.abspath(__file__)) + "/conf.json"
col.conf_json = conf_json
extr.conf_json = conf_json


@app.route("/dsapi/collections/list_collections", methods=['GET'])
def list_collections():
    collections = col.list_collections(print_res=False)

    try:
        if collections is None:
            return app.response_class(status=404, mimetype='application/json')

        return app.response_class(
            response=j.dumps([col for col in collections]),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        print(e)
        return app.response_class(status=404, mimetype='application/json')


@app.route("/dsapi/extraction/extract_collection", methods=['GET'])
def extract_collection():
    try:
        title = request.args.get("title")
        ownerId = request.args.get("ownerId")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        original = request.args.get("original")

        res = col(title, ownerId, start_date, end_date,
                  original).extract_collection()

        return app.response_class(response=j.dumps(res), status=200,
                                  mimetype='application/json')
    except Exception as e:
        print(e)
        return app.response_class(status=404, mimetype='application/json')


@app.route("/dsapi/extraction/scrap_media", methods['GET'])
def scrap_media():
    try:
        collection = request.args.get("collection")
        mode = requests.args.get("mode")

        if mode.lower() == 'i':
            extr("")
