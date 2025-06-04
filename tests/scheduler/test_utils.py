from datetime import datetime, timezone, timedelta
from internal.scheduler.job.implementation import fix_timezone

def test_fix_timezone_naive():
    """Test that naive datetime gets UTC timezone"""
    naive = datetime(2025, 6, 10, 12, 30)
    fixed = fix_timezone(naive)
    
    assert fixed.tzinfo == timezone.utc
    assert fixed.year == naive.year
    assert fixed.month == naive.month
    assert fixed.day == naive.day
    assert fixed.hour == naive.hour
    assert fixed.minute == naive.minute

def test_fix_timezone_aware():
    """Test that timezone-aware datetime gets converted to UTC"""
    moscow_tz = timezone(timedelta(hours=3))
    aware = datetime(2025, 6, 10, 12, 30, tzinfo=moscow_tz)
    fixed = fix_timezone(aware)
    
    assert fixed.tzinfo == timezone.utc
    assert fixed.hour == 9
    assert fixed.minute == 30
    assert fixed.year == aware.year
    assert fixed.month == aware.month
    assert fixed.day == aware.day
