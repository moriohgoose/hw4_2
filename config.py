from flask_sqlalchemy import SQLAlchemy
from flask import Flask


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


