# HOM-i Lead Creation & Status API with WhatsApp Integration

## Product Overview

**Product Name:** Lead Creation & Status API with WhatsApp Integration  
**Product Type:** API Service for Lead Management  
**Department:** Technology / Product  
**Stakeholders:** Engineering, Product  
**Version:** 1.0  
**Last Updated:** July 2025

## Objective

This product provides an API service for Lead Creation, Lead Status retrieval, and WhatsApp notifications for customers. The system enables seamless lead collection, status tracking, and real-time updates for customers through HOM-i Chatbot and WhatsApp.

## Features

- **Lead Creation API**: Automate lead creation from HOM-i Chatbot with Basic Application API integration
- **Lead Status API**: Provide real-time lead status through chatbot and WhatsApp
- **WhatsApp Integration**: Send lead details and status updates via Gupshup WhatsApp with separate templates
- **Supabase Database Integration**: Store and manage lead data in Supabase database
- **Error Handling**: Comprehensive error handling for invalid data and failed API calls
- **Data Validation**: Robust validation for all input parameters
- **Basic Application API Integration**: Seamless integration with internal Basic Application API
- **Modular Architecture**: Clean, maintainable code structure with separation of concerns

## Recent Updates

- **Enhanced Lead Status API Logic** - Improved to handle both mobile number and basic_application_id scenarios:
  - If only mobile number provided: Fetches basic_application_id from database
  - If only basic_application_id provided: Fetches mobile number from database
  - If both provided: Uses them directly
  - Once both are available: Calls GetActivity API and sends response to WhatsApp
- **Enhanced WhatsApp Integration** - Implemented Gupshup WhatsApp with separate templates for lead creation and status updates
- **Fixed database type mismatch error** - Resolved issue with UUID strings being passed to bigint columns
- **Updated field names** - Changed from `application_id` to `basic_application_id` throughout the codebase
- **Enhanced type handling** - Added proper type conversion for database fields to prevent PostgreSQL errors
- **Code optimization** - Removed unnecessary debug prints and improved error handling
- Enhanced lead status retrieval logic to use only application ID and mobile number, removing email requirement
- Fixed date format error when saving to database (converted DD/MM/YYYY to YYYY-MM-DD format)
- Changed database column type to VARCHAR(10) for date storage
- Added proper error handling for Basic Application API status calls
- Added detailed error response handling for 500 errors with specific messages
- Updated leads endpoint to return structured error responses
- Avoided sending WhatsApp notifications on errors

## Project Structure

```
lead-creation-verification/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── api/                       # API layer
│   │   ├── __init__.py
│   │   ├── routes.py              # Main API router
│   │   └── endpoints/             # API endpoints
│   │       ├── __init__.py
│   │       ├── leads.py           # Lead-related endpoints
│   │       └── health.py          # Health check endpoints
│   ├── models/                    # Data models and schemas
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic models
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── basic_application_service.py  # Basic Application API integration
│   │   ├── database_service.py    # Supabase database integration
│   │   └── whatsapp_service.py    # WhatsApp integration
│   ├── config/                    # Configuration
│   │   ├── __init__.py
│   │   └── settings.py            # Application settings
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       └── validators.py          # Validation utilities
├── requirements.txt               # Python dependencies
├── requirements-dev.txt           # Development dependencies
├── env.example                    # Environment variables template
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose configuration
├── .dockerignore                  # Docker ignore file
├── .gitignore                     # Git ignore file
├── supabase_schema.sql            # Database schema
├── README.md                      # Project documentation
└── .cursor/                       # Cursor IDE configuration
    └── rules                      # Project rules and guidelines
```

## Architecture Overview

The project follows a clean, modular architecture with clear separation of concerns:

- **API Layer**: Handles HTTP requests and responses
- **Service Layer**: Contains business logic and external API integrations
- **Model Layer**: Defines data structures and validation
- **Config Layer**: Centralizes configuration management
- **Utils Layer**: Provides utility functions and helpers

