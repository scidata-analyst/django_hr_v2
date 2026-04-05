"""
Onboarding Status Constants
"""

# Onboarding Status
NOT_STARTED = "NOT_STARTED"
IN_PROGRESS = "IN_PROGRESS"
COMPLETED = "COMPLETED"
ON_HOLD = "ON_HOLD"

ONBOARDING_STATUS_CHOICES = [
    (NOT_STARTED, "Not Started"),
    (IN_PROGRESS, "In Progress"),
    (COMPLETED, "Completed"),
    (ON_HOLD, "On Hold"),
]

# Task Status
PENDING = "PENDING"
IN_REVIEW = "IN_REVIEW"
APPROVED = "APPROVED"
REJECTED = "REJECTED"

TASK_STATUS_CHOICES = [
    (PENDING, "Pending"),
    (IN_REVIEW, "In Review"),
    (APPROVED, "Approved"),
    (REJECTED, "Rejected"),
]
