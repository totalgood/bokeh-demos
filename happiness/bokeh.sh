#!/bin/sh

PYTHONPATH=$PWD DJANGO_SETTINGS_MODULE=webapp.settings bokeh serve viz/individual.py --log-level=info --host=localhost:5006 --host=localhost:8001
