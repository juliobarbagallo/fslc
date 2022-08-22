from http import HTTPStatus
from urllib.parse import urlencode
from flask import json
from app.api.model.bag import Bag


class TestBagHandler:
    @staticmethod
    def test_should_get_many_bags(test_client, session):
        bags = [
            {
                "volume": 10,
                "title": "A bag",
            },
            {"volume": 20, "title": "Another bag"},
            {"volume": 30, "title": "A backpack"},
        ]

        bag_ids = []
        for bag in bags:
            bag = Bag(volume=bag["volume"], title=bag["title"])
            session.add(bag)
            session.commit()
            bag_ids.append(bag.id)

        query = urlencode([("bag_id", x) for x in bag_ids])
        response = test_client.get(f"/bags/?{query}")
        assert response.status_code == HTTPStatus.OK
        assert len(bags) == len(response.get_json())

    @staticmethod
    def test_should_get_bag_by_id(test_client, session):
        bag = Bag(volume=10, title="A bag")
        session.add(bag)
        session.commit()

        response = test_client.get(f"/bags/{bag.id}")
        res = response.get_json()

        assert response.status_code == HTTPStatus.OK
        assert res["volume"] == 10
        assert res["title"] == "A bag"

    @staticmethod
    def test_should_create_bag(test_client):
        response = test_client.post(
            "/bags/",
            data=json.dumps({"volume": 5, "title": "Bag"}),
            content_type="application/json",
        )
        res = response.get_json()

        assert response.status_code == HTTPStatus.CREATED
        assert res["volume"] == 5
        assert res["title"] == "Bag"
