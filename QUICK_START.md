# Quick Start - Get Your First AI Campaign in 5 Minutes

## ⚡ Fastest Path to a Working Demo

### Step 1: Get an OpenAI API Key (2 minutes)

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-...`)

### Step 2: Configure Your Environment (1 minute)

1. Open `.env.example` in the hermes folder
2. Copy it to a new file named `.env` (remove the `.example`)
3. Replace the OpenAI key line:

```bash
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
```

Save and close.

### Step 3: Install Dependencies (1 minute)

Open PowerShell in the hermes folder:

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install packages (if not already done)
pip install -r requirements.txt
```

### Step 4: Start the Server (30 seconds)

```powershell
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Generate Your First Campaign (30 seconds)

Open a NEW PowerShell window and run:

```powershell
python test_real_endpoint.py
```

**What happens:**
- ✅ Calls your local server
- ✅ Generates mock behavioral insights (instant)
- ✅ Calls OpenAI GPT-4 to write emails (10-30 seconds)
- ✅ Returns 3 personalized, professional emails
- ✅ Shows you the winning insights and mindset breakdown

---

## 🎉 That's It!

You now have a working AI campaign generator!

### What You Just Built:

✅ **Real AI-powered campaign generation**  
✅ **Behavioral science-based personalization**  
✅ **3 professionally written emails**  
✅ **Complete with subjects, bodies, and CTAs**  

### Cost: ~$0.01-0.05 per campaign

---

## Next Steps

### Want to Save Campaigns to Database?

See `PHASE2_COMPLETE.md` section "Set Up Supabase"

### Want to Deploy to Production?

```powershell
vercel --prod
```

Make sure to add `OPENAI_API_KEY` in Vercel dashboard under Settings > Environment Variables

### Want to Integrate with Frontend?

Your API is ready at:
- **Local:** `http://localhost:8000/generate-campaign`
- **Production:** `https://your-deployment.vercel.app/generate-campaign`

Send POST request with:
```json
{
  "product_description": "Your product description",
  "target_audience_urls": ["https://linkedin.com/in/person1"],
  "messaging_angles": ["Angle 1", "Angle 2"]
}
```

---

## Troubleshooting

### "Configuration error: OpenAI API key not found"
- Make sure `.env` file exists (not `.env.example`)
- Check the key starts with `sk-proj-`
- Restart the server after adding the key

### "Cannot connect to http://localhost:8000"
- Make sure the server is running: `python main.py`
- Check for error messages in the server terminal

### "OpenAI API call failed"
- Verify your API key is valid
- Check you have billing set up on OpenAI
- Ensure you have credits available

---

## What's Next?

Read the full guides:
- **Complete Setup:** `PHASE2_COMPLETE.md`
- **Architecture & Details:** `PHASE2_SUMMARY.md`
- **Database Schema:** `DATABASE_GUIDE.md`

---

**You're all set! Start generating campaigns! 🚀**
