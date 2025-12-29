from datetime import datetime
import pytz

def convert_time_range(start_datetime_str, end_datetime_str, from_timezone_str, to_timezone_strs):
    """
    Convert a datetime range from one timezone to multiple other timezones.

    Args:
        start_datetime_str (str): Start datetime in ISO format (e.g., '2023-12-01T10:00')
        end_datetime_str (str): End datetime in ISO format
        from_timezone_str (str): Source timezone (e.g., 'US/Eastern')
        to_timezone_strs (list[str]): List of target timezones

    Returns:
        list[dict]: List of dicts with 'timezone', 'start', 'end' keys, where start/end are datetime objects

    Raises:
        ValueError: If inputs are invalid
    """
    # Validate timezones
    try:
        from_tz = pytz.timezone(from_timezone_str)
    except pytz.exceptions.UnknownTimeZoneError:
        raise ValueError(f"Invalid source timezone: {from_timezone_str}")

    to_timezones = []
    for tz_str in to_timezone_strs:
        try:
            to_timezones.append(pytz.timezone(tz_str))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(f"Invalid target timezone: {tz_str}")

    # Parse datetimes
    try:
        start_dt = datetime.fromisoformat(start_datetime_str)
        end_dt = datetime.fromisoformat(end_datetime_str)
    except ValueError as e:
        raise ValueError(f"Invalid datetime format: {e}")

    # Validate range
    if start_dt >= end_dt:
        raise ValueError("Start datetime must be before end datetime")

    # Localize to source timezone
    start_localized = from_tz.localize(start_dt)
    end_localized = from_tz.localize(end_dt)

    # Convert to each target timezone
    results = []
    for to_tz in to_timezones:
        start_converted = start_localized.astimezone(to_tz)
        end_converted = end_localized.astimezone(to_tz)
        results.append({
            'timezone': to_tz.zone,
            'start': start_converted,
            'end': end_converted
        })

    return results
