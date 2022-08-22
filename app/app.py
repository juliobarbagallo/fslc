from flask import Flask
from app.api.db import config_db
from app.api.ma import config_ma
from app.api.handler.home import home_api
from app.api.handler.bag import bag_api
from app.api.handler.cuboid import cuboid_api


def create_app():
    _app = Flask(__name__)
    config_db(_app)
    config_ma(_app)

    _app.register_blueprint(home_api)
    _app.register_blueprint(bag_api, url_prefix="/bags")
    _app.register_blueprint(cuboid_api, url_prefix="/cuboids")

    return _app


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="port to listen on"
    )
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host="0.0.0.0", port=port)
