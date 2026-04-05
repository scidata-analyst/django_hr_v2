"""
ESS (Employee Self Service) Status Constants
"""

# Request Status
PENDING = "PENDING"
APPROVED = "APPROVED"
REJECTED = "REJECTED"
CANCELLED = "CANCELLED"
ON_HOLD = "ON_HOLD"

REQUEST_STATUS_CHOICES = [
    (PENDING, "Pending"),
    (APPROVED, "Approved"),
    (REJECTED, "Rejected"),
    (CANCELLED, "Cancelled"),
    (ON_HOLD, "On Hold"),
]

# Request Type
LEAVE_REQUEST = "LEAVE_REQUEST"
EXPENSE_REQUEST = "EXPENSE_REQUEST"
ADVANCE_REQUEST = "ADVANCE_REQUEST"
DOCUMENT_REQUEST = "DOCUMENT_REQUEST"

REQUEST_TYPE_CHOICES = [
    (LEAVE_REQUEST, "Leave Request"),
    (EXPENSE_REQUEST, "Expense Request"),
    (ADVANCE_REQUEST, "Advance Request"),
    (DOCUMENT_REQUEST, "Document Request"),
]
