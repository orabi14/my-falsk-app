from app import app

def test_home_page():
    """Test the home page route."""
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to My Flask App!" in response.data

def test_about_page():
    """Test the about page route."""
    client = app.test_client()
    response = client.get('/about')
    assert response.status_code == 200
    assert b"About This App" in response.data