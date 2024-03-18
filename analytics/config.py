import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_username = os.environ.get("DB_USERNAME", "postgres_piero")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT", "5432")
db_name = os.environ.get("DB_NAME", "mydatabase")

app = Flask(__name__)
conn_string = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config["SQLALCHEMY_DATABASE_URI"] = conn_string

print("This is the connection:\n")
print(conn_string)

db = SQLAlchemy(app)

app.logger.setLevel(logging.DEBUG)