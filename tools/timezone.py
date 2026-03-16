import datetime
import pytz


def get_current_time_in_timezone(timezone: str) -> str:
    """Return the current local time in a given timezone.
    Args:
        timezone: A valid timezone string like 'America/New_York'.
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.datetime.now(tz)
        return now.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return f"Error: {str(e)}"
