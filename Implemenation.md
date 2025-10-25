Project Vision: The Reasoning-First Campaign Generator
We are building an AI co-pilot for marketers that transforms email campaign creation from guesswork into a science. The tool first uses the Subconscious API to run behavioral simulations, discovering the most persuasive messaging angles for a specific audience. It then transparently documents this reasoning before using a Generative AI to write a high-converting email nurture campaign based on those proven insights.
Core Differentiator: We don't just provide the output; we show the user the entire chain of reasoning—from audience analysis to creative brief to final copy—making the AI's decisions transparent, trustworthy, and valuable.

1. Tech Stack Selection
Component
Technology
Why It's the Right Choice for this Hackathon
Front-End
Lovable
Speed & Polish: Enables rapid development of a professional, component-based UI without deep front-end coding, allowing the team to focus on logic and presentation.
Back-End
Python with FastAPI
Simplicity & Performance: FastAPI is a modern, high-performance framework that is easy to learn. Its automatic data validation and documentation are perfect for quickly building a robust API bridge.
Database
Supabase
Zero-Friction Setup: Provides a full-featured Postgres database and an instant API in minutes. The generous free tier and simple Python client library make it the fastest way to get a database running.
Behavioral Sim
Subconscious API
Core Insight Engine: The central component for fulfilling the hackathon track. It provides the unique, data-backed insights that differentiate this tool from a simple text generator.
Text Generation
OpenAI API (GPT-4)
State-of-the-Art Copy: Industry standard for high-quality text generation. Its ability to follow complex instructions is essential for translating the Subconscious insights into a coherent campaign.
Deployment
Vercel
Seamless CI/CD: Offers a simple, git-based workflow for deploying both the front-end and the Python serverless backend. Perfect for rapid, iterative development during a hackathon.


2. System Architecture & Data Flow
User Input: The marketer provides product details and audience URLs (Linkedin) in the Lovable UI
API Request: Lovable sends a POST request to the FastAPI Backend on Vercel.
Insight Generation: The backend calls the Subconscious API and polls for the simulation results.
Reasoning Layer: The backend processes the results to create a summary and a detailed prompt.
Content Generation: The backend sends the detailed prompt to the OpenAI API.
Data Persistence: The entire "story" (inputs, insights, prompt, and final emails) is saved as a single record in the Supabase Database.
API Response: The backend returns a structured JSON object with the full story to the Lovable UI.
Display: The UI renders the reasoning and the final campaign in a clear, narrative format.

3. Database Schema
Table: campaigns (in Supabase)
Column Name
Data Type
Description
id
uuid (primary key)
Unique identifier for the campaign record.
created_at
timestamp
Timestamp of creation.
product_description
text
User's initial product description.
target_audience_urls
jsonb
The list of LinkedIn URLs provided by the user.
winning_insight_summary
text
Human-readable summary of the key finding from Subconscious.
full_subconscious_results
jsonb
The complete, raw JSON output from the Subconscious API for auditability.
final_llm_prompt
text
The exact prompt sent to the OpenAI API, bridging insight and generation.
generated_campaign
jsonb
The final set of generated emails, stored as a JSON array of objects.


4. Detailed Implementation Plan
Phase 1: Setup & Foundations (Est. 1.5 Hours)
1. Account Creation: Create accounts for Lovable, Supabase, OpenAI, and Vercel. Redeem the AntlerNYC code on Lovable.
2. Project Initialization:
Initialize a git repository.
Set up a Python virtual environment (python -m venv venv).
Install all Python dependencies: pip install "fastapi[all]" python-dotenv openai supabase requests.
Create a .env file and populate it with all necessary API keys and Supabase credentials.
3. Database Setup:
In Supabase, create a new project.
Use the SQL Editor to create the campaigns table using the schema defined above.
Phase 2: Backend Core Logic - The Engine (Est. 3 Hours)
Goal: Build a single, powerful API endpoint that orchestrates the entire workflow.
1. FastAPI Boilerplate: Set up a main.py file with a basic FastAPI app and a health check endpoint (/) to confirm it's running.
2. Supabase Client: Initialize the Supabase client in your Python code to be ready for use.
3. Build the 
Define the Pydantic models for the request body and response body to ensure data integrity.
Subconscious Integration: Write a function to call the Subconscious /experiments endpoint. This will likely be asynchronous, so implement a polling mechanism (e.g., check the results endpoint every 30 seconds) to wait for completion.
Insight Summarizer: Create a critical helper function summarize_results(subconscious_json) that parses the raw results and returns the human-readable winning_insight_summary string.
Prompt Engineering: Create a function build_openai_prompt(summary, product_info) that constructs the detailed final_llm_prompt.
OpenAI Integration: Write the function to call the OpenAI API with the generated prompt.
Putting It All Together: In the main endpoint logic, call these functions in sequence.
Save to Database: After a successful generation, save the complete record to the campaigns table in Supabase.
Return the Story: Send back the structured JSON response containing the summary, prompt, and final emails.
Phase 3: Front-End UI with Lovable (Est. 3 Hours)
Goal: Create a polished, intuitive user experience that tells the story of the campaign's creation.
1. Screen 1: Input Form:
Design a clean and simple form with text areas for "Product Description," "Target Audience (LinkedIn URLs)," and a few fields for "Messaging Angles to Test."
Add a prominent "Generate My Campaign" button.
2. Screen 2: Loading State:
Create a dedicated loading view that is shown after the user clicks "Generate."
Display messages like "Analyzing your audience...", "Running behavioral simulations...", "Writing your copy..." to manage user expectations during the API wait time.
3. Screen 3: The Results Narrative:
Design the three-part "story" layout.
Part 1: The Core Insight: Use a large, visually distinct component (like a blockquote) to display the insight_summary.
Part 2: The Creative Brief: Use a pre or code block component to display the final_llm_prompt, making the AI's instructions transparent.
Part 3: The Final Campaign: Use tabs or an accordion to neatly display each email from the generated_campaign object. Each email should have its own "Copy to Clipboard" button.
Phase 4: Integration, Deployment & Polish (Est. 2 Hours)
1. Deploy Backend: Deploy the FastAPI application to Vercel. This will give you a live API URL.
2. Connect Front-End: In Lovable, configure the "Generate" button's action to make a POST request to your live Vercel backend URL.
3. Data Mapping: Connect the fields from the API's JSON response to the correct components on your Lovable results screen.
4. Final Demo Prep:
Record the Loom Video: Create a crisp, sub-2-minute demo video showcasing the end-to-end flow.
Complete the Product Brief: Fill out the "Antler Product Brief Template" using the context from this plan.
Practice the Live Demo: Rehearse a 3-minute presentation that tells a compelling story, focusing on the problem, your unique "reasoning-first" solution, and the value it provides.

