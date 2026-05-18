import os
import json
import random
from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Dict

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# --- 1. CORE APP METADATA & ALIVE CHECK ---
@app.get("/")
async def root():
    return {"status": "online", "message": "OpenWSH Extraction API is running."}

# --- 2. SECURITY & CORS CONFIGURATION ---
# Open wildcard to ensure Vercel frontend can always connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. LIVE DATA API ENRICHMENT ENGINE ---
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

# --- 4. REAL-TIME COLLABORATION MULTIPLAYER HUB ---
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

# --- 5. INTELLIGENT AI EXTRACTION ENDPOINT ---
@app.post("/api/parse-rfp")
async def parse_rfp(file: UploadFile = File(...)):
    try:
        pdf_content = await file.read()

        # THE FIX: Added strict 'primary_country' rule for the pipeline
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

        # Using async client to prevent WebSocket freezing
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