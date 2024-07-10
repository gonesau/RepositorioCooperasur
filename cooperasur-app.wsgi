import sys
import logging

# ruta de linux al proyecto de flask
sys.path.insert(0, '/var/www/cooperasur-app')

# ruta de linux al ambiente virtual de flask
sys.path.insert(0, '/var/www/cooperasur-app/cooperasur-venv/lib/python3.11/site-packages')

# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Import and run the Flask app
from main import app as application
