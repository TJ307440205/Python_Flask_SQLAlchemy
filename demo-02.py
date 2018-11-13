from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# URI 配置: https://docs.sqlalchemy.org/en/latest/core/engines.html
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

