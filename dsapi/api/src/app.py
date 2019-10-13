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


@app.route("/dsapi/collections/add_keywords", methods=['PUT'])
def add_keywords():
    title = request.args.get("title")
    ownerId = request.args.get("ownerId")
    keywords = request.args.get("keywords")

    keywords = keywords.split("//")

    try:
        col(title, ownerId).add_keywords(keywords)

        return app.response_class(
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        print(e)
        return app.response_class(status=404, mimetype='application/json')


@app.route("/dsapi/collections/remove_keywords", methods=['PUT'])
def remove_keywords():
    title = request.args.get("title")
    ownerId = request.args.get("ownerId")
    keywords = request.args.get("keywords")

    keywords = keywords.split("//")

    try:
        col(title, ownerId).remove_keywords(keywords)

        return app.response_class(
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

        col(title, ownerId, start_date, end_date,
            original).extract_collection()

        return app.response_class(response=j.dumps("OK"), status=200,
                                  mimetype='application/json')
    except Exception as e:
        print(e)
        return app.response_class(status=404, mimetype='application/json')


@app.route("/dsapi/extraction/scrap_media", methods=['GET'])
def scrap_media():
    try:
        collection = request.args.get("collection")
        mode = request.args.get("mode")

        if mode.lower() in ('i', 'image', 'v', 'video'):
            extr(collection).media_csv_download(type_file=mode)
        elif mode.lower() in ('b', 'both'):
            extr(collection).media_csv_download(type_file='i')
            extr(collection).media_csv_download(type_file='v')
        else:
            return app.response_class(status=404, mimetype='application/json')

        return app.response_class(response=j.dumps("OK"), status=200,
                                  mimetype='application/json')
    except Exception as e:
        print(e)
        return app.response_class(status=404, mimetype='application/json')


@app.route("/dsapi/extraction/expand_text", methods=['GET'])
def expand_text():
    try:
        collection = request.args.get("collection")

        extr(collection).expand_text()

        return app.response_class(response=j.dumps("OK"), status=200,
                                  mimetype='application/json')
    except Exception as e:
        print(e)
        return app.response_class(status=404, mimetype='application/json')


@app.route("/dsapi/extraction/list_extracted_collections", methods=['GET'])
def list_extracted_collections():
    try:
        cols = extr.list_extracted_collections()

        return app.response_class(response=j.dump(cols), status=200,
                                  mimetype='application/json')
    except Exception as e:
        print(e)
        return app.response_class(status=404, mimetype='application/json')
