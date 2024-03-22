collectstatic:
	poetry run python3 backend/manage.py collectstatic

migrations:
	poetry run python3 backend/manage.py makemigrations

migrate:
	poetry run python3 backend/manage.py migrate

run-server:
	poetry run python3 backend/manage.py runserver
	

watch:
	sass --watch frontend/scss/custom.scss frontend/css/custom.css

check-deploy:
	poetry run python3 backend/manage.py check --deploy


run-production-server:
	cd backend/ && gunicorn backend.mysite.wsgi:application


install:
	poetry install

update: install migrate collectstatic ;