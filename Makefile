run:
	python manage.py runserver

run_bot:
	python manage.py run_bot

test:
	pytest -v

lint:
	ruff check .

format:
	ruff format .

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

superuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

check:
	python manage.py check

setup:
	pip install -r requirements.txt
	python manage.py migrate
	python manage.py check
    pre-commit install
