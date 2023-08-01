#!/bin/bash
python3 -m venv env
source env/bin/activate
pip install -r api/requirements.txt
python api/app.py