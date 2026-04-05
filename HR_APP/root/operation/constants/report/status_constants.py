"""
Report Status Constants
"""

# Report Status
DRAFT = "DRAFT"
SCHEDULED = "SCHEDULED"
GENERATED = "GENERATED"
FAILED = "FAILED"
ARCHIVED = "ARCHIVED"

REPORT_STATUS_CHOICES = [
    (DRAFT, "Draft"),
    (SCHEDULED, "Scheduled"),
    (GENERATED, "Generated"),
    (FAILED, "Failed"),
    (ARCHIVED, "Archived"),
]

# Report Type
MONTHLY = "MONTHLY"
QUARTERLY = "QUARTERLY"
ANNUAL = "ANNUAL"
CUSTOM = "CUSTOM"

REPORT_TYPE_CHOICES = [
    (MONTHLY, "Monthly"),
    (QUARTERLY, "Quarterly"),
    (ANNUAL, "Annual"),
    (CUSTOM, "Custom"),
]
