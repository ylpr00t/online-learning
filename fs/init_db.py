from flask_sqlalchemy import SQLAlchemy
from . import config
from fs.init_app import app

app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy()