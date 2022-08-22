from flask_marshmallow import Marshmallow

ma = Marshmallow()


def config_ma(app):
    ma.init_app(app)
