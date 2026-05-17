import os
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://wash-rfp-frontend.vercel.app", 
    "https://wash-rfp.vercel.app", 
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
    """
    High-speed endpoint designed to extract core tender data 
    well within server timeout thresholds.
    """
    try:
        pdf_content = await file.read()

        # Streamlined prompt optimized for speed and low token generation time
        # Now expanded to capture comprehensive WASH program parameters
        prompt = """
        Analyze this document and extract the core metadata.
        Return a valid JSON object strictly matching this schema:
        {
          "project_metadata": {
            "title": "Project name or title",
            "donor": "Funding agency or donor name",
            "reference_number": "Tender reference code",
            "closing_date": "Submission deadline date",
            "submission_email": "Contact or submission email address",
            "contract_value": "Total budget, grant ceiling, or contract amount (e.g., $10,000,000)",
            "project_duration": "Duration of the project (e.g., 24 months, 5 years)",
            "eligibility_criteria": "Brief summary of who is eligible to apply",
            "target_demographics": "The specific populations, communities, or regions targeted",
            "key_deliverables": "A short summary of the main deliverables, outcomes, or outputs"
          }
        }
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
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
        print(f"Extraction Error: {e}")
        raise HTTPException(status_code=500, detail="Document processing failed")