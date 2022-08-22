from http import HTTPStatus
from flask import Blueprint

home_api = Blueprint("home_api", __name__)


@home_api.route("/")
def run():
    return "Cuboids", HTTPStatus.OK
