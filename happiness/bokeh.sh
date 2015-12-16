#!/bin/sh

PYTHONPATH=$PWD DJANGO_SETTINGS_MODULE=webapp.settings bokeh serve viz/individual.py --log-level=info