Suggested Team Roles & Collaboration
Front-End & UX Champion (Lovable):
Owns the entire Lovable application.
Defines the user flow and designs all three screens.
Works with the backend champion to define the exact JSON structure needed for the results page.
Back-End & API Master (Python):
Owns the FastAPI application and all API integrations (Subconscious, OpenAI, Supabase).
Implements the core logic, including the crucial "Insight Summarizer."
Deploys the backend to Vercel and provides the API endpoint and data contract to the front-end champion

Analysis & Recommendations: How to Build Faster with a Higher Success Rate
The current plan is solid, but it has one major point of failure for a time-constrained hackathon: dependency on live, asynchronous APIs. Waiting 10 minutes for the Subconscious API to return a result during a development loop will destroy your momentum.
Here is a revised strategy that dramatically increases your speed and chances of success by de-risking the project.
The "Parallel Paths" Strategy: Mock Your Backend First
This is the single most important change you can make. Do not build the front-end and back-end sequentially. Build them in parallel by creating a fake (mocked) version of your backend API first.
What to do:
Define the Final JSON Contract: Immediately agree on the exact structure of the JSON your backend will send to the front-end. This is the "API contract" from the previous plan (containing insight_summary, creative_brief_prompt, generated_emails).
Create a Static JSON File: Create a file (e.g., mock_response.json) and fill it with perfect, hardcoded example data. This is what a successful API call will look like.
Deploy a "Dumb" Mock API: In your FastAPI backend, create a temporary new endpoint like /generate-campaign-mock. This endpoint should do nothing but instantly read and return the contents of mock_response.json. Deploy this immediately.
Why this is a game-changer:
Unblocks Your Front-End Developer: The Lovable champion can start building the entire results page immediately against the /generate-campaign-mock endpoint. They don't have to wait for the real logic to be finished.
Enables Parallel Work: While the front-end is being built, the backend champion can work on the complex "real" endpoint (/generate-campaign), wrestling with the Subconscious and OpenAI integrations without blocking anyone.
Guarantees a Working Demo: If, by the end of the hackathon, the Subconscious API is slow or you can't get the integration working perfectly, you still have a 100% functional demo. You can present the mock-powered UI and explain that it's connected to a live data source that is currently in progress. This is a massive safety net.

