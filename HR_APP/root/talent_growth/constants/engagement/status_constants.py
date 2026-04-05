"""
Engagement Status Constants
"""

# Engagement Status
ACTIVE = "ACTIVE"
INACTIVE = "INACTIVE"
ON_TRACK = "ON_TRACK"
AT_RISK = "AT_RISK"

ENGAGEMENT_STATUS_CHOICES = [
    (ACTIVE, "Active"),
    (INACTIVE, "Inactive"),
    (ON_TRACK, "On Track"),
    (AT_RISK, "At Risk"),
]

# Engagement Type
SURVEY = "SURVEY"
FEEDBACK = "FEEDBACK"
MEETING = "MEETING"
EVENT = "EVENT"

ENGAGEMENT_TYPE_CHOICES = [
    (SURVEY, "Survey"),
    (FEEDBACK, "Feedback"),
    (MEETING, "Meeting"),
    (EVENT, "Event"),
]
