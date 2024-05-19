import time
import calendar

# Define the timegm function
def timegm(tm):
    """Equivalent to calendar.timegm()"""
    return int(time.mktime(tm)) - time.timezone

# Patch the calendar module
calendar.timegm = timegm

# Ensure the patch is applied
assert calendar.timegm is timegm
"""daprgen test suite."""

print("Monkey patching calendar.timegm()...")