Optimized Hackathon Build Plan
This revised plan incorporates the parallel strategy.
Phase 1: Foundations & The Mock API (Est. 1 Hour)
1. Setup: All accounts (Vercel, Supabase, etc.) and project initialization (git, venv).
2. Define the API Contract: Create the mock_response.json file with perfect, hardcoded data for the results screen.
3. Deploy the Mock Backend:
Create the FastAPI app.
Implement the /generate-campaign-mock endpoint that just returns the mock_response.json.
Deploy this simple backend to Vercel immediately to get a live URL.
Phase 2: Parallel Development Sprints (Est. 4 Hours)
Track A: The Front-End Champion (Working with the Mock API)
1. Build the Input Screen: Create the form in Lovable.
2. Connect to Mock API: Wire the "Generate" button to call the live /generate-campaign-mock endpoint on Vercel.
3. Build the Results Screen: Build the beautiful, three-part narrative results screen, populating it with the data from the mock response.
4. Build the Loading State: Implement the intermediate loading screen.
Track B: The Back-End Champion (Building the Real API)
1. Integrate Subconscious API: Write the code to call and poll the Subconscious API. This is the hardest part. Focus on getting a valid response.
2. Build the Reasoning Layer: Write the summarize_results and build_openai_prompt functions.
3. Integrate OpenAI API: Write the code to call the generative model.
4. Integrate Supabase: Write the code to save the final, successful result to the database.
5. Implement the  Combine all the pieces into the final, "real" API endpoint.
Phase 3: Integration & Demo Prep (Est. 2-3 Hours)
1. Connect to the Real API: Once the "real" backend is deployed, the front-end champion switches the API call in Lovable from /generate-campaign-mock to /generate-campaign.
2. End-to-End Testing & Debugging: Test the full, live flow. Since the front-end was built against a valid contract, this should primarily involve fixing minor data format issues.
3. Pre-populate for the Demo: Run your generator once with a perfect input to get a great result. Save this result's id from your Supabase table. Create a "secret" demo mode in your app that can load this result directly from the DB to ensure your live presentation is flawless.
4. Record Loom & Practice: Create your demo video and rehearse your 3-minute pitch, focusing on the story and the unique "reasoning" value proposition.
This optimized plan front-loads the creation of a working product, allows your team to work in parallel, and provides a crucial safety net. It maximizes your chances of having a polished, functional, and impressive demo by the deadline.

Here's the json
{
  "id": "campaign_123456789",
  "created_at": "2024-01-15T10:30:00Z",
  "product_description": "AI-powered email marketing automation tool for SaaS companies",
  "target_audience_urls": [
    "https://linkedin.com/in/saas-marketing-director",
    "https://linkedin.com/in/growth-marketing-manager"
  ],
  "winning_insight_summary": "Your audience responds 73% better to messaging that emphasizes 'time-saving automation' over 'advanced AI features'. They prioritize solutions that integrate seamlessly into their existing workflow without requiring extensive training.",
  "full_subconscious_results": {
    "experiment_id": "exp_abc123",
    "status": "completed",
    "tested_messages": [
      { "angle": "time_saving_simplicity", "score": 9.1 },
      { "angle": "advanced_ai_features", "score": 5.3 },
      { "angle": "cost_reduction", "score": 7.2 }
    ],
    "audience_insights": {
      "primary_pain_points": ["tool complexity", "implementation time", "team adoption"]
    }
  },
  "final_llm_prompt": "Based on behavioral analysis showing 73% higher engagement with 'time-saving automation' messaging, write a 3-email nurture sequence for SaaS marketing directors. Focus on workflow integration and simplicity over technical features. Each email should: 1) Address their pain point of tool complexity, 2) Emphasize quick implementation and social proof, 3) End with a soft CTA. Tone: Professional but approachable.",
  "generated_campaign": [
    {
      "email_number": 1,
      "subject": "Stop wrestling with complex marketing tools",
      "preview_text": "There's a simpler way to automate your email campaigns...",
      "body": "<p>Hi [First Name],</p><p>I know you're juggling multiple marketing tools, and each one seems to require a PhD to operate effectively. What if your email automation platform worked exactly how you think it should?</p><p>✅ Set up in under 10 minutes<br>✅ Integrates with your existing CRM<br>✅ No training required for your team</p><p>SoundToo, a SaaS company just like yours, saw 40% better email performance in their first week. Want to see how they did it?</p><p>Best,<br>[Your Name]</p>",
      "cta": "See the 10-minute setup demo"
    },
    {
      "email_number": 2,
      "subject": "The 10-minute setup that changed everything",
      "preview_text": "SoundToo's marketing director shares her story...",
      "body": "<p>Hi [First Name],</p><p>\"I was skeptical. Another email tool promising easy setup? Sure.\"</p><p>That's what Sarah, Marketing Director at SoundToo, told me last month. But here's what happened:</p><p>⏱️ Day 1: Complete setup in 8 minutes<br>📈 Week 1: 40% increase in email engagement<br>🎯 Month 1: 25% more qualified leads</p><p>No consultants. No training sessions. Just results. The secret? Our platform thinks like you do, not like an engineer.</p><p>Best,<br>[Your Name]</p>",
      "cta": "Read Sarah's full case study"
    },
    {
      "email_number": 3,
      "subject": "Last chance: Join the simple automation revolution",
      "preview_text": "This is your final invitation...",
      "body": "<p>Hi [First Name],</p><p>This is my final email. You have two choices:</p><p>1️⃣ Keep struggling with your current complex setup<br>2️⃣ Join the 500+ SaaS companies using simple, powerful automation</p><p>Over the past week, I've shown you how simple setup saves 300+ hours annually and shared real case studies. Now it's decision time.</p><p>Ready to stop wrestling with complex tools?</p><p>Best,<br>[Your Name]</p>",
      "cta": "Start your simple setup today"
    }
  ]
}
