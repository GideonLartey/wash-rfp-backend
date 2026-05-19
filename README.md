
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)]()
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)]()



## OpenWSH-CONTROL Core Backend API & AI Engine ⚙️

The asynchronous, high-speed Python backend engine powering the OpenWSH-CONTROL initiative. This system provides technical teams, directors, and field offices with automated RFP document parsing, localized water stress baseline enrichment, and an active multi-user WebSocket server for collaborative system modeling.

🔗 Live API Gateway: https://wash-ai.onrender.com (or your deployed API gateway URL)

🔗 Live Deployment(MAIN): https://wash-rfp-frontend.vercel.app

## 🏗️ Core Architecture & Services

The server is built with FastAPI to enable low-latency, asynchronous operations, managing heavy AI processes and state broadcasts smoothly using Python’s native asyncio loop.

## 🧠 Intelligent AI Parsing Node (POST /api/parse-rfp)

Ingests raw binary data streams from uploaded PDF tender documents.

Integrates directly with the Google Gemini 2.5 Flash model via the official Google GenAI SDK to run structural metadata extractions.

Executes precise prompt engineering templates to convert unstructured text into unified, type-safe JSON payloads. Missing or corrupt properties are normalized using secure default fallbacks to prevent pipeline failure.

## 🌐 Live Context Enrichment (GET /api/context/{country})

Serves as an index-optimized database query engine simulating real-time global monitoring indexes (like the WHO/UNICEF Joint Monitoring Programme).

Returns core environmental parameters for mapped countries, including baseline Water Stress, institutional Governance quality, and local Climate Risk.

Features an algorithmic fallback generator. When a region outside the database index is queried, the engine runs a localized statistical calculations loop to generate consistent, safe pseudo-random metrics, guaranteeing 100% demo uptime.

## 🔌 Multiplayer Collaboration Hub (WS /ws/collaborate/{workspace_id})

Built on a lightweight native WebSocket connection manager that keeps track of active, open communication channels grouped by dynamic room IDs.

Broadcasts user state adjustments across all socket endpoints in a room concurrently within microseconds, maintaining visual synchronization without database overhead.

## Automated PDF Generation Pipeline: 

Integrates pdfkit and wkhtmltopdf to transition from client-side print-dialog exports to native, server-side generated corporate PDF documentation.

## AI-Driven Matrix Intelligence: 

Added POST /api/generate-logframe endpoint. This utilizes Gemini 2.5 Flash to dynamically synthesize RFP metadata into a standard 4-tier Logical Framework (Goal, Outcome, Output, Activity), and complete with verifiable OVI indicators. 
Also, refines the RFP parsing prompt to enforce strict extraction of primary_country metadata for cleaner GIS spatial indexing.
Pipeline Data Flow: RFP data is passed between modules via the global React Router state object, allowing for seamless transition from data ingestion (/rfp-parser) to strategic matrix generation (/logframe).

## 💻 System Requirements

Runtime Environment: Python v3.9 or higher.

Package Management: pip (Python Package Installer) and virtualenv modules.

Operating System Support: Linux, macOS, or Windows (with GTK3 runtime binaries configured).

AI Access Credentials: An active Google AI Studio Gemini API key (or alternative LLM integration keys).

## 🚀 Installation & Setup

OpenWSH-CONTROL is structured with a decoupled codebase. For clean organization, it is highly recommended to keep both the frontend and backend directories nested side-by-side inside a single workspace folder.

1. Clone the Repository

Download the backend server repository onto your local system:

git clone
```bash
https://github.com/DeonLondn/wash-rfp-backend.git
```



2. Configure Your Virtual Environment

Navigate to the root directory of the backend folder and initialize an isolated Python environment:

cd wash-rfp-backend
python -m venv venv


## Activate the environment based on your current operating system:

```bash
macOS / Linux:

source venv/bin/activate


Windows (Command Prompt):

venv\Scripts\activate.bat


Windows (PowerShell):

.\venv\Scripts\Activate.ps1
```


3. Install Required Dependencies

Once your virtual environment is active, install the required packages:

```bash
pip install -r requirements.txt
```


