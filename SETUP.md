# Hermes - The Reasoning-First Campaign Generator

AI co-pilot for marketers that transforms email campaign creation from guesswork into a science.

## Phase 1 Setup Complete! ✅

This project now has:
- ✅ FastAPI backend with mock endpoint
- ✅ API contract defined (mock_response.json)
- ✅ Vercel deployment configuration
- ✅ Supabase database schema
- ✅ Project structure and dependencies

## Quick Start

### 1. Set up your virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your API keys:

```powershell
copy .env.example .env
```

Then edit `.env` with your actual credentials:
- Supabase URL and Key
- OpenAI API Key
- Subconscious API Key

### 4. Set up Supabase Database

1. Create a new project in Supabase
2. Go to the SQL Editor
3. Copy and paste the contents of `setup_database.sql`
4. Run the query to create the `campaigns` table

### 5. Run locally

```powershell
python main.py
```

The API will be available at `http://localhost:8000`

### 6. Test the mock endpoint

```powershell
# Health check
curl http://localhost:8000/

# Test mock endpoint
curl -X POST http://localhost:8000/generate-campaign-mock -H "Content-Type: application/json" -d '{\"product_description\":\"My amazing product\",\"target_audience_urls\":[\"https://linkedin.com/in/example\"]}'
```

### 7. Deploy to Vercel

```powershell
# Install Vercel CLI (if not already installed)
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

## Project Structure

```
hermes/
├── main.py                  # FastAPI application with mock endpoint
├── mock_response.json       # Perfect example API response
├── requirements.txt         # Python dependencies
├── vercel.json             # Vercel deployment config
├── setup_database.sql      # Supabase table creation
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## API Endpoints

### GET /
Health check endpoint

### POST /generate-campaign-mock
Mock endpoint that returns perfect hardcoded data. Use this for frontend development!

**Request Body:**
```json
{
  "product_description": "Your product description",
  "target_audience_urls": ["https://linkedin.com/in/example"],
  "messaging_angles": ["optional", "angles"]
}
```

### POST /generate-campaign
Real endpoint (Coming in Phase 2) - Will integrate with Subconscious API, OpenAI, and Supabase

## Next Steps - Phase 2

**Track A: Front-End Champion (Lovable)**
1. Build the input screen form
2. Connect to the `/generate-campaign-mock` endpoint
3. Build the results screen with the three-part narrative
4. Implement loading state

**Track B: Back-End Champion (Python)**
1. Integrate Subconscious API with polling
2. Build the reasoning layer (summarize_results, build_openai_prompt)
3. Integrate OpenAI API
4. Integrate Supabase for data persistence
5. Implement the real `/generate-campaign` endpoint

## Tech Stack

- **Backend**: Python + FastAPI
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Vercel
- **Frontend**: Lovable
- **AI Services**: Subconscious API + OpenAI GPT-4

---

Built for the hackathon with ❤️
