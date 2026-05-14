"""
Attendance Status Constants
"""

# Attendance Status
PRESENT = "PRESENT"
ABSENT = "ABSENT"
LATE = "LATE"
HALF_DAY = "HALF_DAY"
LEAVE = "LEAVE"
HOLIDAY = "HOLIDAY"
WEEKEND = "WEEKEND"

ATTENDANCE_STATUS_CHOICES = [
    (PRESENT, "Present"),
    (ABSENT, "Absent"),
    (LATE, "Late"),
    (HALF_DAY, "Half Day"),
    (LEAVE, "Leave"),
    (HOLIDAY, "Holiday"),
    (WEEKEND, "Weekend"),
]

# Check-in/Check-out Status
CHECKED_IN = "CHECKED_IN"
CHECKED_OUT = "CHECKED_OUT"
NOT_CHECKED = "NOT_CHECKED"

CHECK_STATUS_CHOICES = [
    (CHECKED_IN, "Checked In"),
    (CHECKED_OUT, "Checked Out"),
    (NOT_CHECKED, "Not Checked"),
]
