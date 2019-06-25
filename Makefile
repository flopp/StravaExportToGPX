.PHONY: setup format

setup:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements-dev.txt

format:
	venv/bin/black strava2gpx.py
