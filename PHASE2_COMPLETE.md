# Phase 2 Implementation Guide

## Overview

Phase 2 is now **COMPLETE** with a fully functional `/generate-campaign` endpoint that:

1. ✅ Gets behavioral insights (currently using mock Subconscious data)
2. ✅ Extracts winning insights and builds intelligent prompts
3. ✅ Calls OpenAI GPT-4 to generate personalized email campaigns
4. ✅ Saves complete workflow to Supabase database
5. ✅ Returns structured campaign response

## What's Been Built

### New Modules

#### 1. `mock_subconscious.py`
- Generates realistic Subconscious API responses based on real data structure
- Includes mindset segmentation, AMCE results, WTP data
- Use this until you get real Subconscious API access
- Function: `generate_mock_subconscious_response()`

#### 2. `reasoning_layer.py`
- Extracts winning insights from behavioral data
- Builds detailed OpenAI prompts with segment-specific recommendations
- Parses OpenAI JSON responses
- Functions: `summarize_results()`, `build_openai_prompt()`, `extract_emails_from_openai_response()`

#### 3. `openai_client.py`
- Wrapper for OpenAI GPT-4 API calls
- Handles token counting and cost calculation
- Returns structured campaign JSON
- Class: `OpenAIClient` with `generate_campaign()` method

#### 4. `supabase_client.py`
- Complete database workflow management
- Creates campaigns, tracks status, saves all API data
- Stores emails and provides retrieval functions
- Class: `SupabaseClient` + helper function `save_complete_campaign()`

