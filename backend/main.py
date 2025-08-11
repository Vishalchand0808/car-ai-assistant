# backend/main.py
# This script creates a FastAPI web server for our backend logic.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our existing modules
from nlp.intent_classifier import get_intent
from nlp.entity_extractor import extract_entities
from handlers.spotify_handler import play_music_based_on_entities
from handlers.weather_handler import get_weather_for_location

# --- 1. Initialize the FastAPI App ---
app = FastAPI(
    title="Car AI Assistant API",
    description="API for the in-car AI assistant.",
    version="1.0.0",
)

# --- 2. Configure CORS ---
# This is a crucial security step. It allows our React frontend (running on localhost:5173)
# to make requests to our backend server (running on localhost:8000).
origins = [
    "http://localhost:5173",
    "http://localhost:3000", # A common port for React dev servers
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)

# --- 3. Define Request/Response Models ---
# This tells FastAPI what kind of data to expect in the request body.
class CommandRequest(BaseModel):
    text: str

# --- 4. Define Simulated Handlers (as before) ---
def handle_navigation(entities: dict):
    location = entities.get("location")
    if location:
        return f"Okay, setting up navigation to {location}."
    else:
        return "Where would you like to navigate to?"

def handle_temperature_change(text: str):
    if "warmer" in text or "increase" in text or "up" in text:
        return "Okay, making it a bit warmer in here."
    elif "cooler" in text or "decrease" in text or "down" in text:
        return "Okay, cooling things down for you."
    else:
        return "Adjusting the temperature."

def handle_calling(entities: dict):
    contact = entities.get("contact_name")
    if contact:
        return f"Calling {contact} now..."
    else:
        return "Who would you like me to call?"

# --- 5. Create the Main API Endpoint ---
@app.post("/process-command")
async def process_command(request: CommandRequest):
    """
    This is the main endpoint that receives a command from the frontend,
    processes it, and returns the assistant's response.
    """
    user_input = request.text
    print(f"\n[API] Received command: '{user_input}'")

    # Step 1: Get Intent
    intent = get_intent(user_input)
    if not intent:
        return {"response": "I'm sorry, I'm having trouble understanding. Could you rephrase?"}

    # Step 2: Extract Entities
    entities = extract_entities(user_input, intent)

    # Step 3: Route to the Correct Handler
    final_response = ""
    if intent == 'play_music':
        final_response = play_music_based_on_entities(entities)
    elif intent == 'get_weather':
        location = entities.get("location")
        final_response = get_weather_for_location(location)
    elif intent == 'navigate':
        final_response = handle_navigation(entities)
    elif intent == 'adjust_temperature':
        final_response = handle_temperature_change(user_input)
    elif intent == 'call_person':
        final_response = handle_calling(entities)
    else:
        final_response = "I'm not sure how to handle that intent yet."

    print(f"[API] Sending response: '{final_response}'")
    return {"response": final_response}

# --- 6. Add a Root Endpoint for Health Check ---
@app.get("/")
def read_root():
    return {"status": "Car AI Assistant backend is running!"}

# To run this server:
# 1. Open a terminal in the 'backend' folder.
# 2. Make sure your conda env is active.
# 3. Run the command: uvicorn main:app --reload
