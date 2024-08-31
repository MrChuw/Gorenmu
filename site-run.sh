echo "Installing requirements"
python -m pip install -r requirements.txt
python -m pip install -r site-requirements.txt

echo "Generating Site"
python site/generate.py

echo "Starting server..."
python -m http.server 3400 --directory ./site/generated

