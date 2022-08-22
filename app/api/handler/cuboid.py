from http import HTTPStatus
from flask import Blueprint, jsonify, request
from app.api.model.cuboid import Cuboid
from app.api.schema.cuboid import CuboidSchema
from app.api.model.bag import Bag
from app.api.db import db

cuboid_api = Blueprint("cuboid_api", __name__)


@cuboid_api.route("/", methods=["GET"])
def list_cuboids():
    cuboid_ids = request.args.getlist("cuboid_id")
    cuboid_schema = CuboidSchema(many=True)
    cuboids = Cuboid.query.filter(Cuboid.id.in_(cuboid_ids)).all()

    return jsonify(cuboid_schema.dump(cuboids)), HTTPStatus.OK


@cuboid_api.route("/<int:cuboid_id>", methods=["GET"])
def get_cuboid(cuboid_id):
    cuboid_schema = CuboidSchema()
    cuboid = Cuboid.query.get(cuboid_id)

    if cuboid is None:
        return jsonify(message = "Cuboid not found."), HTTPStatus.NOT_FOUND

    return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.OK


@cuboid_api.route("/", methods=["POST"])
def create_cuboid():
    content = request.json

    cuboid_schema = CuboidSchema()
    cuboid = Cuboid(
        width=content["width"],
        height=content["height"],
        depth=content["depth"],
        bag_id=content["bag_id"],
    )

    bag = Bag.query.get(cuboid.bag_id)

    if bag is None:
        return jsonify(message = "Cuboid not found."), HTTPStatus.NOT_FOUND

    if bag.available_volume < cuboid.volume:
        return jsonify(message = "Insufficient capacity in bag"), HTTPStatus.UNPROCESSABLE_ENTITY

    db.session.add(cuboid)
    db.session.commit()

    return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.CREATED


@cuboid_api.route("/<int:cuboid_id>", methods=["PATCH"])
def update_cuboid(cuboid_id):
    content = request.json
    cuboid_schema = CuboidSchema()
    updated_cuboid = Cuboid(
        width=content.get("width"),
        height=content.get("height"),
        depth=content.get("depth"),
        bag_id=content.get("bag_id"),
    )
    cuboid = Cuboid.query.get(cuboid_id)

    if cuboid is None:
        return jsonify(message='The cuboid does not exist'), HTTPStatus.NOT_FOUND

    if not cuboid.bag.has_volume(cuboid.id, updated_cuboid):
        return jsonify(message = "Insufficient capacity in bag"), HTTPStatus.UNPROCESSABLE_ENTITY

    if updated_cuboid.width:
        cuboid.width = updated_cuboid.width
    
    if updated_cuboid.height:
        cuboid.height = updated_cuboid.height

    if updated_cuboid.depth:
        cuboid.depth = updated_cuboid.depth

    if updated_cuboid.bag_id:
        cuboid.bag_id = updated_cuboid.bag_id

    db.session.commit()
    return jsonify(cuboid_schema.dump(cuboid)), HTTPStatus.OK


@cuboid_api.route("/<int:cuboid_id>", methods=["DELETE"])
def delete_cuboid(cuboid_id):
    cuboid = Cuboid.query.get(cuboid_id)
    if cuboid is None:
        return jsonify(message='The cuboid does not exist'), HTTPStatus.NOT_FOUND
    db.session.delete(cuboid)
    db.session.commit()
    return jsonify(message="Cuboid successfully deleted"), HTTPStatus.OK