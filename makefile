#!make

build-no-cache:
	docker-compose build --no-cache

build:
	docker-compose build

run: 
	docker-compose up

run-detached: 
	docker-compose up --detach

stop:
	docker-compose down