4. Configure Environment Variables

Create a new file named .env in the root of the wash-rfp-backend directory. Use the provided .env.example as a template:

I  used (GOOGLE_API_KEY=your_gemini_api_key_here); you can select any LLM key of your preference


(Swap the placeholder value with your live authorization token generated from your LLM).

5. Start the Server

Run the local server using the high-performance ASGI web server, Uvicorn:

```bash
uvicorn main:app --reload
```

## NOTE:
The application will launch on http://localhost:8000. You can access the auto-generated Swagger documentation at http://localhost:8000/docs to test endpoints interactively.

## 🛠️ Windows Troubleshooting: PDF Generation & GTK3 Setup

1. GTK3 SETUP: If you are running the backend on a Windows machine and encounter compilation errors related to OS libraries (such as those required by PDF compilers like WeasyPrint), you must install the missing system dependencies.

Download the unified package gtk3-runtime-3.24.31-2022-01-04-ts-win64 (or a newer stable release of the GTK3 runtime for Windows).

Run the installer and proceed with all options left at DEFAULT.

Ensure the checkbox for "Set to PATH environment variable" is enabled during the wizard.

Restart your terminal window and restart your virtual environment. This will automatically link the system libraries to your execution path, fully resolving WeasyPrint rendering and compilation errors on Windows.

2. WINDOWS USERS ONLY: The PDF compiler in LogFrame Matrix window requires (wkhtmltopdf) installed on the host server. Ensure the binary path is included in the system environment PATH variables. Download from: https://wkhtmltopdf.org/downloads/


run
```bash
.\venv\Scripts\Activate.ps1
```
for a refresh and then 

run 
```bash
uvicorn main:app --reload
```

Also, try this command to install the package successfully

```bash
pip install pdfkit
```

if you encounter any error after running these commands because you worked in a global environemt previously,
try doing a clean install of all your packages in requirements.txt, so your system can detect can install pdfkit.

run 
```bash
pip install -r requirements.txt
```

Check to verify installed packages:

```bash
type requirements.txt
```
then save your packages with :

```bash
pip freeze > requirements.txt
```
## NOTE: 
MAKE SURE THE REQUIREMENTS.TXT FILE IS NOT EMPTY. YOR BACKEND SERVER OR PROJECT NEEDS EVERY PACKAGE IN IT TO RUN THE APP SUCCESSFULLY


## 📡 Backend API Reference

```bash
Endpoint Route           HTTP Method   Data Protocol     Operational Function & Execution Context
                       
/                        GET           HTTP              Validates runtime availability  and reverse proxy status.
                       
/api/parse-rfp           POST          HTTP(Multipart)   Accepts a raw PDF multipart upload. Runs async AI extraction 

/api/context/{country}   GET           HTTP              Returns baseline telemetry. Falls back to calculation loops for unindexed countries.

/ws/collaborate/{id}      WS           WebSocket         Establishes bidirectional streaming socket connection 
```


📂 Project Structure

```bash
OpenWsh-Control/
├── wash-rfp-backend/
│   ├── main.py                 # Core API routing, socket states, and AI prompts
│   ├── requirements.txt        # Backend dependencies list
│   ├── .env                    # System secrets (ignored by Git)
│   ├── venv/                   # Environemt configuration 
│   └── .gitignore              # Root system ignoring patterns
├── wash-rfp-frontend/          # Front-End Web Client
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── package.json
├── .gitignore                 
└── README.md
```


## ⚠️ Important Security Note: 
Ensure that your local .env configuration file is explicitly registered inside your .gitignore file. Never commit sensitive environment configurations, server keys, or API credentials to public code repositories. Only commit configuration templates like .env.example.


## 📄 License & Authors

Lead Architect: Gideon Lartey (DeonLondn)

Last Code Optimization: May 2026

Licensed under the terms of the open-source MIT License—see the root LICENSE file for precise details.


## ⚖️ Disclaimer

This is an independent systems prototype built strictly for technical demonstration and educational purposes. It is not associated, affiliated, endorsed, or partnered in any way with WaterAid, or any organization, interest, subsidiary, or entity connected to the official WaterAid organization.





