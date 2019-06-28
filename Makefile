.PHONY: setup format mypy

setup:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements-dev.txt

format:
	venv/bin/black strava2gpx.py

mypy:
	venv/bin/mypy strava2gpx.py

