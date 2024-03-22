collectstatic:
	poetry run python backend/manage.py collectstatic

migrations:
	poetry run python backend/manage.py makemigrations

migrate:
	poetry run python backend/manage.py migrate

run-server:
	poetry run python backend/manage.py runserver
	

watch:
	sass --watch frontend/scss/custom.scss frontend/css/custom.css