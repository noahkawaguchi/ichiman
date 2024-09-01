import json

with open('../translations.json', 'r') as tr:
    translations = json.load(tr)

def get_trns(key: str, lang: str = 'en') -> str:
    """Get the translation for the given key in the given language"""
    # Return an empty dictionary if the language does not exist
    # Return the key itself if the key does not exist
    return translations.get(lang, {}).get(key, key)

user_lang = 'ja'

print(get_trns('farewell', user_lang))