**Note**: This API integrates with the Basic Application API for lead processing and stores lead data in Supabase database for local management and analytics.

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Docker and Docker Compose (for containerized deployment)
- Supabase account
- Gupshup WhatsApp Business API account

### Installation

#### Option 1: Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lead-creation-verification
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development dependencies (optional)**
   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your actual API keys and URLs
   ```

6. **Set up Supabase Database**
   - Create a Supabase project at https://supabase.com
   - Get your project URL and anon key from Settings > API
   - Add them to your `.env` file:
     ```
     SUPABASE_URL=your_supabase_project_url
     SUPABASE_KEY=your_supabase_anon_key
     ```
   - Run the SQL schema in Supabase SQL Editor (see `supabase_schema.sql`)

7. **Configure Gupshup WhatsApp**
   - Get your Gupshup API credentials from the Gupshup dashboard
   - Create two WhatsApp templates:
     - **Lead Creation Template**: For confirming lead creation
     - **Lead Status Template**: For status updates
   - Add the configuration to your `.env` file:
     ```
     GUPSHUP_API_KEY=your_gupshup_api_key
     GUPSHUP_SOURCE=your_whatsapp_source_number
     GUPSHUP_TEMPLATE_LEAD_CREATION=your_lead_creation_template_id
     GUPSHUP_TEMPLATE_LEAD_STATUS=your_lead_status_template_id
     GUPSHUP_SOURCE_LEAD_CREATION=your_lead_creation_source_name
     GUPSHUP_SOURCE_LEAD_STATUS=your_lead_status_source_name
     ```

8. **Run the application**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

9. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/api/v1/health

#### Option 2: Docker Deployment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lead-creation-verification
   ```

2. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your actual API keys and URLs
   ```

3. **Build and run with Docker Compose**
   ```bash
   # Build and start the application
   docker-compose up --build
   
   # Run in background
   docker-compose up -d --build
   
   # View logs
   docker-compose logs -f
   
   # Stop the application
   docker-compose down
   ```

4. **Or build and run with Docker directly**
   ```bash
   # Build the image
   docker build -t lead-creation-api .
   
   # Run the container
   docker run -d \
     --name lead-creation-api \
     -p 8000:8000 \
     --env-file .env \
     lead-creation-api
   ```

5. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/api/v1/health

## API Endpoints

### 1. Lead Creation API

**Endpoint:** `POST /api/v1/lead/create`

**Purpose:** Create a new lead with customer details and loan information. This API integrates with the Basic Application API endpoint `/api/v1/NewApplication/FullfilmentByBasic`.

**Request Body:**
```json
{
  "loan_type": "Home Loan",
  "loan_amount": 5000000,
  "loan_tenure": 20,
  "pan_number": "ABCDE1234F",
  "first_name": "John",
  "last_name": "Doe",
  "gender": "Male",
  "mobile_number": "9876543210",
  "email": "john.doe@example.com",
  "dob": "1990-01-01",
  "pin_code": "123456"
}
```

**Response:**
```json
{
          "basic_application_id": "ABC12345",
  "message": "Lead Created Successfully."
}
```

**Basic Application API Integration:**
The API automatically converts the request to the Basic Application API format:
```json
{
  "gender": "Male",
  "dateOfBirth": "1990-01-01",
  "annualIncome": 0,
  "id": "random-guid",
  "loanType": "HL",
  "loanAmountReq": 5000000,
  "customerId": "",
  "firstName": "John",
  "lastName": "Doe",
  "mobile": "9876543210",
  "email": "john.doe@example.com",
  "pincode": "123456",
  "city": "",
  "district": "",
  "state": "",
  "createdFromPemId": "",
  "pan": "ABCDE1234F",
  "remarks": "",
  "applicationAssignedToRm": "",
  "isLeadPrefilled": true,
  "includeCreditScore": true,
  "loanTenure": 20
}
```

**Validation Rules:**
- `loan_type`: Must be one of the supported loan types
- `loan_amount`: Must be greater than 0
- `loan_tenure`: Must be greater than 0
- `pan_number`: Must be in format ABCDE1234F (5 letters + 4 digits + 1 letter)
- `mobile_number`: Must be exactly 10 digits
- `pin_code`: Must be exactly 6 digits
- `email`: Must be valid email format

**Loan Type Mapping:**
- "Home Loan" → "HL"
- "Personal Loan" → "PL"
- "Business Loan" → "BL"
- "Car Loan" → "CL"
- "Education Loan" → "EL"

### 2. Lead Status API

**Endpoint:** `POST /api/v1/lead/status`

**Purpose:** Retrieve lead status using various identifiers.

**Request Body:**
```json
{
  "mobile_number": "9876543210",
  "basic_application_id": "ABC12345"
}
```

**Note:** Either mobile number or basic application ID must be provided.

**Response:**
```json
{
  "status": "Lead",
  "message": "Your lead status is: Lead"
}
```

**Possible Status Values:**
- Lead
- Login
- Section
- Disbursement
- Not Found (when no data is available)

### 3. Health Check

**Endpoint:** `GET /health`

**Purpose:** Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "HOM-i Lead API"
}
```

