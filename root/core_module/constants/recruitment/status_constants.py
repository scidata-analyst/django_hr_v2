"""
Recruitment Status Constants
"""

# Job Status
OPEN = "OPEN"
CLOSED = "CLOSED"
ON_HOLD = "ON_HOLD"
FILLED = "FILLED"

JOB_STATUS_CHOICES = [
    (OPEN, "Open"),
    (CLOSED, "Closed"),
    (ON_HOLD, "On Hold"),
    (FILLED, "Filled"),
]

# Application Status
APPLIED = "APPLIED"
SHORTLISTED = "SHORTLISTED"
INTERVIEW = "INTERVIEW"
SELECTED = "SELECTED"
REJECTED = "REJECTED"
OFFER_EXTENDED = "OFFER_EXTENDED"

APPLICATION_STATUS_CHOICES = [
    (APPLIED, "Applied"),
    (SHORTLISTED, "Shortlisted"),
    (INTERVIEW, "Interview"),
    (SELECTED, "Selected"),
    (REJECTED, "Rejected"),
    (OFFER_EXTENDED, "Offer Extended"),
]
