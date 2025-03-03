#!/bin/bash



echo "Activate venv"
source .venv_site/bin/activate

cd bot_site/static/ || exit
tailwindcss -i ./styles.css -o ./output.css -w

