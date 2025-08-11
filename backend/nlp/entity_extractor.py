# backend/nlp/entity_extractor.py

from transformers import pipeline
import re

# --- 1. Initialize the Models (Pipelines) ---
# This is done once when the module is first imported, making it efficient.
try:
    print("[Entity Extractor] Loading models...")
    # Pipeline for Named Entity Recognition (to find names, locations, etc.)
    ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)
    
    # Pipeline for Emotion Classification (to find the mood)
    emotion_pipeline = pipeline("text-classification", model="bhadresh-savani/bert-base-go-emotion")
    print("[Entity Extractor] Models loaded successfully.")
except Exception as e:
    print(f"[Entity Extractor] Error loading models: {e}")
    ner_pipeline = None
    emotion_pipeline = None

# --- 2. Define Helper Data ---
# A simple list of languages we can search for
SUPPORTED_LANGUAGES = {"hindi", "english", "punjabi", "gujarati", "bhojpuri", "spanish"}

# A mapping from the detailed emotions of the model to our simple mood categories
EMOTION_TO_MOOD_MAP = {
    'admiration': 'happy',
    'amusement': 'happy',
    'approval': 'happy',
    'caring': 'relaxed',
    'desire': 'excited',
    'excitement': 'excited',
    'gratitude': 'happy',
    'joy': 'happy',
    'love': 'happy',
    'optimism': 'happy',
    'pride': 'happy',
    'relief': 'relaxed',
    'anger': 'angry',
    'annoyance': 'angry',
    'disapproval': 'angry',
    'disgust': 'angry',
    'grief': 'sad',
    'sadness': 'sad',
    'disappointment': 'sad',
    'embarrassment': 'sad',
    'fear': 'sad',
    'remorse': 'sad',
    'confusion': 'neutral',
    'curiosity': 'neutral',
    'nervousness': 'neutral',
    'realization': 'neutral',
    'surprise': 'neutral',
    'neutral': 'neutral'
}

# --- 3. The Main Extraction Function ---
def extract_entities(text: str, intent: str) -> dict:
    """
    Extracts relevant entities from the text based on the classified intent.

    Args:
        text (str): The user's input command.
        intent (str): The intent classified by our primary model.

    Returns:
        dict: A dictionary containing the extracted entities.
    """
    entities = {
        "mood": None,
        "language": None,
        "artist": None,
        "location": None,
        "contact_name": None,
    }

    if not text or not intent:
        return entities

    # --- Entity Extraction for Music ---
    if intent == 'play_music':
        # a) Extract Language (simple keyword search)
        for lang in SUPPORTED_LANGUAGES:
            if re.search(r'\b' + lang + r'\b', text.lower()):
                entities["language"] = lang
                break # Stop after finding the first language
        
        # b) Extract Artist (using NER)
        if ner_pipeline:
            ner_results = ner_pipeline(text)
            for entity in ner_results:
                if entity['entity_group'] == 'PER': # PER stands for Person
                    entities["artist"] = entity['word']
                    break # Stop after finding the first artist name
        
        # c) Extract Mood (using emotion model)
        # This is a good fallback if no language or artist is mentioned.
        if emotion_pipeline:
            emotion_results = emotion_pipeline(text)
            top_emotion = emotion_results[0]['label']
            entities["mood"] = EMOTION_TO_MOOD_MAP.get(top_emotion, 'neutral')

    # --- Entity Extraction for Weather or Navigation ---
    elif intent in ['get_weather', 'navigate']:
        if ner_pipeline:
            ner_results = ner_pipeline(text)
            for entity in ner_results:
                if entity['entity_group'] == 'LOC': # LOC stands for Location
                    entities["location"] = entity['word']
                    break # Stop after finding the first location

    # --- Entity Extraction for Calling ---
    elif intent == 'call_person':
        if ner_pipeline:
            ner_results = ner_pipeline(text)
            for entity in ner_results:
                if entity['entity_group'] == 'PER': # PER stands for Person
                    entities["contact_name"] = entity['word']
                    break # Stop after finding the first person's name

    print(f"  [Entity Extractor] Extracted Entities: {entities}")
    return entities

# --- Testing Block ---
# To run it, open a terminal in your `backend` folder and type:
# python nlp/entity_extractor.py
if __name__ == "__main__":
    print("\n--- Testing Entity Extractor ---")

    # Test Case 1: Music with mood and language
    text1 = "play some sad hindi songs for me"
    intent1 = "play_music"
    print(f"\nInput: '{text1}' (Intent: {intent1})")
    entities1 = extract_entities(text1, intent1)
    
    # Test Case 2: Music with artist
    text2 = "I want to listen to Arijit Singh"
    intent2 = "play_music"
    print(f"\nInput: '{text2}' (Intent: {intent2})")
    entities2 = extract_entities(text2, intent2)

    # Test Case 3: Weather
    text3 = "what is the weather like in Guwahati"
    intent3 = "get_weather"
    print(f"\nInput: '{text3}' (Intent: {intent3})")
    entities3 = extract_entities(text3, intent3)

    # Test Case 4: Calling
    text4 = "can you please call Soni"
    intent4 = "call_person"
    print(f"\nInput: '{text4}' (Intent: {intent4})")
    entities4 = extract_entities(text4, intent4)
