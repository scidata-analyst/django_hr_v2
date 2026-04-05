"""
Payroll Status Constants
"""

# Salary Status
DRAFT = "DRAFT"
SUBMITTED = "SUBMITTED"
APPROVED = "APPROVED"
PROCESSED = "PROCESSED"
PAID = "PAID"
FAILED = "FAILED"

SALARY_STATUS_CHOICES = [
    (DRAFT, "Draft"),
    (SUBMITTED, "Submitted"),
    (APPROVED, "Approved"),
    (PROCESSED, "Processed"),
    (PAID, "Paid"),
    (FAILED, "Failed"),
]

# Payment Method
BANK_TRANSFER = "BANK_TRANSFER"
CHEQUE = "CHEQUE"
CASH = "CASH"

PAYMENT_METHOD_CHOICES = [
    (BANK_TRANSFER, "Bank Transfer"),
    (CHEQUE, "Cheque"),
    (CASH, "Cash"),
]
