.PHONY: setup format run

setup:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements-dev.txt

format:
	venv/bin/black main.py

run:
	venv/bin/python main.py --strava-export data/export_11565561 --output out --filter-type Run --filter-type Hike
