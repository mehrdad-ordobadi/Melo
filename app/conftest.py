import os
import pytest
from app import app, db
from models import User, Artist, Event
from flask_login import login_user

# Use app instance directly from your app module
@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    flask_app.config['TESTING'] = True
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()

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