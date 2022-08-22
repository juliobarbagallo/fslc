from app.api.model.bag import Bag
from app.api.model.cuboid import Cuboid


class TestCuboidModel:
    cuboid_data = [
        {"width": 3, "height": 3, "depth": 3, "volume": 27},
        {"width": 4, "height": 4, "depth": 4, "volume": 64},
    ]

    def test_cuboid_model(self, session):
        bag = Bag(volume=100, title="A bag")
        session.add(bag)
        session.commit()

        for each_cuboid in self.cuboid_data:
            cuboid = Cuboid(
                width=each_cuboid["width"],
                height=each_cuboid["height"],
                depth=each_cuboid["depth"],
                bag_id=bag.id,
            )

            assert cuboid.width == each_cuboid["width"]
            assert cuboid.height == each_cuboid["height"]
            assert cuboid.depth == each_cuboid["depth"]
            assert cuboid.volume is each_cuboid["volume"]
