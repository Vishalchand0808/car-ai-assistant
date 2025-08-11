# backend/nlp/intent_classifier.py
# FINAL VERSION: This file calls the Gradio Space API using the official gradio_client library.

import os
from dotenv import load_dotenv
from gradio_client import Client, exceptions
from urllib.parse import urlparse

# --- 1. Load Environment Variables ---
load_dotenv()

# --- 2. Configure the Gradio Client ---
# Get the standard URL of your running Hugging Face Space from the .env file
# e.g., "https://huggingface.co/spaces/Vishalchand0808/car-intent-classifier-demo"
SPACE_URL = os.getenv("HF_SPACE_URL")

if not SPACE_URL:
    raise ValueError("HF_SPACE_URL is not set in the .env file! Please add it.")

def get_space_id_from_url(space_url: str) -> str:
    """Extracts the 'username/repo_name' ID from a full Hugging Face Space URL."""
    parsed_url = urlparse(space_url)
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) == 3 and path_parts[0] == 'spaces':
        return f"{path_parts[1]}/{path_parts[2]}"
    raise ValueError("Invalid Hugging Face Space URL format. Expected format: https://huggingface.co/spaces/username/space-name")

# Extract the Space ID (e.g., "Vishalchand0808/car-intent-classifier-demo")
SPACE_ID = get_space_id_from_url(SPACE_URL)

# Initialize the client with the Space ID
try:
    print(f"Initializing Gradio client for Space: '{SPACE_ID}'...")
    client = Client(SPACE_ID)
    print("Gradio client initialized successfully.")
except Exception as e:
    print(f"Failed to initialize Gradio client: {e}")
    client = None

def get_intent(text: str) -> str | None:
    """
    Calls the deployed Gradio Space API to classify the intent of the given text.

    Args:
        text (str): The user's input command.

    Returns:
        str: The predicted intent label (e.g., 'play_music', 'get_weather').
             Returns None if the API call fails.
    """
    if not client:
        print("Gradio client is not available.")
        return None

    if not text or not isinstance(text, str):
        print("Invalid input text provided.")
        return None

    try:
        print(f"  [Intent Classifier] Predicting for text: '{text}'...")
        # Use the predict method as shown in the API documentation
        result = client.predict(
            text=text,
            api_name="/predict"
        )
        
        # The result is the raw string output from our Gradio function
        # e.g., "Intent: play_music (Score: 0.9987)"
        if "Intent: " in result:
            intent = result.split(" (")[0].replace("Intent: ", "")
            print(f"  [Intent Classifier] Raw Response: {result}")
            print(f"  [Intent Classifier] Predicted Intent: '{intent}'")
            return intent
        else:
            print(f"  [Intent Classifier] Received an unexpected response from the Space: {result}")
            return None

    except exceptions.APIError as e:
        # This handles specific Gradio API errors, like if the Space is building
        print(f"  [Intent Classifier] Gradio API error: {e}")
        return None
    except Exception as e:
        # This catches other errors (network, etc.)
        print(f"  [Intent Classifier] An unexpected error occurred: {e}")
        return None

# --- Testing Block ---
if __name__ == "__main__":
    print("\n--- Testing Intent Classifier via Gradio Client ---")
    
    if "YOUR_USERNAME" in SPACE_URL or not SPACE_URL:
        print("\n!!! PLEASE UPDATE the HF_SPACE_URL in your .env file with your actual Space URL before testing. !!!")
    else:
        test_command = "it's a bit chilly in here"
        print(f"\nInput: '{test_command}'")
        predicted_intent = get_intent(test_command)
        print(f"--> Final Intent: {predicted_intent}")

        test_command_2 = "play some happy punjabi songs"
        print(f"\nInput: '{test_command_2}'")
        predicted_intent_2 = get_intent(test_command_2)
        print(f"--> Final Intent: {predicted_intent_2}")
