import os
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Added this
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# --- Configuration for cross-origin requests ---
origins = [
    "http://localhost:5173", 
    "https://wash-rfp-frontend.vercel.app", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/parse-rfp")
async def parse_rfp(file: UploadFile = File(...)):
    try:
        pdf_content = await file.read()

        # Prompt template
        prompt = """
        You are an expert bid manager. Analyze this tender document and extract the critical project data.
        You MUST return a valid JSON object that STRICTLY follows this exact structure and keys. 
        If a detail is not found in the document, write "Not specified".

        {
          "project_metadata": {
            "title": "Full name of the project",
            "donor": "Funding agency",
            "reference_number": "Tender or RFP code",
            "closing_date": "Submission deadline",
            "submission_email": "Where to send the bid"
          },
          "technical_scope": {
            "summary": "Brief 2-sentence overview",
            "locations": ["List of regions, districts, or provinces"],
            "key_activities": ["List of physical works or services, e.g., boreholes, latrines"],
            "environmental_goals": "Any climate, greening, or sustainability requirements"
          },
          "financial_and_contractual": {
            "budget_estimate": "Total value if mentioned",
            "overhead_cap": "Limits on indirect costs or admin fees",
            "payment_schedule": [
              {"milestone": "Name of deliverable", "percentage": "% of payment"}
            ],
            "duration_or_phases": "Project timeline or distinct phases"
          },
          "evaluation_rubric": {
            "technical_weight": "Percentage weight for technical score",
            "financial_weight": "Percentage weight for financial score",
            "key_criteria": ["Main points they will grade the proposal on"]
          },
          "compliance_and_safeguarding": {
            "mandatory_certifications_or_plans": ["e.g., ESMP, Health and Safety Plan"],
            "safeguarding_rules": ["e.g., gender equality, child protection rules"]
          }
        }
        """

        # Call Gemini 1.5 Flash 
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                types.Part.from_bytes(data=pdf_content, mime_type="application/pdf"),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        extracted_data = json.loads(response.text)       
        return {"success": True, "data": extracted_data}

    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))