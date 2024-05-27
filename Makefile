requirements:
	pip install -r requirements.txt

server:
	gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:3000

celery:
	celery -A app.tasks.process_transaction.celery worker --loglevel=info -Q process_transaction

local-server:
	uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload --proxy-headers

migrate-down:
	alembic downgrade base

.PHONY: requirements server local-server