from http import HTTPStatus
from urllib.parse import urlencode
from flask import json
from app.api.model.bag import Bag
from app.api.model.cuboid import Cuboid


class TestCuboidGet:
    @staticmethod
    def test_should_get_all_cuboids(test_client, session):
        bag = Bag(volume=100, title="A bag")
        session.add(bag)
        session.commit()

        cuboids = [
            {"width": 2, "height": 2, "depth": 2, "bag_id": bag.id},
            {"width": 3, "height": 3, "depth": 3, "bag_id": bag.id},
            {"width": 4, "height": 4, "depth": 4, "bag_id": bag.id},
        ]

        cuboid_ids = []
        for a_cuboid in cuboids:
            cuboid = Cuboid(
                width=a_cuboid["width"],
                height=a_cuboid["height"],
                depth=a_cuboid["depth"],
                bag_id=bag.id,
            )
            session.add(cuboid)
            session.commit()
            cuboid_ids.append(cuboid.id)

        query = urlencode([("cuboid_id", x) for x in cuboid_ids])
        response = test_client.get(f"/cuboids/?{query}")
        res = response.get_json()

        assert response.status_code == HTTPStatus.OK
        assert len(cuboids) == len(res)

        for res_cuboid in res:
            assert res_cuboid["width"]
            assert res_cuboid["height"]
            assert res_cuboid["depth"]
            assert res_cuboid["bag"]["id"] == bag.id

    @staticmethod
    def test_should_get_cuboid_by_id(test_client, session):
        bag = Bag(volume=10, title="A bag")
        session.add(bag)
        session.commit()

        cuboid = Cuboid(width=1, height=2, depth=2, bag_id=bag.id)
        session.add(cuboid)
        session.commit()

        response = test_client.get(f"/cuboids/{cuboid.id}")
        res = response.get_json()

        assert response.status_code == HTTPStatus.OK
        assert res["width"] == 1
        assert res["height"] == 2
        assert res["depth"] == 2

    @staticmethod
    def test_should_get_with_volume(test_client, session):
        bag = Bag(volume=100, title="A bag")
        session.add(bag)
        session.commit()

        cuboid = Cuboid(width=4, height=4, depth=4, bag_id=bag.id)
        session.add(cuboid)
        session.commit()

        response = test_client.get(f"/cuboids/{cuboid.id}")
        res = response.get_json()

        assert response.status_code == HTTPStatus.OK
        assert res["volume"] == 64

    @staticmethod
    def test_should_return_not_found(test_client):
        response = test_client.get("/cuboids/0")
        assert response.status_code == HTTPStatus.NOT_FOUND


class TestCuboidCreate:
    @staticmethod
    def _before_each(session):
        bag = Bag(volume=2000, title="A bag")
        session.add(bag)
        session.commit()

        for _ in range(3):
            cuboid = Cuboid(width=10, height=10, depth=5, bag_id=bag.id)
            session.add(cuboid)

        session.commit()

        return bag

    @staticmethod
    def test_should_create_cuboid(test_client, session):
        bag = TestCuboidCreate._before_each(session)

        response = test_client.post(
            "/cuboids/",
            data=json.dumps({"width": 6, "height": 7, "depth": 8, "bag_id": bag.id}),
            content_type="application/json",
        )
        res = response.get_json()

        assert response.status_code == HTTPStatus.CREATED
        assert res["width"] == 6
        assert res["height"] == 7
        assert res["depth"] == 8
        assert res["bag"]["id"] == bag.id

    @staticmethod
    def test_should_fail_if_insufficient_capacity(test_client, session):
        bag = TestCuboidCreate._before_each(session)

        response = test_client.post(
            "/cuboids/",
            data=json.dumps({"width": 7, "height": 8, "depth": 9, "bag_id": bag.id}),
            content_type="application/json",
        )
        res = response.get_json()

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert res["message"] == "Insufficient capacity in bag"

    @staticmethod
    def test_should_return_not_found_if_no_bag(test_client):
        response = test_client.post(
            "/cuboids/",
            data=json.dumps({"width": 7, "height": 8, "depth": 9, "bag_id": 9999}),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.NOT_FOUND


#################################
# DO NOT modify the tests ABOVE #
# IMPLEMENT the tests BELOW     #
#################################


class TestCuboidUpdate:
    @staticmethod
    def _before_each(session):
        bag = Bag(volume=250, title="A bag")
        session.add(bag)
        session.commit()

        _cuboid = Cuboid(width=5, height=5, depth=5, bag_id=bag.id)
        session.add(_cuboid)

        cuboid = Cuboid(width=4, height=4, depth=4, bag_id=bag.id)
        session.add(cuboid)

        session.commit()

        return [bag, cuboid]

    @staticmethod
    def test_should_update_cuboid(test_client, session):
        # pylint: disable=unused-variable
        bag, cuboid = TestCuboidUpdate._before_each(session)

        # DO NOT modify the new_width, new_height and new_depth values.
        # The test case should pass with these values.
        new_width = 5
        new_height = 5
        new_depth = 5

        response = test_client.patch(
            f"/cuboids/{cuboid.id}",
            data=json.dumps({"width": new_width, "height": new_height, "depth": new_depth}),
            content_type="application/json",
        )

        assert response.status_code == HTTPStatus.OK

    @staticmethod
    def test_should_fail_if_insufficient_capacity(test_client, session):
        # pylint: disable=unused-variable
        bag, cuboid = TestCuboidUpdate._before_each(session)

        # DO NOT modify the new_width, new_height and new_depth values.
        # The test case should pass with these values.
        new_width = 6
        new_height = 6
        new_depth = 6

        response = test_client.patch(
            f"/cuboids/{cuboid.id}",
            data=json.dumps({"width": new_width, "height": new_height, "depth": new_depth}),
            content_type="application/json",
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @staticmethod
    def test_should_return_not_found_if_cuboid_doesnt_exists(test_client):
        new_width = 6
        new_height = 6
        new_depth = 6

        response = test_client.patch(
            "/cuboids/99",
            data=json.dumps({"width": new_width, "height": new_height, "depth": new_depth}),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.NOT_FOUND


class TestCuboidDelete:
    @staticmethod
    def _before_each(session):
        bag = Bag(volume=250, title="A bag")
        session.add(bag)
        session.commit()

        cuboid = Cuboid(width=4, height=4, depth=4, bag_id=bag.id)
        session.add(cuboid)
        session.commit()

        return cuboid

    @staticmethod
    def test_should_delete_the_cuboid(test_client, session):
        bag, cuboid = TestCuboidUpdate._before_each(session)
        response = test_client.delete(f"/cuboids/{cuboid.id}")
        assert response.status_code == HTTPStatus.OK

    @staticmethod
    def test_should_return_not_found_if_cuboid_doesnt_exists(test_client):
        response = test_client.delete("/cuboids/99")
        assert response.status_code == HTTPStatus.NOT_FOUND
