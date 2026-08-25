import os
import json
import base64
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from google import genai
from google.genai import types


load_dotenv()

app = FastAPI(
    title="PetOlife AI Health Timeline",
    version="1.0.0"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Gemini
# ---------------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured")


client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "PetOlife AI Health Timeline API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ---------------------------------------------------------
# Document analysis
# ---------------------------------------------------------

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )

    try:

        file_bytes = await file.read()

        mime_type = file.content_type or "application/pdf"

        # Gemini-compatible input
        document_part = types.Part.from_bytes(
            data=file_bytes,
            mime_type=mime_type
        )

        prompt = """
You are a veterinary health-record analysis assistant.

Analyze the uploaded pet health document.

Extract information ONLY when it is actually present in the document.

Return ONLY valid JSON in this exact structure:

{
  "pet_name": "",
  "document_type": "",
  "summary": "",
  "events": [
    {
      "date": "YYYY-MM-DD",
      "type": "checkup",
      "title": "",
      "description": "",
      "status": ""
    }
  ],
  "lab_results": [
    {
      "name": "",
      "value": "",
      "unit": "",
      "reference_range": ""
    }
  ],
  "medications": [
    {
      "name": "",
      "strength": "",
      "form": "",
      "frequency": "",
      "duration": "",
      "status": ""
    }
  ],
  "vaccinations": [
    {
      "name": "",
      "last_administered": "",
      "next_due": ""
    }
  ],
  "insights": []
}

For events, identify things such as:
- veterinary checkups
- vaccinations
- laboratory tests
- medications
- diagnoses
- procedures
- important health observations

Do not invent information.

If a field is unavailable, use an empty string.

Return JSON only.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                document_part,
                prompt
            ]
        )

        text = response.text.strip()

        # Remove markdown JSON fences if Gemini adds them
        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        result = json.loads(text)

        return {
            "success": True,
            "file_name": file.filename,
            "data": result
        }

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Gemini returned invalid JSON"
        )

    except Exception as e:

        print("ANALYSIS ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Document analysis failed: {str(e)}"
        )