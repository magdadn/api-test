SERVICE =
IMAGE =
help:
	@echo 'Makefile                                                 '
	@echo '                                                         '
	@echo 'Usage:                                                   '
	@echo ' make build      build images                            '
	@echo ' make up         creates containers and starts service   '
	@echo ' make start      starts service containers               '
	@echo ' make stop       stops service containers                '
	@echo ' make down       stops service and removes containers    '
	@echo '                                                         '
	@echo ' make migrate    run migrations                          '
	@echo ' make test       run tests                               '
	@echo '
	@echo '                                                         '

build:
	docker-compose build

up:
	docker-compose up -d db

start:
	docker-compose start db

stop:
	docker-compose stop

down:
	docker-compose down

attach: ## Attach to api container
	docker attach api_app

shell: ## Shell into api container
	docker exec -it api_app /bin/bash

test: start
	docker-compose exec users_test.py

