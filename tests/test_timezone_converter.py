import pytest
from datetime import datetime
import pytz
from timezone_converter import convert_time_range

def test_basic_conversion():
    """Test basic timezone conversion."""
    results = convert_time_range(
        '2023-12-01T10:00',
        '2023-12-01T11:00',
        'US/Eastern',
        ['US/Pacific', 'Europe/London']
    )

    assert len(results) == 2
    assert results[0]['timezone'] == 'US/Pacific'
    assert results[1]['timezone'] == 'Europe/London'

    # US/Eastern to US/Pacific is 3 hours behind
    expected_start_pacific = datetime(2023, 12, 1, 7, 0)
    assert results[0]['start'].replace(tzinfo=None) == expected_start_pacific
    assert results[0]['end'].replace(tzinfo=None) == datetime(2023, 12, 1, 8, 0)

    # US/Eastern to Europe/London is 5 hours ahead
    expected_start_london = datetime(2023, 12, 1, 15, 0)
    assert results[1]['start'].replace(tzinfo=None) == expected_start_london
    assert results[1]['end'].replace(tzinfo=None) == datetime(2023, 12, 1, 16, 0)

def test_dst_transition():
    """Test conversion across DST transition."""
    # March 12, 2023, is when DST starts in US (2am to 3am)
    results = convert_time_range(
        '2023-03-12T01:00',
        '2023-03-12T04:00',
        'US/Eastern',
        ['US/Pacific']
    )

    assert len(results) == 1
    start_converted = results[0]['start']
    end_converted = results[0]['end']

    # Check UTC times to avoid DST representation issues
    start_utc = start_converted.astimezone(pytz.utc)
    end_utc = end_converted.astimezone(pytz.utc)

    # 1am EST (before DST) = 6am UTC
    assert start_utc.hour == 6
    assert start_utc.day == 12

    # 4am EDT (after DST) = 8am UTC
    assert end_utc.hour == 8
    assert end_utc.day == 12

def test_invalid_source_timezone():
    """Test invalid source timezone."""
    with pytest.raises(ValueError, match="Invalid source timezone"):
        convert_time_range('2023-12-01T10:00', '2023-12-01T11:00', 'Invalid/TZ', ['US/Pacific'])

def test_invalid_target_timezone():
    """Test invalid target timezone."""
    with pytest.raises(ValueError, match="Invalid target timezone"):
        convert_time_range('2023-12-01T10:00', '2023-12-01T11:00', 'US/Eastern', ['Invalid/TZ'])

def test_invalid_datetime_format():
    """Test invalid datetime string."""
    with pytest.raises(ValueError, match="Invalid datetime format"):
        convert_time_range('invalid', '2023-12-01T11:00', 'US/Eastern', ['US/Pacific'])

def test_start_after_end():
    """Test start datetime after end."""
    with pytest.raises(ValueError, match="Start datetime must be before end datetime"):
        convert_time_range('2023-12-01T12:00', '2023-12-01T11:00', 'US/Eastern', ['US/Pacific'])

def test_empty_target_list():
    """Test empty target timezone list."""
    results = convert_time_range('2023-12-01T10:00', '2023-12-01T11:00', 'US/Eastern', [])
    assert results == []
