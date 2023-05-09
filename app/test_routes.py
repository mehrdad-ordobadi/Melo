
def test_dashboard_not_logged_in(test_client):
    response = test_client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'login' in response.data

def test_logout_not_logged_in(test_client):
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'login' in response.data

# To test the dashboard and logout routes when the user is logged in,
# you need to create a test user and log in using that user. 
# Then, you can use the logged-in test client to make requests to the protected routes.
