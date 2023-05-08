from unittest.mock import patch

from venv import pytest
def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'homepage.html' in response.data

def test_dashboard(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'login' in response.data

def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logged out successfully' in response.data