## WhatsApp Integration

The API automatically sends WhatsApp messages using Gupshup templates for:

1. **Lead Creation Confirmation**: When a lead is successfully created
   - Template Parameters: Customer Name, Loan Type, Basic Application ID
   - Uses dedicated lead creation template and source name

2. **Status Updates**: When lead status is retrieved
   - Template Parameters: Current Status
   - Uses dedicated status update template and source name

**Template Configuration:**
- **Lead Creation Template**: Sends confirmation with customer details and application ID
- **Lead Status Template**: Sends current status information
- Each template uses its own source name for proper branding
- Templates are pre-approved by WhatsApp for business messaging

**Gupshup API Integration:**
- Uses Gupshup WhatsApp Business API with template messaging
- Automatic template parameter substitution
- Separate source names for different message types
- Development mode logging when API is not configured

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Basic Application API Configuration
BASIC_APPLICATION_API_URL=https://dev-applicationservice.basichomeloan.com
BASIC_APPLICATION_USER_ID=your_user_id_here
BASIC_APPLICATION_API_KEY=your_api_key_here

# AWS Configuration
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key

# Gupshup WhatsApp API Configuration
GUPSHUP_API_URL=https://api.gupshup.io/wa/api/v1/msg
GUPSHUP_API_KEY=your_gupshup_api_key
GUPSHUP_SOURCE=your_whatsapp_source_number
GUPSHUP_LEAD_CREATION_TEMPLATE_ID=your_lead_creation_template_id
GUPSHUP_LEAD_STATUS_TEMPLATE_ID=your_lead_status_template_id
GUPSHUP_LEAD_CREATION_SRC_NAME=your_lead_creation_source_name
GUPSHUP_LEAD_STATUS_SRC_NAME=your_lead_status_source_name

# Supabase Database Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Environment Variables Explanation

- **BASIC_APPLICATION_API_URL**: Base URL for the Basic Application API
- **BASIC_APPLICATION_USER_ID**: User ID for Basic Application API authentication
- **BASIC_APPLICATION_API_KEY**: API key for Basic Application API authentication
- **AWS_REGION**: AWS region for Lambda function (default: ap-south-1)
- **AWS_ACCESS_KEY_ID**: AWS access key for Lambda invocation
- **AWS_SECRET_ACCESS_KEY**: AWS secret key for Lambda invocation
- **GUPSHUP_API_URL**: Gupshup WhatsApp API endpoint
- **GUPSHUP_API_KEY**: API key for Gupshup authentication
- **GUPSHUP_SOURCE**: Source phone number for WhatsApp messages
- **GUPSHUP_LEAD_CREATION_TEMPLATE_ID**: Template ID for lead creation messages
- **GUPSHUP_LEAD_STATUS_TEMPLATE_ID**: Template ID for status update messages
- **GUPSHUP_LEAD_CREATION_SRC_NAME**: Source name for lead creation messages
- **GUPSHUP_LEAD_STATUS_SRC_NAME**: Source name for status update messages
- **SUPABASE_URL**: Supabase project URL
- **SUPABASE_KEY**: Supabase anonymous key for database access

