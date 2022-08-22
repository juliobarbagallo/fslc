from app.api.ma import ma
from app.api.model.bag import Bag


class BagSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Bag
        fields = (
            "id",
            "volume",
            "title",
            "cuboids",
            "payload_volume",
            "available_volume",
        )

    id = ma.auto_field()
    volume = ma.auto_field()
    title = ma.auto_field()
    cuboids = ma.Nested("CuboidSchema", many=True, exclude=("bag",))
