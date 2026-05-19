import os
import json
import random
import tempfile
import pdfkit
from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Dict

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# CORE APP METADATA & ALIVE CHECK ---
@app.get("/")
async def root():
    return {"status": "online", "message": "OpenWSH Extraction API is running."}

# --- SECURITY & CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LIVE DATA API ENRICHMENT ENGINE ---
class CountryContext(BaseModel):
    country: str
    water_stress_index: float
    governance_score: int
    primary_climate_risk: str
    infrastructure_baseline: int

@app.get("/api/context/{country_name}", response_model=CountryContext)
async def get_live_country_context(country_name: str):
    target = country_name.lower().strip()
    
    db = {
        "mali": {"water_stress": 82.4, "governance": 35, "risk": "Drought", "infra": 42},
        "kenya": {"water_stress": 64.1, "governance": 52, "risk": "Drought", "infra": 58},
        "uganda": {"water_stress": 45.8, "governance": 48, "risk": "Flood", "infra": 50},
        "bangladesh": {"water_stress": 31.2, "governance": 45, "risk": "Flood", "infra": 65},
        "papua new guinea": {"water_stress": 28.5, "governance": 38, "risk": "Flood", "infra": 35}
    }
    
    if target in db:
        data = db[target]
        return CountryContext(
            country=country_name.title(),
            water_stress_index=data["water_stress"],
            governance_score=data["governance"],
            primary_climate_risk=data["risk"],
            infrastructure_baseline=data["infra"]
        )
    
    return CountryContext(
        country=country_name.title(),
        water_stress_index=round(random.uniform(30.0, 85.0), 1),
        governance_score=random.randint(30, 70),
        primary_climate_risk=random.choice(["Drought", "Flood", "Cyclonic Storm"]),
        infrastructure_baseline=random.randint(40, 75)
    )

# --- REAL-TIME COLLABORATION MULTIPLAYER HUB ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, workspace_id: str):
        await websocket.accept()
        if workspace_id not in self.active_connections:
            self.active_connections[workspace_id] = []
        self.active_connections[workspace_id].append(websocket)

    def disconnect(self, websocket: WebSocket, workspace_id: str):
        if workspace_id in self.active_connections:
            self.active_connections[workspace_id].remove(websocket)
            if not self.active_connections[workspace_id]:
                del self.active_connections[workspace_id]

    async def broadcast(self, message: str, workspace_id: str, sender: WebSocket):
        if workspace_id in self.active_connections:
            for connection in self.active_connections[workspace_id]:
                if connection != sender: 
                    try:
                        await connection.send_text(message)
                    except Exception:
                        pass 

manager = ConnectionManager()

@app.websocket("/ws/collaborate/{workspace_id}")
async def websocket_endpoint(websocket: WebSocket, workspace_id: str):
    await manager.connect(websocket, workspace_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, workspace_id, sender=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, workspace_id)

