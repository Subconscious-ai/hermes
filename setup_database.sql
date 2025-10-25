-- Hermes Campaign Generator Database Schema
-- Execute this in the Supabase SQL Editor to create the campaigns table

CREATE TABLE IF NOT EXISTS campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    product_description TEXT NOT NULL,
    target_audience_urls JSONB NOT NULL,
    winning_insight_summary TEXT,
    full_subconscious_results JSONB,
    final_llm_prompt TEXT,
    generated_campaign JSONB
);

-- Create an index on created_at for faster queries
CREATE INDEX IF NOT EXISTS idx_campaigns_created_at ON campaigns(created_at DESC);

-- Enable Row Level Security (RLS) - Optional for hackathon, recommended for production
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows all operations for now (adjust for production)
CREATE POLICY "Enable all access for authenticated users" ON campaigns
    FOR ALL
    USING (true)
    WITH CHECK (true);
