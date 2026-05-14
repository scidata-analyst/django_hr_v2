"""
Integration Status Constants
"""

# Integration Status
ACTIVE = "ACTIVE"
INACTIVE = "INACTIVE"
ERROR = "ERROR"
PENDING = "PENDING"

INTEGRATION_STATUS_CHOICES = [
    (ACTIVE, "Active"),
    (INACTIVE, "Inactive"),
    (ERROR, "Error"),
    (PENDING, "Pending"),
]

# Integration Type
API = "API"
WEBHOOK = "WEBHOOK"
DATABASE = "DATABASE"
FILE_SYNC = "FILE_SYNC"

INTEGRATION_TYPE_CHOICES = [
    (API, "API"),
    (WEBHOOK, "Webhook"),
    (DATABASE, "Database"),
    (FILE_SYNC, "File Sync"),
]