#### 5. Updated `main.py`
- Fully implemented `/generate-campaign` endpoint
- Complete orchestration of all workflow steps
- Graceful error handling and status codes
- Works even if Supabase is not configured (just won't save to DB)

---

## Setup Instructions

### Step 1: Install Dependencies

If you haven't already:

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install/update packages
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```powershell
cp .env.example .env
```

Edit `.env`:

```bash
# Required for real campaign generation
OPENAI_API_KEY=sk-your-openai-key-here

# Optional - if not set, won't save to database but endpoint will still work
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here

# Not needed yet (using mock data)
SUBCONSCIOUS_API_KEY=your-key-when-you-get-it
```

### Step 3: Set Up Supabase (Optional but Recommended)

1. Create account at https://supabase.com
2. Create new project
3. Go to SQL Editor and run `setup_database.sql`
4. Get your URL and anon key from Project Settings > API
5. Add to `.env` file

### Step 4: Get OpenAI API Key (Required)

1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env` as `OPENAI_API_KEY`
4. Add billing method (GPT-4 costs ~$0.01-0.05 per campaign)

---

## Testing the New Endpoint

### Test Individual Modules

Each module has a test function at the bottom:

```powershell
# Test mock Subconscious generator
python mock_subconscious.py

# Test reasoning layer
python reasoning_layer.py

# Test OpenAI integration (requires OPENAI_API_KEY)
python openai_client.py

# Test Supabase integration (requires SUPABASE_URL and SUPABASE_KEY)
python supabase_client.py
```

### Test the Full API

1. **Start the server:**

```powershell
python main.py
```

2. **Test with the test script:**

Create a new file `test_real_endpoint.py`:

```python
import requests
import json

# Test data
payload = {
    "product_description": "AI-powered email marketing automation for B2B SaaS companies",
    "target_audience_urls": [
        "https://linkedin.com/in/marketing-director",
        "https://linkedin.com/in/growth-manager"
    ],
    "messaging_angles": ["Time Savings", "Revenue Growth", "Team Efficiency"]
}

# Call real endpoint
print("Calling /generate-campaign endpoint...")
print("This will take 10-30 seconds (calling OpenAI GPT-4)...\n")

response = requests.post("http://localhost:8000/generate-campaign", json=payload)

if response.status_code == 200:
    result = response.json()
    print("✅ SUCCESS!\n")
    print(f"Campaign ID: {result['id']}")
    print(f"Winning Insight: {result['winning_insight_summary'][:100]}...")
    print(f"\nGenerated {len(result['generated_campaign'])} emails:")
    
    for email in result['generated_campaign']:
        print(f"\n--- Email {email['email_number']} ---")
        print(f"Subject: {email['subject']}")
        print(f"CTA: {email['cta']}")
        print(f"Body preview: {email['body'][:150]}...")
else:
    print(f"❌ Error {response.status_code}")
    print(response.json())
```

Run it:

```powershell
python test_real_endpoint.py
```

---

## What Happens When You Call `/generate-campaign`

1. **Mock Subconscious Analysis** (instant)
   - Generates realistic behavioral insights
   - 3 mindset segments with characteristics
   - AMCE data showing what messaging works
   - Winning insight summary

2. **Reasoning Layer** (instant)
   - Extracts top insights
   - Identifies largest audience segments
   - Builds detailed GPT-4 prompt with behavioral data

3. **OpenAI Generation** (10-30 seconds)
   - Calls GPT-4-turbo with behavioral prompt
   - Generates 3 personalized emails
   - Returns structured JSON
   - Costs: ~$0.01-0.05 per campaign

4. **Database Save** (instant, if configured)
   - Creates campaign record
   - Saves all API requests/responses
   - Stores generated emails
   - Updates status to "completed"

5. **Response**
   - Returns complete campaign
   - 3 emails with subjects, bodies, CTAs
   - Winning insight summary
   - Full behavioral data

---

## Cost Estimates

- **OpenAI GPT-4 Turbo**: ~$0.01-0.05 per 3-email campaign
- **Supabase**: Free tier covers ~50,000 rows (hundreds of campaigns)
- **Subconscious API**: Pricing TBD when you get access

---

## Next Steps

### Now: Test Without Subconscious API

Since you don't have Subconscious API access yet:

1. ✅ Set up OpenAI API key (required)
2. ✅ Set up Supabase (optional)
3. ✅ Test `/generate-campaign` endpoint with mock data
4. ✅ Build frontend to consume this API
5. ✅ Demo the full workflow to stakeholders

### Later: Integrate Real Subconscious API

When you get API access:

1. Create `real_subconscious.py` module
2. Implement actual API calls following their documentation
3. Update `main.py` to use real API instead of mock:

```python
# In main.py, replace this:
subconscious_response = generate_mock_subconscious_response(...)

# With this:
from real_subconscious import call_subconscious_api
subconscious_response = await call_subconscious_api(...)
```

4. Test and deploy!

---

## Deployment

### Deploy to Vercel

The endpoint is already configured for Vercel:

```powershell
vercel --prod
```

**Important**: Make sure to add environment variables in Vercel dashboard:
- Settings > Environment Variables
- Add `OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`

---

## Troubleshooting

### "Configuration error: OpenAI API key not found"

- Add `OPENAI_API_KEY` to your `.env` file
- Make sure `.env` is in the same directory as `main.py`
- Restart the server after adding the key

### "External API error: OpenAI API call failed"

- Check your OpenAI API key is valid
- Ensure you have billing set up on OpenAI account
- Check you have sufficient credits

### "Database error: ..."

- Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Run `setup_database.sql` in Supabase SQL Editor
- Check Supabase project is not paused

### Mock endpoint works but real endpoint doesn't

- The real endpoint requires `OPENAI_API_KEY`
- The mock endpoint (`/generate-campaign-mock`) has no dependencies
- Use mock endpoint for frontend development if needed

---

## Architecture Summary

```
User Request
    ↓
FastAPI Endpoint (/generate-campaign)
    ↓
Mock Subconscious (mock_subconscious.py)
    ↓
Reasoning Layer (reasoning_layer.py)
    ↓
OpenAI GPT-4 (openai_client.py)
    ↓
Supabase Database (supabase_client.py)
    ↓
Response to User
```

---

## File Structure

```
hermes/
├── main.py                    # FastAPI app with both endpoints
├── mock_subconscious.py       # Mock behavioral insights
├── reasoning_layer.py         # Extract insights, build prompts
├── openai_client.py          # OpenAI API wrapper
├── supabase_client.py        # Database operations
├── mock_response.json        # Mock data for /generate-campaign-mock
├── setup_database.sql        # Supabase schema
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── .env                      # Your actual credentials (gitignored)
└── vercel.json               # Deployment config
```

---

## You're Ready! 🚀

Phase 2 is complete. You now have:

- ✅ Fully functional `/generate-campaign` endpoint
- ✅ Mock Subconscious data (no API access needed yet)
- ✅ Real OpenAI GPT-4 integration
- ✅ Complete database workflow
- ✅ Production-ready code structure

**To test right now:**
1. Add your `OPENAI_API_KEY` to `.env`
2. Run `python main.py`
3. Call `/generate-campaign` endpoint
4. Get a real AI-generated campaign in 10-30 seconds!
