"""
Attendance Validation Constants
"""

import re

# Regex Patterns
TIME_FORMAT_REGEX = r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"  # HH:MM format

# Validation Rules
MIN_WORK_HOURS = 8  # Minimum hours to work per day
MAX_WORK_HOURS = 12  # Maximum hours to work per day
LATE_THRESHOLD_MINUTES = 15  # Minutes after start time to mark late
