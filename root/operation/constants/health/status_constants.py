"""
Health & Safety Status Constants
"""

# Incident Status
REPORTED = "REPORTED"
INVESTIGATING = "INVESTIGATING"
RESOLVED = "RESOLVED"
CLOSED = "CLOSED"

INCIDENT_STATUS_CHOICES = [
    (REPORTED, "Reported"),
    (INVESTIGATING, "Investigating"),
    (RESOLVED, "Resolved"),
    (CLOSED, "Closed"),
]

# Severity Level
MINOR = "MINOR"
MAJOR = "MAJOR"
CRITICAL = "CRITICAL"

SEVERITY_CHOICES = [
    (MINOR, "Minor"),
    (MAJOR, "Major"),
    (CRITICAL, "Critical"),
]
