
import pytest
from datetime import datetime
from flask_login import login_user, current_user
from models import User, Artist, Event
from app import db

def test_dashboard_not_logged_in(test_client):
    response = test_client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'login' in response.data

def test_logout_not_logged_in(test_client):
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'login' in response.data

