"""
Compliance Status Constants
"""

# Compliance Status
COMPLIANT = "COMPLIANT"
NON_COMPLIANT = "NON_COMPLIANT"
PENDING = "PENDING"
UNDER_REVIEW = "UNDER_REVIEW"

COMPLIANCE_STATUS_CHOICES = [
    (COMPLIANT, "Compliant"),
    (NON_COMPLIANT, "Non-Compliant"),
    (PENDING, "Pending"),
    (UNDER_REVIEW, "Under Review"),
]

# Compliance Type
LEGAL = "LEGAL"
REGULATORY = "REGULATORY"
POLICY = "POLICY"
AUDIT = "AUDIT"

COMPLIANCE_TYPE_CHOICES = [
    (LEGAL, "Legal"),
    (REGULATORY, "Regulatory"),
    (POLICY, "Policy"),
    (AUDIT, "Audit"),
]
