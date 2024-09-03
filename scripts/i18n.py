import json
from pathlib import Path

file_path = Path(__file__).parents[1] / 'translations.json'

with open(file_path, 'r') as tr:
    translations = json.load(tr)

def get_translation(key: str, language: str = 'en') -> str:
    """Get the translation for the given key in the given language"""
    # Return an empty dictionary if the language does not exist
    # Return the key itself if the key does not exist
    return translations.get(language, {}).get(key, key)
