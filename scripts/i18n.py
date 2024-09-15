import json
import copy
from pathlib import Path

import matplotlib.dates as mdates


file_path = Path(__file__).parents[1] / 'translations.json'
with open(file_path, 'r') as tr:
    translations = json.load(tr)

def get_translation(key_path: str, language: str = 'en-US') -> str:
    """Get the translation for the given key path in the given language"""
    key1, key2 = key_path.split('.')
    # Use an empty dictionary if the language or outer key does not exist. 
    # Return the inner key itself if the language or a key does not exist.
    return translations.get(language, {}).get(key1, {}).get(key2, key2)

def test_name_to_japanese(test_name: str) -> str:
    """Convert the name of a set of test data to Japanese"""
    return (test_name.replace('-day test data', '日間のテストデータ')
            .replace(' with short durations', '（割と短い時間）'))

def localize_ConciseDateFormatter(
        input_formatter: mdates.ConciseDateFormatter,
        lang: str = 'en-US',
        ) -> mdates.ConciseDateFormatter:
    """Format a ConciseDateFormatter based on localized formatting.
    Currently only US English ('en-US') or Japanese ('ja').
    """

    ret_formatter = copy.copy(input_formatter)

    if lang == 'en-US':
        # Set the formatting for the beginning of the month amongst 
        # ticks of mostly days
        ret_formatter.zero_formats[2] = '%b %d'

        # Make the "offset" string at the right of the axis in the 
        # standard order for US English 
        ret_formatter.offset_formats = ['', '%Y', '%B %Y', '%B %d, %Y',
                                    '%B %d, %Y', '%B %d, %Y %H:%M']
    
    elif lang == 'ja':
        # Change date formatting to Japanese
        ret_formatter.formats = ['%y年', '%m月', '%d日', # format yr/mo/day
                            '%H:%M', '%H:%M', '%S.%f'] # not using hr/min/sec
        
        # Set "zeros" to mostly the same formatting except for the 
        # beginning of the month amongst ticks of mostly days
        ret_formatter.zero_formats = [''] + ret_formatter.formats[:-1]
        ret_formatter.zero_formats[2] = '%m月%d日'

        # Make the "offset" string at the right of the axis have
        # Japanese formatting as well 
        ret_formatter.offset_formats = ['', '%Y年', '%Y年%m月', '%Y年%m月%d日',
                                    '%Y年%m月%d日', '%Y年%m月%d日 %H:%M']
    
    return ret_formatter
