import pytest
from app import app, db, Customers

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_ECHO'] = True
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create the database tables
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after tests

def test_index(client):
    """Test if the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Please enter required fields" not in response.data

def test_submit_empty_form(client):
    """Test form submission with empty data."""
    response = client.post('/submit', data={
        'firstName': '',
        'exampleInputEmail1': '',
        'address': '',
        'country': '',
        'state': '',
        'zip': ''
    })
    assert response.status_code == 200
    assert b"Please enter required fields" in response.data

def test_submit_valid_form(client):
    """Test form submission with valid data."""
    response = client.post('/submit', data={
        'firstName': 'John Doe',
        'exampleInputEmail1': 'john@example.com',
        'address': '123 Elm Street',
        'country': 'USA',
        'state': 'CA',
        'zip': '90001'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Thank you for your submission. Our team will get back to you soon." in response.data

def test_404(client):
    """Test that a 404 error is handled correctly."""
    response = client.get('/non-existent-page')
    assert response.status_code == 404
    assert b"Page Not Found" in response.data

# def test_500(client):
#     """Simulate an Internal Server Error (500) to test error handling."""
#     # Temporarily replace the database connection to simulate a failure
#     original_uri = app.config['SQLALCHEMY_DATABASE_URI']
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
#     # Cause an intentional error by adding invalid data
#     with app.app_context():
#         db.drop_all()  # This will cause a failure since the table doesn't exist
        
#         response = client.post('/submit', data={
#             'firstName': 'John Doe',
#             'exampleInputEmail1': 'john@example.com',
#             'address': '123 Elm Street',
#             'country': 'USA',
#             'state': 'CA',
#             'zip': '90001'
#         })
#         print(response.data)
#         assert response.status_code == 500
#         assert b"Internal Server Error" in response.data
    
#     # Restore the original database URI
#     app.config['SQLALCHEMY_DATABASE_URI'] = original_uri

def test_405(client):
    """Test that a 405 error is handled correctly."""
    response = client.get('/submit')
    assert response.status_code == 405
    assert b"Method Not Allowed" in response.data
