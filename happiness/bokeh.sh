#!/bin/sh

PYTHONPATH=$PWD DJANGO_SETTINGS_MODULE=webapp.settings bokeh serve viz/individual.py viz/individuals.py viz/team.py viz/teams.py --log-level=info --host=localhost:5006 --host=localhost:8001
