"""
Global Status Constants
"""

# System Status
ACTIVE = "ACTIVE"
INACTIVE = "INACTIVE"
MAINTENANCE = "MAINTENANCE"
ARCHIVED = "ARCHIVED"

SYSTEM_STATUS_CHOICES = [
    (ACTIVE, "Active"),
    (INACTIVE, "Inactive"),
    (MAINTENANCE, "Maintenance"),
    (ARCHIVED, "Archived"),
]

# Priority Level
LOW = "LOW"
MEDIUM = "MEDIUM"
HIGH = "HIGH"
CRITICAL = "CRITICAL"

PRIORITY_CHOICES = [
    (LOW, "Low"),
    (MEDIUM, "Medium"),
    (HIGH, "High"),
    (CRITICAL, "Critical"),
]
