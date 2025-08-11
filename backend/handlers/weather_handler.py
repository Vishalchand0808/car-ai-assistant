# backend/handlers/weather_handler.py

import os
from dotenv import load_dotenv
import requests

# --- 1. Load Environment Variables ---
load_dotenv()

# --- 2. Initialize API Key ---
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# It's good practice to check if the environment variable was loaded correctly
if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY is not set in the .env file!")

# --- 3. The Main Handler Function ---
def get_weather_for_location(location: str | None) -> str:
    """
    Fetches the current weather for a given location using the OpenWeatherMap API.

    Args:
        location (str | None): The name of the city/location.

    Returns:
        str: A formatted string with the weather description, or an error message.
    """
    # If the entity extractor didn't find a location, default to a known city
    if not location:
        print("  [Weather Handler] No location provided, defaulting to Guwahati.")
        location = "Guwahati"

    print(f"  [Weather Handler] Fetching current weather for: '{location}'...")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  # Get temperature in Celsius
    }
    
    try:
        response = requests.get(base_url, params=params)
        # This line will raise an error for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        weather_data = response.json()
        
        # Safely extract information using .get() to avoid errors if a key is missing
        description = weather_data.get('weather', [{}])[0].get('description', 'N/A').capitalize()
        temp = weather_data.get('main', {}).get('temp', 'N/A')
        feels_like = weather_data.get('main', {}).get('feels_like', 'N/A')
        
        result_string = (
            f"Currently in {location}, it is {temp}°C and the sky is: {description}. "
            f"It feels like {feels_like}°C."
        )
        print(f"  [Weather Handler] Success: {result_string}")
        return result_string
        
    except requests.exceptions.HTTPError as http_err:
        # Handle specific HTTP errors from the API
        if response.status_code == 401:
            error_message = "Error: Invalid API Key. Please check your OpenWeatherMap API key. Note: New keys can take a few minutes to an hour to activate."
        elif response.status_code == 404:
            error_message = f"Error: The city '{location}' could not be found."
        else:
            error_message = f"An HTTP error occurred: {http_err}"
        
        print(f"  [Weather Handler] {error_message}")
        return "Sorry, I couldn't fetch the weather right now."
        
    except requests.exceptions.RequestException as req_err:
        # Handle network-related errors (e.g., no internet connection)
        print(f"  [Weather Handler] A network error occurred: {req_err}")
        return "Sorry, I'm having trouble connecting to the weather service."

    except Exception as e:
        # Catch any other unexpected errors
        print(f"  [Weather Handler] An unexpected error occurred: {e}")
        return "Sorry, an unexpected error occurred while fetching the weather."

# --- Testing Block ---
if __name__ == "__main__":
    print("\n--- Testing Weather Handler ---")

    # Test Case 1: A valid city
    print("\nTest Case 1: Valid City")
    get_weather_for_location("Mumbai")

    # Test Case 2: Another valid city
    print("\nTest Case 2: Another Valid City")
    get_weather_for_location("London")

    # Test Case 3: A city that doesn't exist
    print("\nTest Case 3: Invalid City")
    get_weather_for_location("NotARealCity")
    
    # Test Case 4: No location provided (should default to Guwahati)
    print("\nTest Case 4: No Location Provided")
    get_weather_for_location(None)
