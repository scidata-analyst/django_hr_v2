"""
Employee Validation Constants
"""

import re

# Regex Patterns
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
PHONE_REGEX = r"^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$"
EMPLOYEE_ID_REGEX = r"^EMP\d{6}$"

# Validation Rules
MIN_AGE = 18
MAX_AGE = 65
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 100
