from flask import Flask, request
from flask_restplus import Api, Resource
from flask_json import FlaskJSON
from core.base_api import base_blueprint
import json as j
import os
import traceback

from social_tracker_library import collection as col
from social_tracker_library import extractor as extr
from social_tracker_library import query_expansion as qe

app: Flask = Flask(__name__)
app.register_blueprint(base_blueprint)
json: FlaskJSON = FlaskJSON(app)

api = Api(app=app, version="1.0", title="DS API",
          description="API for features developed to the Dejavu Project")

col_namespace = api.namespace('dsapi/collections',
                              description='Collections')
qe_namespace = api.namespace('dsapi/query_expansion',
                             description='Query Expansion')
extr_namespace = api.namespace('dsapi/extractor',
                               description='Extractor')

# model = api.model('Name Model',
#                   {'name': fields.String(required=True, description="Name of\
#                                          the person", help="Name cannot be \
#                                          blank.")})

list_of_names = {}

conf_json = os.path.dirname(os.path.abspath(__file__)) + "/conf.json"
col.conf_json = conf_json
extr.conf_json = conf_json


@col_namespace.route("/list_collections")
class list_collections(Resource):

    @api.doc(responses={200: 'OK', 404: 'None Collections'})
    def get(self):
        collections = col.list_collections()

        try:
            if collections is None:
                return app.response_class(status=404,
                                          mimetype='application/json')

            return app.response_class(
                response=j.dumps([col for col in collections]),
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            print(traceback.format_exc())
            return app.response_class(status=404, mimetype='application/json')


@col_namespace.route("/create")
class create_collection(Resource):

    @api.doc(
             responses={200: 'OK', 404: 'Error'},
             params={"title": "collection's title",
                     "ownerId": "collection's owner",
                     "keywords": "new keywords"})
    def post(self):
        title = request.args.get("title")
        ownerId = request.args.get("ownerId")
        keywords = request.args.get("keywords")

        keywords = keywords.split("//")

        keywords = [k.strip() for k in keywords]

        try:
            cole = col(title, ownerId)

            if cole.exists():
                return app.response_class(status=404,
                                          mimetype='application/json')

            cole.create(keywords)

            return app.response_class(
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            print(traceback.format_exc())
            return app.response_class(status=404, mimetype='application/json')

@col_namespace.route("/add_keywords")
class add_keywords(Resource):
    @api.doc(responses={200: 'OK', 404: 'Error'},
             params={"title": "collection's title",
                     "ownerId": "collection's owner",
                     "keywords": "new keywords"})
    def put(self):
        title = request.args.get("title")
        ownerId = request.args.get("ownerId")
        keywords = request.args.get("keywords")

        keywords = keywords.split("//")

        keywords = [k.strip() for k in keywords]

        try:
            col(title, ownerId).add_keywords(keywords)

            return app.response_class(
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            print(traceback.format_exc())
            return app.response_class(status=404, mimetype='application/json')


@col_namespace.route("/remove_keywords")
class remove_keywords(Resource):
    @api.doc(responses={200: 'OK', 404: 'Error'},
             params={"title": "collection's title",
                     "ownerId": "collection's owner",
                     "keywords": "keywords to be deleted"})
    def delete(self):
        title = request.args.get("title")
        ownerId = request.args.get("ownerId")
        keywords = request.args.get("keywords")

        keywords = keywords.split("//")

        keywords = [k.strip() for k in keywords]

        try:
            col(title, ownerId).remove_keywords(keywords)

            return app.response_class(
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            print(traceback.format_exc())
            return app.response_class(status=404, mimetype='application/json')


@col_namespace.route("/delete_collection")
class delete_collection(Resource):
    @api.doc(responses={200: 'OK', 404: 'Error'},
             params={"title": "collection's title",
                     "ownerId": "collection's owner"})
    def delete(self):
        title = request.args.get("title")
        ownerId = request.args.get("ownerId")

        try:
            col(title, ownerId).delete()

            return app.response_class(
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            print(traceback.format_exc())
            return app.response_class(status=404, mimetype='application/json')


@qe_namespace.route("/tags_method")
class tags_method(Resource):
    @api.doc(responses={200: 'OK', 404: "Error"},
             params={"title": "collection's title",
                     "ownerId": "collection's owner",
                     "start_date": "collection's start date",
                     "end_date": "collection's end date",
                     "original": "only original items",
                     "limit_suggestion": "max number of new keywords",
                     "stopwords_analysis": "Stopwords filter",
                     "places_analysis": "geographical names filter",
                     "add": "whether add or just display the new keywords"
                     })
    def put(self):
        try:
            title = request.args.get("title")
            ownerId = request.args.get("ownerId")
            start_date = request.args.get("start_date")
            end_date = request.args.get("end_date")
            original = bool(request.args.get("original"))
            limit_suggestion = int(request.args.get("limit_suggestion"))
            stopwords_analysis = request.args.get("stopwords_analysis")
            places_analysis = request.args.get("places_analysis")
            add = bool(request.args.get("add"))

            cole = col(title, ownerId, start_date, end_date, original)

            qe(cole).Tags(limit_suggestion=limit_suggestion,
                          stopwords_analysis=stopwords_analysis,
                          places_analysis=places_analysis, ask_conf=False)

            return app.response_class(
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            print(traceback.format_exc())
            return app.response_class(status=404, mimetype='application/json')


@qe_namespace.route("/coocurrence_method")
class coocurrence_method(Resource):
    @api.doc(responses={200: 'OK', 404: "Error"},
             params={"title": "collection's title",
                     "ownerId": "collection's owner",
                     "start_date": "collection's start date",
                     "end_date": "collection's end date",
                     "original": "only original items",
                     "limit_suggestion": "max number of new keywords",
                     "add": "whether add or just display the new keywords"
                     })
    def put(self):
        try:
            title = request.args.get("title")
            ownerId = request.args.get("ownerId")
            start_date = request.args.get("start_date")
            end_date = request.args.get("end_date")
            original = bool(request.args.get("original"))
            limit_suggestion = int(request.args.get("limit_suggestion"))
            add = bool(request.args.get("add"))

            cole = col(title, ownerId, start_date, end_date, original)

            qe(cole).Cooccurrence(limit_suggestion=limit_suggestion, add=add)
        except Exception as e:
            print(traceback.format_exc())
            return app.response_class(status=404, mimetype='application/json')


@extr_namespace.route("/extract_collection")
class extract_collection(Resource):
    @api.doc(responses={200: 'OK', 404: 'Error'},
             params={"title": "collection's title",
                     "ownerId": "collection's owner",
                     "start_date": "collection's start date",
                     "end_date": "collection's end date",
                     "original": "only original items"})
    def get(self):
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
            print(traceback.format_exc())
            return app.response_class(status=404, mimetype='application/json')


@extr_namespace.route("/scrap_media")
class scrap_media(Resource):
    @api.doc(responses={200: 'OK', 404: 'Error'},
             params={"collection": "collection's title",
                     "mode": "(i)mage, (v)ideo, or (b)oth"})
    def get(self):
        try:
            collection = request.args.get("collection")
            mode = request.args.get("mode")

            if mode.lower() in ('i', 'image', 'v', 'video'):
                extr(collection).media_csv_download(type_file=mode)
            elif mode.lower() in ('b', 'both'):
                extr(collection).media_csv_download(type_file='i')
                extr(collection).media_csv_download(type_file='v')
            else:
                return app.response_class(status=404,
                                          mimetype='application/json')

            return app.response_class(response=j.dumps("OK"), status=200,
                                      mimetype='application/json')
        except Exception as e:
            print(traceback.format_exc())
            return app.response_class(status=404, mimetype='application/json')


@extr_namespace.route("/expand_text")
class expand_text(Resource):
    @api.doc(responses={200: 'OK', 404: 'Error'},
             params={"collection": "collection's title"})
    def get(self):
        try:
            collection = request.args.get("collection")

            extr(collection).expand_text()

            return app.response_class(response=j.dumps("OK"), status=200,
                                      mimetype='application/json')
        except Exception as e:
            print(traceback.format_exc())
            return app.response_class(status=404, mimetype='application/json')


@extr_namespace.route("/list_extracted_collections")
class list_extracted_collections(Resource):
    @api.doc(responses={200: 'OK', 404: 'Error'})
    def get(self):
        try:
            cols = extr.list_extracted_collections()

            return app.response_class(response=j.dumps(cols), status=200,
                                      mimetype='application/json')
        except Exception as e:
            print(traceback.format_exc())
            return app.response_class(status=404, mimetype='application/json')
