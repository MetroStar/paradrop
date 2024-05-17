#!/usr/bin/env python3
from flask import Flask
from flask_restful import Api
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
# from flask_wtf.csrf import CSRFProtect
from flasgger import Swagger
from asgiref.wsgi import WsgiToAsgi
import logging
import sys
from config.config import FLASK_DEBUG, PARADROP_SECRET_KEY

# Set up logger
if FLASK_DEBUG:
    file_handler = logging.FileHandler(filename="debug_log.log")
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
        handlers=handlers,
    )
    logger = logging.getLogger()

else:
    file_handler = logging.FileHandler(filename="error_log.log")
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]
    logging.basicConfig(
        level=logging.ERROR,
        format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
        handlers=handlers,
    )
    logger = logging.getLogger()


# FLASK app Setup
# INITIALIZE FLASK APP

app = Flask(__name__)
app.debug = FLASK_DEBUG

# FLASK APP CONFIG
app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # Seconds => 1 hour
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SECRET_KEY"] = PARADROP_SECRET_KEY
app.config['TESTING'] = False
app.config['SWAGGER'] = {
    'title': 'paradrop Project API',
    'uiversion': 3,
    "version": "v1"
}

# Disabling CSRF protection by default. To enable CSRF protection
# on a specific endpoint, just add csrf_protection_enabled decorator
# from utils/csrf_protection file to the endpoint that you want to have
# CSRF protected.
app.config['WTF_CSRF_CHECK_DEFAULT'] = False

# INITIALIZE FLASK CSRF
# csrf = CSRFProtect(app)

swagger = Swagger(app)

# INITIALIZE FLASK SESSION
Session(app)

# INITIALIZE Bcrypt for bcrypt hash operations
bcrypt = Bcrypt(app)

# INITIALIZE FLASK API
api = Api(app)

# INITIALIZE CORS
CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://127.0.0.1:8000",
        "http://127.0.0.1:5000",
        "https://127.0.0.1",
        "http://127.0.0.1:8443",
        "https://localhost:8443",
        "https://localhost",
        "https://demo.paradrop.io"])

# Converting app from WSGI to ASGI
asgi_app = WsgiToAsgi(app)
