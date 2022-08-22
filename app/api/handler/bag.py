from http import HTTPStatus
from flask import Blueprint, jsonify, request
from app.api.model.bag import Bag
from app.api.schema.bag import BagSchema
from app.api.db import db

bag_api = Blueprint("bag_api", __name__)


@bag_api.route("/", methods=["GET"])
def list_bags():
    bag_ids = request.args.getlist("bag_id")
    bag_schema = BagSchema(many=True)
    bags = Bag.query.filter(Bag.id.in_(bag_ids)).all()

    return jsonify(bag_schema.dump(bags)), HTTPStatus.OK


@bag_api.route("/<int:bag_id>", methods=["GET"])
def get_bag(bag_id):
    bag_schema = BagSchema()
    bag = Bag.query.get(bag_id)

    if bag is None:
        return "", HTTPStatus.NOT_FOUND

    return jsonify(bag_schema.dump(bag)), HTTPStatus.OK


@bag_api.route("/", methods=["POST"])
def create_bag():
    content = request.json
    bag_schema = BagSchema()
    bag = Bag(volume=content["volume"], title=content["title"])
    db.session.add(bag)
    db.session.commit()

    return jsonify(bag_schema.dump(bag)), HTTPStatus.CREATED
