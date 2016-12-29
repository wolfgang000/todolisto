#!/bin/bash
cp config/gae/app.yaml ./app.yaml
cp config/gae/appengine_config.py ./appengine_config.py
pip install -r config/gae/requirements.txt -t lib/
