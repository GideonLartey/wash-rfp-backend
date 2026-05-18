
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)]()
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)]()

## OPENWSH-CONTROL
A comprehensive, full-stack analytics and processing prototype designed for WaterAid (see disclaimer below), Water, Sanitation, and Hygiene (WASH) initiative. OpenWSH-CONTROL provides technical teams  and directors with autonomous RFP data extraction, macro-indicator context fetching, systems strengthening recommendations, a climate prediction engine, and real-time multiplayer system modeling. The system relies on five foundational analytical views, each isolated cleanly via client-side routing to guarantee modular runtime execution.
## URL: https://www.openwsh-control.xyz


## System Requirements
Frontend: Node.js v18+, npm/yarn
Backend: Python v3.9+, pip
API Keys: Google Gemini API access or any AI of your choice(Claude, ChatGPT)
Installation & Setup
This project uses a decoupled architecture. You can create a project that houses both the backend server and the frontend client. 
I deliberately uploaded both files as separate entities. You should ensure both folders are in a master folder(OPENWSH-CONTROL) 
for organization


## BACKEND INSTALLATION
1. **Clone the Repository**
Download backend to your local machine:
git clone https://github.com/DeonLondn/wash-rfp-backend.git

2. **Backend Setup (FastAPI / Python)**
Open a new terminal and navigate to the backend folder:
cd wash-rfp-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Environment Configuration: Create a .env file in the wash-rfp-backend directory:
YOUR_AI_API_KEY=your_ai_api_key_here

3. **Run the Server:**
uvicorn main:app --reload. If you encounter any error in the terminal while using a  Windows machine,
download the “gtk3-runtime-3.24.31-2022-01-04-ts-win64,” which will fix the error. Just go to Google and download from the first
search result. Leave everything as DEFAULT(don’t change anything). It will automatically install to the PATH directory on your computer’s
Environment Variables section.


## Backend API Reference
Endpoint	             - Method	    - Description

/	                     - GET	        - Health check and server status.
/api/parse-rfp	         - POST         - Accepts a PDF UploadFile and returns extracted JSON metadata.
/api/context/{country}	 - GET	        - Returns LiveContextData (Water Stress, Governance, Risk).
/ws/collaborate/{id}	 - WS	        - Establishes a bidirectional WebSocket connection for live UI sync.

## Project Structure
OpenWsh-Control/
├── wash-rfp-backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── wash-rfp-frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── .env.example
├── .gitignore
└── README.md

## NOTE: Your ".env.example" goes into your .gitignore file


## Future Enhancements
1. Export Master Report to comprehensive PDFs.
2. PostgreSQL database integration for persistent workspaces.
3. Redis caching layer for frequent country queries.
4. Replace mock dictionary with HTTP calls to live Donor Data APIs.


## License & Authors
Developer: [Gideon Lartey/DeonLondn]
Last Updated: May 2026
MIT License

## DISCLAIMER: 
This is an independent systems prototype for demonstration purposes only, and is not affiliated in any way with 
WaterAid or any organization, interest, or entity affiliated with WaterAid organization.