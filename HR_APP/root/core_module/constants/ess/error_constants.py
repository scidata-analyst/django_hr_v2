"""
ESS (Employee Self Service) Error Constants
"""

# Error Codes
REQUEST_NOT_FOUND = "REQUEST_NOT_FOUND"
INSUFFICIENT_BALANCE = "INSUFFICIENT_BALANCE"
INVALID_REQUEST_TYPE = "INVALID_REQUEST_TYPE"
REQUEST_ALREADY_PROCESSED = "REQUEST_ALREADY_PROCESSED"
MISSING_ATTACHMENTS = "MISSING_ATTACHMENTS"

# Error Messages
ERROR_MESSAGES = {
    REQUEST_NOT_FOUND: "Request not found",
    INSUFFICIENT_BALANCE: "Insufficient balance for this request",
    INVALID_REQUEST_TYPE: "Invalid request type",
    REQUEST_ALREADY_PROCESSED: "Request has already been processed",
    MISSING_ATTACHMENTS: "Required attachments are missing",
}
