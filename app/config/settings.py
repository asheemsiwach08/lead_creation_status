import os
from dotenv import load_dotenv
from typing import Dict

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # API Configuration
    API_TITLE = "HOM-i Lead Creation & Status API"
    API_DESCRIPTION = "API for Lead Creation, Status retrieval, and WhatsApp Integration"
    API_VERSION = "1.0.0"
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Basic Application API Configuration
    BASIC_APPLICATION_API_URL = os.getenv("BASIC_APPLICATION_API_URL", "")
    BASIC_APPLICATION_USER_ID = os.getenv("BASIC_APPLICATION_USER_ID", "")
    BASIC_APPLICATION_API_KEY = os.getenv("BASIC_APPLICATION_API_KEY", "")
    
    # AWS Configuration
    AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    
    # Gupshup WhatsApp API Configuration
    GUPSHUP_API_URL = os.getenv("GUPSHUP_API_URL", "https://api.gupshup.io/wa/api/v1/msg")
    GUPSHUP_API_KEY = os.getenv("GUPSHUP_API_KEY", "")
    GUPSHUP_SOURCE = os.getenv("GUPSHUP_SOURCE", "")
    GUPSHUP_SRC_NAME = os.getenv("GUPSHUP_SRC_NAME", "")
    
    # Gupshup WhatsApp Templates
    GUPSHUP_LEAD_CREATION_TEMPLATE_ID = os.getenv("GUPSHUP_LEAD_CREATION_TEMPLATE_ID", "")
    GUPSHUP_LEAD_STATUS_TEMPLATE_ID = os.getenv("GUPSHUP_LEAD_STATUS_TEMPLATE_ID", "")
    GUPSHUP_LEAD_CREATION_SRC_NAME = os.getenv("GUPSHUP_LEAD_CREATION_SRC_NAME", "")
    GUPSHUP_LEAD_STATUS_SRC_NAME = os.getenv("GUPSHUP_LEAD_STATUS_SRC_NAME", "")
    
    # Legacy WhatsApp API Configuration (fallback)
    WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "https://api.whatsapp.com/send")
    WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "")
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    
    # Loan Type Mapping
    LOAN_TYPE_MAPPING = {
        "home_loan": "HL",
        "home loan": "HL",
        "HOME LOAN": "HL",
        "Home Loan": "HL",
        "Home loan": "HL",
        "Home Loan": "HL",
        "Loan Against Property": "LAP",
        "Loan against property": "LAP",
        "Loan Against Property": "LAP",
        "loan_against_property": "LAP",
        "loan against property": "LAP",
        "LAP": "LAP",
        "lap": "LAP",
        "personal_loan": "PL",
        "business_loan": "BL",
        "car_loan": "CL",
        "education_loan": "EL"
    }

# Global settings instance
settings = Settings() 