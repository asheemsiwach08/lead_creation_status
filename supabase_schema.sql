-- Supabase Database Schema for Lead Management
-- Run this SQL in your Supabase SQL Editor

-- Create leads table
CREATE TABLE IF NOT EXISTS leads (
    id BIGSERIAL PRIMARY KEY,
    basic_application_id VARCHAR(255) UNIQUE NOT NULL,
    customer_id VARCHAR(255),
    relation_id VARCHAR(255),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    mobile_number VARCHAR(15) NOT NULL,
    email VARCHAR(255),
    pan_number VARCHAR(10),
    loan_type VARCHAR(50) NOT NULL,
    loan_amount DECIMAL(15,2) NOT NULL,
    loan_tenure INTEGER NOT NULL,
    gender VARCHAR(10),
    dob VARCHAR(10), -- Store as YYYY-MM-DD format
    pin_code VARCHAR(10),
    basic_api_response JSONB, -- Store full Basic API response
    status VARCHAR(50) DEFAULT 'created',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_leads_basic_application_id ON leads(basic_application_id);
CREATE INDEX IF NOT EXISTS idx_leads_mobile_number ON leads(mobile_number);
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_leads_updated_at 
    BEFORE UPDATE ON leads 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- -- Enable Row Level Security (RLS)
-- ALTER TABLE leads ENABLE ROW LEVEL SECURITY;

-- -- Create policy for authenticated users (adjust based on your auth requirements)
-- CREATE POLICY "Allow authenticated users to read leads" ON leads
--     FOR SELECT USING (auth.role() = 'authenticated');

-- CREATE POLICY "Allow authenticated users to insert leads" ON leads
--     FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- CREATE POLICY "Allow authenticated users to update leads" ON leads
--     FOR UPDATE USING (auth.role() = 'authenticated');

-- Optional: Create a view for lead statistics
CREATE OR REPLACE VIEW lead_statistics AS
SELECT 
    COUNT(*) as total_leads,
    COUNT(CASE WHEN status = 'created' THEN 1 END) as created_leads,
    COUNT(CASE WHEN status = 'approved' THEN 1 END) as approved_leads,
    COUNT(CASE WHEN status = 'rejected' THEN 1 END) as rejected_leads,
    COUNT(CASE WHEN created_at >= NOW() - INTERVAL '24 hours' THEN 1 END) as leads_last_24h,
    COUNT(CASE WHEN created_at >= NOW() - INTERVAL '7 days' THEN 1 END) as leads_last_7d
FROM leads; 