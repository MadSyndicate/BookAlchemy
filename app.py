import os
from flask import Flask
# from flask_cors import CORS
# from flask_limiter import Limiter
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)

# TODO: Check if "needed" + imports
# CORS(app)  # This will enable CORS for all routes
# limiter = Limiter(app=app, key_func=get_remote_address)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)



#just once
"""
with app.app_context():
    db.create_all()
"""
