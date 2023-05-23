"""
This contains the SQLAlchemy database instance.

Attributes:
    db (SQLAlchemy): The SQLAlchemy database instance.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
