"""
Employee Status Constants
"""

# Employee Status
ACTIVE = "ACTIVE"
INACTIVE = "INACTIVE"
ON_LEAVE = "ON_LEAVE"
TERMINATED = "TERMINATED"
SUSPENDED = "SUSPENDED"
RETIRED = "RETIRED"

EMPLOYEE_STATUS_CHOICES = [
    (ACTIVE, "Active"),
    (INACTIVE, "Inactive"),
    (ON_LEAVE, "On Leave"),
    (TERMINATED, "Terminated"),
    (SUSPENDED, "Suspended"),
    (RETIRED, "Retired"),
]

# Employment Type
FULL_TIME = "FULL_TIME"
PART_TIME = "PART_TIME"
CONTRACT = "CONTRACT"
INTERN = "INTERN"

EMPLOYMENT_TYPE_CHOICES = [
    (FULL_TIME, "Full Time"),
    (PART_TIME, "Part Time"),
    (CONTRACT, "Contract"),
    (INTERN, "Intern"),
]
