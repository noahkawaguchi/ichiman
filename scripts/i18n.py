import json
from pathlib import Path

file_path = Path(__file__).parents[1] / 'translations.json'

with open(file_path, 'r') as tr:
    translations = json.load(tr)

def get_translation(key_path: str, language: str = 'en') -> str:
    """Get the translation for the given key path in the given language"""
    key1, key2 = key_path.split('.')
    # Use an empty dictionary if the language or outer key does not exist. 
    # Return the inner key itself if the language or a key does not exist.
    return translations.get(language, {}).get(key1, {}).get(key2, key2)

def test_name_to_japanese(test_name: str) -> str:
    """Convert the name of a set of test data to Japanese"""
    return (test_name.replace('-day test data', '日間のテストデータ')
            .replace(' with short durations', '（割と短い時間）'))
