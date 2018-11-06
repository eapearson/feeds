install:
	pip install -r requirements.txt
	pip install -r dev-requirements.txt

docs:
	-rm -r docs
	-rm -r docsource/internal_apis
	mkdir -p docs
	sphinx-apidoc --separate -o docsource/internal_apis feeds

test:
	# flake8 feeds
	pytest --verbose test --cov --cov-report html feeds -s

start:
	gunicorn --worker-class gevent --timeout 300 --workers 1 --bind :5000 feeds.server:app

.PHONY: test docs