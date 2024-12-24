from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


app = Flask(__name__)

@app.route("/siginup")
def siginup():
    return True