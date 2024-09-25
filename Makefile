SERVER_CONTAINER=landing_server

attach:
	docker exec -it $(SERVER_CONTAINER) bash

up:
	docker compose up -d

logs:
	docker compose logs -f

stop:
	docker compose stop

rm:
	docker compose rm

extract:
	docker exec -it $(SERVER_CONTAINER) poetry run python manage.py extract

install:
	docker exec -it $(SERVER_CONTAINER) poetry install

createsu:
	docker exec -it $(SERVER_CONTAINER) poetry run python manage.py createsuperuser

migrate:
	docker exec -it $(SERVER_CONTAINER) poetry run python manage.py makemigrations && docker exec -it $(SERVER_CONTAINER) poetry run python manage.py migrate

makemigrations:
	docker exec -it $(SERVER_CONTAINER) poetry run python manage.py makemigrations
	make fix-perms

shell:
	docker exec -it $(SERVER_CONTAINER) poetry run python manage.py shell

fix-perms: 
	sudo chown -R $(USER):$(USER) .
