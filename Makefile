



dev-services:
	docker-compose -f ./docker/docker-compose.dev.yml --env-file=./docker/docker-compose.dev.env up -d --build

head:
	alembic upgrade heads

autogenerate:
	alembic revision --autogenerate -m $(m)


set-python-path:
	export PYTHONPATH="$PYTHONPATH:$PWD"