"""
Payroll Error Constants
"""

# Error Codes
PAYROLL_NOT_FOUND = "PAYROLL_NOT_FOUND"
INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
INVALID_SALARY_SLIP = "INVALID_SALARY_SLIP"
DUPLICATE_PAYROLL = "DUPLICATE_PAYROLL"
CALCULATION_ERROR = "CALCULATION_ERROR"

# Error Messages
ERROR_MESSAGES = {
    PAYROLL_NOT_FOUND: "Payroll record not found",
    INSUFFICIENT_FUNDS: "Insufficient funds for salary processing",
    INVALID_SALARY_SLIP: "Invalid salary slip",
    DUPLICATE_PAYROLL: "Payroll already processed for this period",
    CALCULATION_ERROR: "Error in salary calculation",
}