**Note**: Authentication signatures are generated dynamically using the AWS Lambda function `AuthSignatureLambda` for secure and centralized signature management.

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run tests with coverage
pytest --cov=app
```

### Test Coverage

The test suite includes:
- API endpoint testing
- Data validation testing
- Error handling testing
- Integration testing (mocked)

## Testing the API

### Using curl

**Create Lead:**
```bash
curl -X POST "http://localhost:8000/api/v1/lead/create" \
  -H "Content-Type: application/json" \
  -d '{
    "loan_type": "Home Loan",
    "loan_amount": 5000000,
    "loan_tenure": 20,
    "pan_number": "ABCDE1234F",
    "first_name": "John",
    "last_name": "Doe",
    "gender": "Male",
    "mobile_number": "9876543210",
    "email": "john.doe@example.com",
    "dob": "1990-01-01",
    "pin_code": "123456"
  }'
```

**Get Lead Status:**
```bash
curl -X POST "http://localhost:8000/api/v1/lead/status" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile_number": "9876543210"
  }'
```

### Using Python requests

```python
import requests

# Create lead
lead_data = {
    "loan_type": "Home Loan",
    "loan_amount": 5000000,
    "loan_tenure": 20,
    "pan_number": "ABCDE1234F",
    "first_name": "John",
    "last_name": "Doe",
    "gender": "Male",
    "mobile_number": "9876543210",
    "email": "john.doe@example.com",
    "dob": "1990-01-01",
    "pin_code": "123456"
}

response = requests.post("http://localhost:8000/api/v1/lead/create", json=lead_data)
print(response.json())

# Get status
status_data = {"mobile_number": "9876543210"}
response = requests.post("http://localhost:8000/api/v1/lead/status", json=status_data)
print(response.json())
```

## Error Handling

The API provides comprehensive error handling:

- **Validation Errors**: Detailed error messages for invalid input data
- **API Errors**: Proper HTTP status codes and error messages
- **Not Found**: Appropriate message when lead data is not found
- **Server Errors**: Internal server error handling with logging
- **Basic Application API Errors**: Proper error handling for external API failures

## Performance Requirements

- **Response Time**: API calls processed within 2-5 seconds
- **Throughput**: Handle up to 1000 requests per minute
- **Availability**: 99.9% uptime target

## Security Considerations

- PAN Number and Personal Information are securely handled
- Environment variables for sensitive configuration
- Input validation and sanitization
- HTTPS recommended for production deployment
- Authorization headers for Basic Application API integration

## Development

### Running in Development Mode

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running in Production

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Code Organization

The project follows these principles:
- **Single Responsibility**: Each module has a single, well-defined purpose
- **Dependency Injection**: Services are injected where needed
- **Configuration Management**: Centralized configuration handling
- **Error Handling**: Consistent error handling across all layers
- **Testing**: Comprehensive test coverage

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation using Python type annotations
- **httpx**: Async HTTP client for external API calls
- **python-dotenv**: Environment variable management
- **requests**: HTTP library for external API calls

### Development Dependencies
- **pytest**: Testing framework
- **pytest-asyncio**: Async testing support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is proprietary and confidential.

## Support

For technical support or questions, please contact the development team.

---

**Note:** This API is designed to integrate with HOM-i Chatbot, Basic Application API, and external WhatsApp services. Ensure proper configuration of external API endpoints and credentials before deployment. 