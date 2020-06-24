build:
	@echo "Building App via docker-compose"
	docker-compose -f docker-compose.yml build

run:
	@echo "Running via docker-compose WITHOUT -d"
	docker-compose -f docker-compose.yml up

run-service:
	@echo "Running via docker-compose as service"
	docker-compose -f docker-compose.yml up -d

down:
	@echo "Stopping docker-compose containers"
	docker-compose -f docker-compose.yml down

dev:
	@echo "Stopping docker-compose containers"
	docker-compose -f docker-compose-dev.yml up --build

test:
	@echo "Running Tests"
	python -m unittest project.rspv.tests.test_helper

coverage:
	@echo "Generating Coverage"
	@echo "Requires coverage to be installed"
	coverage run -m unittest project.rspv.tests.test_helper
	coverage report