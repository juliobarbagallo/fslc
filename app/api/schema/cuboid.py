from app.api.ma import ma
from app.api.model.cuboid import Cuboid


class CuboidSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cuboid
        fields = ("id", "width", "height", "depth", "bag", "volume")

    id = ma.auto_field()
    width = ma.auto_field()
    height = ma.auto_field()
    depth = ma.auto_field()
    bag = ma.Nested("BagSchema", exclude=("cuboids",))
