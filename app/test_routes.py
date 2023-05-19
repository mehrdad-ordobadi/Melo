
import pytest
import os
from datetime import datetime
from flask_login import login_user, current_user
from models import User, Artist, Event
from app import db
from werkzeug.datastructures import FileStorage


def test_dashboard_not_logged_in(test_client):
    response = test_client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'login' in response.data

def test_logout_not_logged_in(test_client):
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'login' in response.data

def test_upload_no_album_details(test_client, init_database, mocker):
    # Mock current_user to simulate a logged in user
    mocker.patch('flask_login.utils._get_user', return_value=User(id=1))

    # Create a dummy file for testing
    with open('test.mp3', 'w') as f:
        f.write('Dummy file content')

    data = {
        'file': (open('test.mp3', 'rb'), 'test.mp3'),
        'cover': (None, ''),
        'album_title': 'test_album',
        'album_release_date': ''
    }

    response = test_client.post('/upload', data=data, content_type='multipart/form-data')

    os.remove('test.mp3')  # Cleanup after test

    with test_client.session_transaction() as session:
        flashed_messages = dict(session['_flashes'])
        print(flashed_messages)

    assert 'New albums require a release dates!' == flashed_messages['message']


# Test failure when an unauthenticated user tries to upload an album.
def test_upload_without_login(test_client, init_database):
    # Create a dummy file for testing
    with open('test.mp3', 'w') as f:
        f.write('Dummy file content')

    data = {
        'file': (open('test.mp3', 'rb'), 'test.mp3'),
        'cover': (None, ''),
        'album_title': 'test_album',
        'album_release_date': '2023-05-20'
    }

    response = test_client.post('/upload', data=data, content_type='multipart/form-data')

    os.remove('test.mp3')  # Cleanup after test

    # Here we expect the response status code to be 401 (Unauthorized) 
    # because the user is not logged in. But your actual status code may be different.
    assert response.status_code == 302
