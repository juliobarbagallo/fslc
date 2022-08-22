# pylint: skip-file
import pytest
from flask_migrate import upgrade
from app.app import create_app
from app.api.db import db as _db


@pytest.fixture(scope="session")
def testing_app():
    return create_app()


@pytest.fixture(scope="session")
def db(testing_app):
    with testing_app.app_context():
        _db.drop_all()
        _db.engine.execute("DROP TABLE IF EXISTS alembic_version")
        upgrade()


@pytest.fixture(scope="session")
def test_client(testing_app):
    with testing_app.test_client() as testclient:
        return testclient


@pytest.fixture(scope="function", autouse=True)
def session(testing_app, db, request):
    with testing_app.app_context():
        conn = _db.engine.connect()

        options = dict(bind=conn, binds={})
        sess = _db.create_scoped_session(options=options)

        sess.begin_nested()

        _db.session = sess
        yield sess

        sess.commit()
        conn.close()
