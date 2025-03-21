#!/bin/bash
source venv/bin/activate && gunicorn -c config/gunicorn_config.py main:app
