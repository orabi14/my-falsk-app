import pytest
from app import create_app  # Import your app factory function

@pytest.fixture
def client():
    """Set up test client for Flask app."""
    app = create_app()
    app.config['TESTING'] = True  # Enable testing mode
    return app.test_client()

def test_home_page(client):
    """Test the home page route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to My Flask App!" in response.data  # Ensure correct content

def test_about_page(client):
    """Test the about page route."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b"About This App" in response.data
