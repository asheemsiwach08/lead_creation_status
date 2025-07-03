import re
from app.config.settings import settings

def validate_pan_number(pan: str) -> bool:
    """Validate PAN number format"""
    return bool(re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', pan))

def validate_mobile_number(mobile: str) -> bool:
    """Validate mobile number format"""
    return bool(re.match(r'^[0-9]{10}$', mobile))

def validate_pin_code(pin: str) -> bool:
    """Validate PIN code format"""
    return bool(re.match(r'^[0-9]{6}$', pin))

def validate_loan_amount(amount: float) -> bool:
    """Validate loan amount"""
    return amount > 0

def validate_loan_tenure(tenure: int) -> bool:
    """Validate loan tenure"""
    return tenure > 0

def validate_loan_type(loan_type: str) -> bool:
    """Validate loan type"""
    valid_types = settings.LOAN_TYPE_MAPPING.keys()
    return loan_type in valid_types 