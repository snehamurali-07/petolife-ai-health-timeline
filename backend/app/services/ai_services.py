import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_health_document(file_path: str, mime_type: str):

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    prompt = """
You are an AI assistant for PetOLife, a pet health management application.

Analyze the uploaded veterinary health document.

Extract information that is actually present in the document.

Return ONLY valid JSON in exactly this structure:

{
  "pet_name": null,
  "document_type": null,
  "summary": "",
  "events": [
    {
      "date": null,
      "type": "",
      "title": "",
      "description": "",
      "status": ""
    }
  ],
  "lab_results": [],
  "medications": [],
  "vaccinations": [],
  "insights": []
}

Rules:

1. Never invent information.
2. If information is missing, use null or an empty array.
3. Dates should use YYYY-MM-DD when possible.
4. Event type can be:
   vaccination,
   medication,
   diagnosis,
   laboratory,
   checkup,
   surgery,
   other.
5. Keep the summary concise.
6. Extract important laboratory values when available.
7. Extract medication name and dosage when available.
8. Extract vaccination name and date when available.
9. insights should contain observations that can reasonably be derived from the document.
10. Do NOT provide a medical diagnosis beyond what the document states.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",

            contents=[
                types.Part.from_bytes(
                    data=file_bytes,
                    mime_type=mime_type
                ),
                prompt
            ],

            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        print("\n========== GEMINI RESPONSE ==========")
        print(response.text)
        print("=====================================\n")

        result = json.loads(response.text)

        return result

    except Exception as e:

        print("\n========== GEMINI ERROR ==========")
        print(str(e))
        print("==================================\n")

        return {
            "pet_name": None,
            "document_type": "unknown",
            "summary": "AI analysis could not be completed.",
            "events": [],
            "lab_results": [],
            "medications": [],
            "vaccinations": [],
            "insights": [],
            "error": str(e)
        }