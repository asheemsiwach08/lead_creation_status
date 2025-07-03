import os
from typing import Dict, Optional, List
from supabase import create_client, Client
from fastapi import HTTPException
from app.config.settings import settings


class DatabaseService:
    """Service for handling Supabase database operations"""
    
    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        
        if not self.supabase_url or not self.supabase_key:
            print("WARNING: Supabase credentials not configured.")
            print("Please set SUPABASE_URL and SUPABASE_KEY environment variables.")
            self.client = None
        else:
            try:
                self.client = create_client(self.supabase_url, self.supabase_key)
                print("Supabase client initialized successfully")
            except Exception as e:
                print(f"Error initializing Supabase client: {e}")
                self.client = None
    
    def save_lead_data(self, lead_data: Dict, basic_api_response: Dict) -> Dict:
        """
        Save lead data to Supabase database
        
        Args:
            lead_data: Original lead data from request
            basic_api_response: Response from Basic Application API
            
        Returns:
            Dict: Database operation result
        """
        if not self.client:
            raise HTTPException(
                status_code=500,
                detail="Supabase client not initialized. Check database configuration."
            )
        
        try:            
            # Extract basic application ID from Basic API response
            basic_application_id = (
                basic_api_response.get("result", {})
                .get("basicAppId")
            )
            
            if not basic_application_id:
                raise HTTPException(
                    status_code=400,
                    detail="Basic Application ID not found in Basic API response"
                )
            
            # Format date for database (convert DD/MM/YYYY to YYYY-MM-DD)
            dob = lead_data.get("dob", "")
            if dob:
                try:
                    if '/' in dob:
                        # Convert DD/MM/YYYY to YYYY-MM-DD
                        day, month, year = dob.split('/')
                        dob = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    elif 'T' in dob:
                        # If it's already in ISO format, extract just the date part
                        dob = dob.split('T')[0]
                except Exception as e:
                    dob = None
            
            # Prepare data for database with proper type handling
            relation_id = basic_api_response.get("result", {}).get("id")
            customer_id = basic_api_response.get("result", {}).get("primaryBorrower", {}).get("customerId")
            
            # Ensure string values for VARCHAR fields
            if relation_id is not None:
                relation_id = str(relation_id)
            if customer_id is not None:
                customer_id = str(customer_id)
            
            db_data = {
                "basic_application_id": str(basic_application_id),
                "customer_id": customer_id,
                "relation_id": relation_id,
                "first_name": str(lead_data.get("first_name", "")),
                "last_name": str(lead_data.get("last_name", "")),
                "mobile_number": str(lead_data.get("mobile_number", "")),
                "email": str(lead_data.get("email", "")),
                "pan_number": str(lead_data.get("pan_number", "")),
                "loan_type": str(lead_data.get("loan_type", "")),
                "loan_amount": float(lead_data.get("loan_amount", 0)),
                "loan_tenure": int(lead_data.get("loan_tenure", 0)),
                "gender": str(lead_data.get("gender", "")),
                "dob": str(dob) if dob else None,
                "pin_code": str(lead_data.get("pin_code", "")),
                "basic_api_response": basic_api_response,  # Store full response for reference
                "status": "created",
                "created_at": "now()"
            }
            
            
            # Insert data into leads table
            result = self.client.table("leads").insert(db_data).execute()
            
            if result.data:
                return {
                    "success": True,
                    "database_id": result.data[0].get("id"),
                    "basic_application_id": basic_application_id,
                    "message": "Lead data saved to database"
                }
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to save lead data to database"
                )
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )
    
    def get_lead_by_application_id(self, basic_application_id: str) -> Optional[Dict]:
        """
        Get lead data by basic application ID
        
        Args:
            basic_application_id: Basicpplication ID from Basic API
            
        Returns:
            Optional[Dict]: Lead data or None if not found
        """
        if not self.client:
            return None
        
        try:
            result = self.client.table("leads").select("*").eq("basic_application_id", basic_application_id).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            return None
    
    def get_lead_by_mobile(self, mobile_number: str) -> Optional[Dict]:
        """
        Get lead data by mobile number
        
        Args:
            mobile_number: Mobile number
            
        Returns:
            Optional[Dict]: Lead data or None if not found
        """
        if not self.client:
            return None
        
        try:
            result = self.client.table("leads").select("*").eq("mobile_number", mobile_number).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            return None
    
    
    def update_lead_status(self, basic_application_id: str, status: str) -> bool:
        """
        Update lead status
        
        Args:
            basic_application_id: Basic Application ID
            status: New status
            
        Returns:
            bool: Success status
        """
        if not self.client:
            return False
        
        try:
            result = self.client.table("leads").update({"status": status}).eq("basic_application_id", basic_application_id).execute()
            return bool(result.data)
            
        except Exception as e:
            return False
    
    def get_all_leads(self, limit: int = 100) -> List[Dict]:
        """
        Get all leads with pagination
        
        Args:
            limit: Number of records to return
            
        Returns:
            List[Dict]: List of lead records
        """
        if not self.client:
            return []
        
        try:
            result = self.client.table("leads").select("*").order("created_at", desc=True).limit(limit).execute()
            return result.data or []
            
        except Exception as e:
            return []


# Global database service instance
database_service = DatabaseService() 