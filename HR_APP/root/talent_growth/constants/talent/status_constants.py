"""
Talent Management Status Constants
"""

# Talent Pool Status
ACTIVE = "ACTIVE"
INACTIVE = "INACTIVE"
PROMOTED = "PROMOTED"
TRANSFERRED = "TRANSFERRED"

TALENT_POOL_STATUS_CHOICES = [
    (ACTIVE, "Active"),
    (INACTIVE, "Inactive"),
    (PROMOTED, "Promoted"),
    (TRANSFERRED, "Transferred"),
]

# Succession Status
IDENTIFIED = "IDENTIFIED"
DEVELOPED = "DEVELOPED"
READY = "READY"
PROMOTED = "PROMOTED"

SUCCESSION_STATUS_CHOICES = [
    (IDENTIFIED, "Identified"),
    (DEVELOPED, "Developed"),
    (READY, "Ready"),
    (PROMOTED, "Promoted"),
]
