"""
Attendance Error Constants
"""

# Error Codes
ATTENDANCE_NOT_FOUND = "ATTENDANCE_NOT_FOUND"
DUPLICATE_ATTENDANCE = "DUPLICATE_ATTENDANCE"
INVALID_DATE_RANGE = "INVALID_DATE_RANGE"
INVALID_CHECK_TIME = "INVALID_CHECK_TIME"
FUTURE_DATE_NOT_ALLOWED = "FUTURE_DATE_NOT_ALLOWED"
MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"

# Error Messages
ERROR_MESSAGES = {
    ATTENDANCE_NOT_FOUND: "Attendance record not found",
    DUPLICATE_ATTENDANCE: "Attendance record already exists for this date",
    INVALID_DATE_RANGE: "Invalid date range provided",
    INVALID_CHECK_TIME: "Invalid check-in/check-out time",
    FUTURE_DATE_NOT_ALLOWED: "Future dates are not allowed",
    MISSING_REQUIRED_FIELD: "Required field is missing",
}
