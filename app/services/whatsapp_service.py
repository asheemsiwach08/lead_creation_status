import httpx
import json
from app.config.settings import settings

class WhatsAppService:
    """Service for handling WhatsApp message sending using Gupshup API with different templates"""
    
    def __init__(self):
        self.api_url = settings.GUPSHUP_API_URL
        self.api_key = settings.GUPSHUP_API_KEY
        self.source = settings.GUPSHUP_SOURCE
        
        # Template configurations
        self.lead_creation_template_id = settings.GUPSHUP_LEAD_CREATION_TEMPLATE_ID
        self.lead_status_template_id = settings.GUPSHUP_LEAD_STATUS_TEMPLATE_ID
        self.lead_creation_src_name = settings.GUPSHUP_LEAD_CREATION_SRC_NAME
        self.lead_status_src_name = settings.GUPSHUP_LEAD_STATUS_SRC_NAME
    
    async def send_lead_creation_confirmation(self, customer_name: str, loan_type: str, basic_application_id: str, phone_number: str) -> dict:
        """
        Send lead creation confirmation message using Gupshup template
        
        Args:
            customer_name: Customer's full name
            loan_type: Type of loan
            basic_application_id: Generated basic application ID
            phone_number: Customer's phone number
            
        Returns:
            dict: Response with success status and message
        """
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
            'apikey': self.api_key,
            'cache-control': 'no-cache'
        }
        
        # Template parameters for lead creation
        template_params = [
            customer_name,
            # loan_type,
            basic_application_id
        ]
        
        data = {
            'channel': 'whatsapp',
            'source': self.source,
            'destination': phone_number,
            'src.name': self.lead_creation_src_name,
            'template': f'{{"id":"{self.lead_creation_template_id}","params":{json.dumps(template_params)}}}'
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    data=data,
                    timeout=30.0
                )
                
                # Gupshup API returns 202 for successful submissions
                if response.status_code in [200, 202]:
                    try:
                        response_data = response.json()
                        data_dict = response_data if isinstance(response_data, dict) else {"response": str(response_data)}
                    except json.JSONDecodeError:
                        data_dict = {"response": response.text}
                    
                    return {
                        "success": True,
                        "message": "Lead creation confirmation sent successfully",
                        "data": data_dict
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Failed to send lead creation confirmation. Status: {response.status_code}",
                        "data": {"error": response.text}
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "message": f"Error sending lead creation confirmation: {str(e)}",
                "data": {"error": str(e)}
            }
    
    async def send_lead_status_update(self, phone_number: str, name: str, status: str) -> dict:
        """
        Send lead status update message using Gupshup template
        
        Args:
            phone_number: Customer's phone number
            name: Customer's full name
            status: Current lead status
            
        Returns:
            dict: Response with success status and message
        """
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
            'apikey': self.api_key,
            'cache-control': 'no-cache'
        }
        
        # Template parameters for lead status
        template_params = [name, status]
        
        data = {
            'channel': 'whatsapp',
            'source': self.source,
            'destination': phone_number,
            'src.name': self.lead_status_src_name,
            'template': f'{{"id":"{self.lead_status_template_id}","params":{json.dumps(template_params)}}}'
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    data=data,
                    timeout=30.0
                )
                
                # Gupshup API returns 202 for successful submissions
                if response.status_code in [200, 202]:
                    try:
                        response_data = response.json()
                        data_dict = response_data if isinstance(response_data, dict) else {"response": str(response_data)}
                    except json.JSONDecodeError:
                        data_dict = {"response": response.text}
                    
                    return {
                        "success": True,
                        "message": "Lead status update sent successfully",
                        "data": data_dict
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Failed to send lead status update. Status: {response.status_code}",
                        "data": {"error": response.text}
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "message": f"Error sending lead status update: {str(e)}",
                "data": {"error": str(e)}
            }

# Global instance
whatsapp_service = WhatsAppService() 