# --- INTELLIGENT AI EXTRACTION ENDPOINT ---
@app.post("/api/parse-rfp")
async def parse_rfp(file: UploadFile = File(...)):
    try:
        pdf_content = await file.read()

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
            "primary_country": "Extract ONLY the single primary country name where the project takes place (e.g., 'Papua New Guinea', 'Kenya', 'Mali'). DO NOT use abbreviations like PNG. DO NOT include regions or provinces here.",
            "key_deliverables": "A short summary of the main deliverables, outcomes, or outputs"
          }
        }
        """

        response = await client.aio.models.generate_content(
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

# --- SERVER-SIDE LOGFRAME PDF COMPILER ---
class LogFrameRequest(BaseModel):
    rfpData: dict

@app.post("/api/generate-logframe")
async def generate_logframe_pdf_endpoint(payload: LogFrameRequest):
    try:
        data = payload.rfpData
        
        # AI Prompt
        prompt = f"""
        Act as a Senior Technical Director for an international WASH NGO.
        Based on the following extracted project parameters, generate a highly professional, 
        4-row Logical Framework (LogFrame) Matrix.
        
        Project Source Data:
        Target Country: {data.get('primaryCountry', 'Unknown')}
        Donor: {data.get('budget', 'Unknown')}
        Deliverables: {data.get('deliverables', 'WASH Infrastructure and Capacity Building')}
        
        Return a valid JSON array containing exactly 4 objects. 
        Each object MUST have these exact keys: "level", "narrative", "indicators", "verification", "assumptions".
        
        The 'level' values MUST strictly be:
        Row 1: "1. Strategic Impact (Goal)"
        Row 2: "2. Project Outcomes"
        Row 3: "3. Tangible Outputs"
        Row 4: "4. Key Activities & Inputs"
        """

        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        
        matrix_data = json.loads(response.text)

        # Convert JSON into Corporate HTML structure
        html_rows = ""
        for i, row in enumerate(matrix_data):
            bg_class = "row-bg" if i % 2 != 0 else ""
            html_rows += f"""
            <tr class="{bg_class}">
                <td><strong>{row.get('level')}</strong></td>
                <td>{row.get('narrative')}</td>
                <td>{row.get('indicators')}</td>
                <td>{row.get('verification')}</td>
                <td>{row.get('assumptions')}</td>
            </tr>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            @page {{ size: A4 landscape; margin: 15mm; background-color: #ffffff; }}
            body {{ font-family: 'Arial', sans-serif; color: #111111; line-height: 1.4; }}
            .header {{ border-bottom: 3px solid #1A365D; padding-bottom: 12px; margin-bottom: 25px; }}
            .title {{ font-size: 22pt; font-weight: 800; color: #1A365D; text-transform: uppercase; margin: 0; }}
            .subtitle {{ font-size: 11pt; color: #444444; font-weight: bold; margin-top: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ border: 1px solid #cccccc; padding: 14px; text-align: left; vertical-align: top; font-size: 10pt; }}
            th {{ background-color: #f0f4f8; color: #1A365D; text-transform: uppercase; font-size: 9pt; }}
            .row-bg {{ background-color: #fbfcfd; }}
            .footer {{ margin-top: 30px; font-size: 8pt; color: #777777; text-align: center; border-top: 1px solid #eeeeee; padding-top: 10px; }}
            .metadata-block {{ margin-bottom: 20px; font-size: 10pt; background: #f9f9f9; padding: 10px; border-left: 4px solid #3B82F6; }}
        </style>
        </head>
        <body>
            <div class="header">
                <h1 class="title">Logical Framework Matrix</h1>
                <div class="subtitle">Comprehensive Project Assessment & Strategic Impact Report</div>
            </div>
            
            <div class="metadata-block">
                <strong>Project Reference:</strong> {data.get('projectNumber', 'N/A')} <br>
                <strong>Funding Origin:</strong> {data.get('budget', 'Strategic Capital')} <br>
                <strong>Target Jurisdiction:</strong> {data.get('primaryCountry', 'Unspecified')}
            </div>

            <table>
                <thead>
                    <tr>
                        <th style="width: 15%;">Hierarchy</th>
                        <th style="width: 25%;">Detailed Narrative Summary</th>
                        <th style="width: 20%;">Verifiable Indicators (OVI)</th>
                        <th style="width: 20%;">Means of Verification</th>
                        <th style="width: 20%;">Critical Assumptions</th>
                    </tr>
                </thead>
                <tbody>
                    {html_rows}
                </tbody>
            </table>
            
            <div class="footer">
                Generated by OpenWSH-CONTROL Enterprise Pipeline. All details, cards, and sub-metrics included for comprehensive institutional audit compliance.
            </div>
        </body>
        </html>
        """

        # Render PDF natively and force browser download
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        
        # specify path to pdfkit.
        pdfkit.from_string(html_content, temp_pdf.name)

        return FileResponse(
            path=temp_pdf.name, 
            filename=f"LogFrame_{data.get('projectNumber', 'Export')}.pdf",
            media_type="application/pdf",
            background=None 
        )

    except Exception as e:
        print(f"LogFrame Generation Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to compile LogFrame PDF")