# coding: utf-8
from flask import Flask
from . import config

app = Flask(__name__)
app.secret_key = config.APP_FLASK_KEY