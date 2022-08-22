from app.api.model.bag import Bag
from app.api.model.cuboid import Cuboid


class TestBagModel:
    bag_data = [
        {
            "volume": 10,
            "title": "A bag with no cuboids",
            "payload_volume": 0,
            "available_volume": 10,
            "cuboids": [],
        },
        {
            "volume": 20,
            "title": "A bag with one cuboid",
            "payload_volume": 18,
            "available_volume": 2,
            "cuboids": [{"width": 3, "height": 2, "depth": 3}],
        },
        {
            "volume": 10,
            "title": "A bag with two cuboids",
            "payload_volume": 8,
            "available_volume": 2,
            "cuboids": [
                {"width": 1, "height": 2, "depth": 3},
                {"width": 1, "height": 2, "depth": 1},
            ],
        },
        {
            "volume": 100,
            "title": "A bag with three cuboid",
            "payload_volume": 99,
            "available_volume": 1,
            "cuboids": [
                {"width": 2, "height": 2, "depth": 2},
                {"width": 3, "height": 3, "depth": 3},
                {"width": 4, "height": 4, "depth": 4},
            ],
        },
    ]

    def test_bag_model(self, session):
        for each_bag in self.bag_data:
            bag = Bag(volume=each_bag["volume"], title=each_bag["title"])
            session.add(bag)
            session.commit()

            for cuboid in each_bag["cuboids"]:
                cuboid = Cuboid(
                    width=cuboid["width"],
                    height=cuboid["height"],
                    depth=cuboid["depth"],
                    bag_id=bag.id,
                )
                session.add(cuboid)
                session.commit()

            assert bag.volume == each_bag["volume"]
            assert bag.title == each_bag["title"]
            assert bag.payload_volume is each_bag["payload_volume"]
            assert bag.available_volume is each_bag["available_volume"]
