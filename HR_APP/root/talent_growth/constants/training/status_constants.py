"""
Training Status Constants
"""

# Training Status
PLANNED = "PLANNED"
SCHEDULED = "SCHEDULED"
IN_PROGRESS = "IN_PROGRESS"
COMPLETED = "COMPLETED"
CANCELLED = "CANCELLED"

TRAINING_STATUS_CHOICES = [
    (PLANNED, "Planned"),
    (SCHEDULED, "Scheduled"),
    (IN_PROGRESS, "In Progress"),
    (COMPLETED, "Completed"),
    (CANCELLED, "Cancelled"),
]

# Training Type
ONBOARDING = "ONBOARDING"
SKILL_DEVELOPMENT = "SKILL_DEVELOPMENT"
COMPLIANCE = "COMPLIANCE"
LEADERSHIP = "LEADERSHIP"
TECHNICAL = "TECHNICAL"

TRAINING_TYPE_CHOICES = [
    (ONBOARDING, "Onboarding"),
    (SKILL_DEVELOPMENT, "Skill Development"),
    (COMPLIANCE, "Compliance"),
    (LEADERSHIP, "Leadership"),
    (TECHNICAL, "Technical"),
]
