#!/bin/bash

echo "Activate venv"
source .venv_site/bin/activate

echo "Installing requirements"
# pip install -r requirements.txt
pip install -r site-requirements.txt

echo "Starting Server"
python site_start.py


