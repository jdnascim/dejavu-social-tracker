from flask import Blueprint

base_blueprint = Blueprint('base_blueprint', __name__)


@base_blueprint.route("/healthcheck")
def healthcheck() -> str:
    return "OK"
