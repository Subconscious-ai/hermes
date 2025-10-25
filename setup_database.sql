-- Hermes Campaign Generator Database Schema
-- Execute this in the Supabase SQL Editor to create the database tables

-- =============================================================================
-- Main Campaigns Table
-- Stores the complete campaign generation workflow and results
-- =============================================================================
CREATE TABLE IF NOT EXISTS campaigns (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- User inputs
    product_description TEXT NOT NULL,
    target_audience_urls JSONB NOT NULL, -- Array of LinkedIn URLs
    messaging_angles JSONB DEFAULT '[]'::JSONB, -- Optional messaging angles to test
    
    -- Processing status
    status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, failed
    error_message TEXT,
    
    -- Subconscious API Integration
    subconscious_experiment_id VARCHAR(255), -- Reference to Subconscious experiment
    subconscious_request JSONB, -- What we sent to Subconscious API
    subconscious_response JSONB, -- Full raw response from Subconscious API
    
    -- Processed Insights (extracted from Subconscious response)
    mindset_segments JSONB, -- Audience mindset breakdowns with percentages
    winning_insight_summary TEXT, -- Human-readable key finding
    audience_recommendations JSONB, -- Persona-based recommendations (Ins_3, Ins_4)
    amce_results JSONB, -- Average Marginal Component Effects data
    willingness_to_pay JSONB, -- WTP metrics by mindset
    
    -- OpenAI Integration
    openai_request JSONB, -- What we sent to OpenAI
    openai_response JSONB, -- Full response from OpenAI
    final_llm_prompt TEXT, -- The exact prompt sent to OpenAI
    
    -- Generated Output
    generated_campaign JSONB NOT NULL, -- Array of email objects
    
    -- Metadata
    generation_duration_seconds INTEGER, -- How long the entire process took
    api_costs JSONB DEFAULT '{}'::JSONB -- Track costs: {subconscious: 0, openai: 0}
);

-- =============================================================================
-- Experiment Results Table (Optional - for tracking Subconscious experiments)
-- Store detailed experiment data separately for analysis
-- =============================================================================
CREATE TABLE IF NOT EXISTS experiment_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Experiment metadata
    experiment_type VARCHAR(50), -- conjoint, survey, etc.
    sample_size INTEGER,
    confidence_level VARCHAR(20),
    
    -- Detailed results from Subconscious
    mindset_partworth JSONB, -- Detailed part-worth utilities by mindset
    attribute_importance JSONB, -- Which attributes matter most
    market_segments JSONB, -- Segment sizes and characteristics
    
    -- Raw data files (if needed for audit trail)
    calculations_data JSONB,
    amce_data JSONB,
    experiment_definition JSONB
);

-- =============================================================================
-- Generated Emails Table (Optional - for easier querying of individual emails)
-- Normalized storage of generated emails
-- =============================================================================
CREATE TABLE IF NOT EXISTS generated_emails (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Email details
    email_number INTEGER NOT NULL,
    subject VARCHAR(500) NOT NULL,
    preview_text VARCHAR(500),
    body TEXT NOT NULL,
    cta VARCHAR(200),
    
    -- Email metadata
    mindset_target VARCHAR(100), -- Which mindset this email targets (if personalized)
    estimated_effectiveness DECIMAL(5,2), -- Optional: predicted performance score
    
    UNIQUE(campaign_id, email_number)
);

-- =============================================================================
-- Indexes for Performance
-- =============================================================================
CREATE INDEX IF NOT EXISTS idx_campaigns_created_at ON campaigns(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_campaigns_subconscious_id ON campaigns(subconscious_experiment_id);
CREATE INDEX IF NOT EXISTS idx_experiment_results_campaign_id ON experiment_results(campaign_id);
CREATE INDEX IF NOT EXISTS idx_generated_emails_campaign_id ON generated_emails(campaign_id);

-- =============================================================================
-- Triggers
-- =============================================================================
-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- Row Level Security (RLS)
-- =============================================================================
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE experiment_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_emails ENABLE ROW LEVEL SECURITY;

-- Simple policy for hackathon (allow all operations)
-- TODO: Implement user-based policies for production
CREATE POLICY "Enable all access for now" ON campaigns
    FOR ALL
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Enable all access for now" ON experiment_results
    FOR ALL
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Enable all access for now" ON generated_emails
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- =============================================================================
-- Helpful Views
-- =============================================================================

-- View: Recent successful campaigns with key metrics
CREATE OR REPLACE VIEW recent_campaigns AS
SELECT 
    c.id,
    c.created_at,
    c.product_description,
    c.status,
    c.winning_insight_summary,
    jsonb_array_length(c.generated_campaign) as email_count,
    c.generation_duration_seconds,
    c.api_costs
FROM campaigns c
WHERE c.status = 'completed'
ORDER BY c.created_at DESC;

-- View: Campaign performance summary
CREATE OR REPLACE VIEW campaign_summary AS
SELECT 
    c.id,
    c.created_at,
    c.product_description,
    c.winning_insight_summary,
    jsonb_array_length(c.target_audience_urls) as audience_count,
    jsonb_array_length(c.generated_campaign) as email_count,
    c.mindset_segments->>'total_segments' as segment_count,
    c.status
FROM campaigns c
ORDER BY c.created_at DESC;

-- =============================================================================
-- Sample Data Insertion Function (for testing)
-- =============================================================================
CREATE OR REPLACE FUNCTION insert_sample_campaign()
RETURNS UUID AS $$
DECLARE
    new_campaign_id UUID;
BEGIN
    INSERT INTO campaigns (
        product_description,
        target_audience_urls,
        winning_insight_summary,
        generated_campaign,
        status
    ) VALUES (
        'Sample AI Marketing Tool',
        '["https://linkedin.com/in/sample"]'::JSONB,
        'Test insight summary',
        '[{"email_number": 1, "subject": "Test", "body": "Test body", "cta": "Click here"}]'::JSONB,
        'completed'
    )
    RETURNING id INTO new_campaign_id;
    
    RETURN new_campaign_id;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Comments for Documentation
-- =============================================================================
COMMENT ON TABLE campaigns IS 'Main table storing all campaign generation workflows and results';
COMMENT ON TABLE experiment_results IS 'Detailed Subconscious API experiment data for analysis';
COMMENT ON TABLE generated_emails IS 'Normalized storage of individual generated emails';
COMMENT ON COLUMN campaigns.status IS 'Workflow status: pending, processing, completed, failed';
COMMENT ON COLUMN campaigns.mindset_segments IS 'Audience segmentation from Subconscious API (e.g., Data-Driven Advocates 40%, Story Believers 60%)';
COMMENT ON COLUMN campaigns.api_costs IS 'JSON object tracking API costs: {"subconscious": 0, "openai": 0.05, "total": 0.05}';
