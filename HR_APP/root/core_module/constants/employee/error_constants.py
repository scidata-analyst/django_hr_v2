"""
Employee Error Constants
"""

# Error Codes
EMPLOYEE_NOT_FOUND = "EMPLOYEE_NOT_FOUND"
DUPLICATE_EMPLOYEE = "DUPLICATE_EMPLOYEE"
INVALID_EMAIL = "INVALID_EMAIL"
INVALID_PHONE = "INVALID_PHONE"
INVALID_EMPLOYEE_ID = "INVALID_EMPLOYEE_ID"
MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"

# Error Messages
ERROR_MESSAGES = {
    EMPLOYEE_NOT_FOUND: "Employee not found",
    DUPLICATE_EMPLOYEE: "Employee with this email or ID already exists",
    INVALID_EMAIL: "Invalid email address",
    INVALID_PHONE: "Invalid phone number",
    INVALID_EMPLOYEE_ID: "Invalid employee ID format",
    MISSING_REQUIRED_FIELD: "Required field is missing",
}
