from pydantic import BaseModel, EmailStr
from typing import Optional

class LeadCreateRequest(BaseModel):
    loan_type: str
    loan_amount: float
    loan_tenure: int
    pan_number: str
    first_name: str
    last_name: str
    gender: Optional[str] = None
    mobile_number: str
    email: EmailStr
    dob: str
    pin_code: str

class LeadStatusRequest(BaseModel):
    mobile_number: Optional[str] = None
    basic_application_id: Optional[str] = None

class LeadCreateResponse(BaseModel):
    basic_application_id: str
    message: str

class LeadStatusResponse(BaseModel):
    status: str
    message: str 