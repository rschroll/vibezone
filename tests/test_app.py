import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_homepage(client):
    """Test GET request to homepage."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Time Zone Converter' in response.data

def test_valid_conversion(client):
    """Test valid form submission."""
    data = {
        'from_timezone': 'US/Eastern',
        'start_datetime': '2023-12-01T10:00',
        'end_datetime': '2023-12-01T11:00',
        'to_timezones': ['US/Pacific', 'Europe/London']
    }
    response = client.post('/', data=data)
    assert response.status_code == 200
    assert b'Converted Times' in response.data
    assert b'US/Pacific' in response.data
    assert b'Europe/London' in response.data
    # Check inputs are preserved
    assert b'value="US/Eastern"' in response.data
    assert b'value="2023-12-01T10:00"' in response.data

def test_invalid_source_timezone(client):
    """Test invalid source timezone."""
    data = {
        'from_timezone': 'Invalid/Timezone',
        'start_datetime': '2023-12-01T10:00',
        'end_datetime': '2023-12-01T11:00',
        'to_timezones': ['US/Pacific']
    }
    response = client.post('/', data=data)
    assert response.status_code == 200
    assert b'Invalid source timezone' in response.data

def test_invalid_target_timezone(client):
    """Test invalid target timezone."""
    data = {
        'from_timezone': 'US/Eastern',
        'start_datetime': '2023-12-01T10:00',
        'end_datetime': '2023-12-01T11:00',
        'to_timezones': ['Invalid/Timezone']
    }
    response = client.post('/', data=data)
    assert response.status_code == 200
    assert b'Invalid target timezone' in response.data

def test_missing_fields(client):
    """Test missing required fields."""
    data = {
        'from_timezone': 'US/Eastern',
        # missing start_datetime
        'end_datetime': '2023-12-01T11:00',
        'to_timezones': ['US/Pacific']
    }
    response = client.post('/', data=data)
    assert response.status_code == 200
    assert b'All fields are required' in response.data

def test_start_after_end(client):
    """Test start datetime after end."""
    data = {
        'from_timezone': 'US/Eastern',
        'start_datetime': '2023-12-01T12:00',
        'end_datetime': '2023-12-01T11:00',
        'to_timezones': ['US/Pacific']
    }
    response = client.post('/', data=data)
    assert response.status_code == 200
    assert b'Start datetime must be before end datetime' in response.data

def test_empty_to_timezones(client):
    """Test empty to_timezones list."""
    data = {
        'from_timezone': 'US/Eastern',
        'start_datetime': '2023-12-01T10:00',
        'end_datetime': '2023-12-01T11:00',
        'to_timezones': []
    }
    response = client.post('/', data=data)
    assert response.status_code == 200
    assert b'All fields are required' in response.data

def test_invalid_datetime_format(client):
    """Test invalid datetime format."""
    data = {
        'from_timezone': 'US/Eastern',
        'start_datetime': 'invalid-date',
        'end_datetime': '2023-12-01T11:00',
        'to_timezones': ['US/Pacific']
    }
    response = client.post('/', data=data)
    assert response.status_code == 200
    assert b'Invalid datetime format' in response.data
