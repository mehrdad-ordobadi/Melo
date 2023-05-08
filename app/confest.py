import pytest
import app  # Replace 'yourapp' with your application's module name

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
