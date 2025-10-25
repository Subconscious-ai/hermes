# Database Schema Reference

## Overview

The updated schema now supports the complete Hermes workflow with real Subconscious API integration.

## Schema Design Principles

1. **Full Audit Trail**: Store raw requests/responses from both Subconscious and OpenAI
2. **Processed Insights**: Extract and store key insights separately for easy access
3. **Flexible JSONB**: Use JSONB for complex nested data structures
4. **Status Tracking**: Monitor campaign generation progress
5. **Cost Tracking**: Keep tabs on API usage costs

---

## Main Tables

### 1. `campaigns` (Primary Table)

Stores the complete campaign generation workflow.

**Key Fields:**

- **User Input**:
  - `product_description`: What the product/service is
  - `target_audience_urls`: LinkedIn profile URLs (JSONB array)
  - `messaging_angles`: Optional angles to test (JSONB array)

- **Status & Processing**:
  - `status`: `pending` → `processing` → `completed` / `failed`
  - `error_message`: If something goes wrong
  - `generation_duration_seconds`: Performance tracking

- **Subconscious Integration**:
  - `subconscious_experiment_id`: Reference ID from Subconscious
  - `subconscious_request`: What we sent
  - `subconscious_response`: Full raw response (like the florida_school data)
  - `mindset_segments`: Extracted segments (e.g., "Data-Driven Advocates: 40%")
  - `amce_results`: Marginal effects data
  - `willingness_to_pay`: WTP metrics by segment

- **Insights & Recommendations**:
  - `winning_insight_summary`: Human-readable key finding
  - `audience_recommendations`: Persona-based recommendations

- **OpenAI Integration**:
  - `final_llm_prompt`: Exact prompt sent to GPT-4
  - `openai_request`: Full request object
  - `openai_response`: Full response
  - `generated_campaign`: Final email array (JSONB)

- **Metadata**:
  - `api_costs`: `{"subconscious": 0, "openai": 0.05, "total": 0.05}`

---

### 2. `experiment_results` (Optional Detail Table)

Stores detailed Subconscious experiment data separately for analysis.

**When to use**: If you want to run analytics on experiment results without loading the full campaigns table.

**Key Fields:**
- `campaign_id`: Links to main campaign
- `mindset_partworth`: Detailed utility scores by mindset
- `attribute_importance`: Which factors matter most
- `calculations_data`: Raw calculation results
- `amce_data`: Full AMCE dataset

---

### 3. `generated_emails` (Optional Normalized Table)

Stores individual emails in normalized form.

**When to use**: If you want to query/filter individual emails easily.

**Key Fields:**
- `campaign_id`: Links to main campaign
- `email_number`: 1, 2, 3, etc.
- `subject`, `preview_text`, `body`, `cta`
- `mindset_target`: Which segment this email targets
- `estimated_effectiveness`: Optional performance prediction

---

## Example Data Flow

### Step 1: Create Campaign Record
```sql
INSERT INTO campaigns (
    product_description,
    target_audience_urls,
    status
) VALUES (
    'AI-powered email automation',
    '["https://linkedin.com/in/user1", "https://linkedin.com/in/user2"]'::JSONB,
    'pending'
)
RETURNING id;
```

### Step 2: Update with Subconscious Results
```sql
UPDATE campaigns SET
    status = 'processing',
    subconscious_experiment_id = 'exp_abc123',
    subconscious_response = '{ ... }'::JSONB,
    mindset_segments = '{
        "segments": [
            {"name": "Data-Driven Advocates", "percentage": 40},
            {"name": "Story Believers", "percentage": 60}
        ]
    }'::JSONB,
    winning_insight_summary = 'Your audience responds 73% better to...'
WHERE id = 'campaign_id';
```

### Step 3: Complete with Generated Campaign
```sql
UPDATE campaigns SET
    status = 'completed',
    final_llm_prompt = 'Based on behavioral analysis...',
    generated_campaign = '[
        {
            "email_number": 1,
            "subject": "Subject line",
            "body": "Email body",
            "cta": "Click here"
        }
    ]'::JSONB,
    generation_duration_seconds = 45,
    api_costs = '{"subconscious": 0, "openai": 0.05, "total": 0.05}'::JSONB
WHERE id = 'campaign_id';
```

---

## Helpful Views

### `recent_campaigns`
Quick overview of recent successful campaigns:
```sql
SELECT * FROM recent_campaigns LIMIT 10;
```

### `campaign_summary`
Summary statistics for all campaigns:
```sql
SELECT * FROM campaign_summary WHERE status = 'completed';
```

---

## Query Examples

### Get a campaign with all details
```sql
SELECT 
    id,
    product_description,
    winning_insight_summary,
    generated_campaign,
    api_costs
FROM campaigns
WHERE id = 'your_campaign_id';
```

### Get all campaigns for a specific product
```sql
SELECT * FROM campaigns
WHERE product_description ILIKE '%marketing%'
ORDER BY created_at DESC;
```

### Get campaigns with their email count
```sql
SELECT 
    id,
    product_description,
    jsonb_array_length(generated_campaign) as email_count,
    status
FROM campaigns
WHERE status = 'completed';
```

### Get total API costs
```sql
SELECT 
    SUM((api_costs->>'subconscious')::decimal) as total_subconscious_cost,
    SUM((api_costs->>'openai')::decimal) as total_openai_cost,
    SUM((api_costs->>'total')::decimal) as total_cost
FROM campaigns
WHERE status = 'completed';
```

### Extract specific email from campaign
```sql
SELECT 
    id,
    product_description,
    generated_campaign->0->>'subject' as first_email_subject,
    generated_campaign->1->>'subject' as second_email_subject
FROM campaigns
WHERE id = 'your_campaign_id';
```

---

## Migration from Old Schema

If you already have data in the old schema:

```sql
-- Add new columns (Supabase will handle this)
ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'completed';
ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS mindset_segments JSONB;
ALTER TABLE campaigns ADD COLUMN IF NOT EXISTS subconscious_experiment_id VARCHAR(255);
-- ... etc

-- Rename old column to new naming convention
ALTER TABLE campaigns RENAME COLUMN full_subconscious_results TO subconscious_response;
```

---

## Testing

Use the sample data function:
```sql
SELECT insert_sample_campaign();
```

Then verify:
```sql
SELECT * FROM recent_campaigns;
```

---

## Next Steps for Phase 2

When implementing the real `/generate-campaign` endpoint:

1. **Create record** with `status='pending'`
2. **Call Subconscious API** → Update with response & `status='processing'`
3. **Parse insights** → Extract mindset segments, winning insight
4. **Build OpenAI prompt** → Store in `final_llm_prompt`
5. **Call OpenAI** → Get campaign emails
6. **Update record** → Set `status='completed'`, add costs, duration
7. **Return to client** → Send back the simplified response

The database now captures the ENTIRE workflow for auditing, debugging, and analytics!
