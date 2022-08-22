.PHONY: dev
dev:
		FLASK_APP=./app/app.py FLASK_ENV=development flask run

test:
		PYTHONPATH=. pytest --testdox -s

lint:
		pylint --load-plugins pylint_flask_sqlalchemy app

black:
		black --target-version=py39 .

migrate-up:
		FLASK_APP=./app/app.py flask db upgrade

migrate-down:
		FLASK_APP=./app/app.py flask db downgrade

migrate:
		FLASK_APP=./app/app.py flask db migrate
