"""
This contains test fixtures and configuration for running tests.

"""
import os
import pytest
from app import app, db
from models import User, Artist, Event
from flask_login import login_user


"""
Configuration class for testing.

Attributes:
    TESTING (bool): Set to True for testing mode.
    SQLALCHEMY_DATABASE_URI (str): URI for the in-memory SQLite database for testing.
    SQLALCHEMY_TRACK_MODIFICATIONS (bool): Set to False to disable tracking modifications in SQLAlchemy.
"""


class TestConfig:
    TESTING = True
    # Use an in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


"""
Fixture for creating a test client and testing the Flask app"""


@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    flask_app.config['TESTING'] = True
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client 

    ctx.pop()


"""
Fixture for initializing the test database."""


@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    test_artist = Artist.query.filter_by(username='TestUser').first()
    if not test_artist:
        # Only create the test artist if it does not already exist
        artist = Artist(username='TestUser', password='testpassword', user_type='artist',
                        first_name='Test', last_name='User', artist_stagename='TestArtist',
                        artist_city='TestCity', artist_tags='TestTag')
        db.session.add(artist)
        db.session.commit()

    yield db

    db.drop_all()
