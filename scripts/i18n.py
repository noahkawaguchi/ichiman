import json
import copy
from pathlib import Path

import pandas as pd
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
        arg_CDF: mdates.ConciseDateFormatter,
        lang: str = 'en-US',
        ) -> mdates.ConciseDateFormatter:
    """Format a ConciseDateFormatter based on localized formatting.
    Currently only US English ('en-US') or Japanese ('ja').
    """

    ret_CDF = copy.copy(arg_CDF)

    if lang == 'en-US':
        # Set the formatting for the beginning of the month amongst 
        # ticks of mostly days
        ret_CDF.zero_formats[2] = '%b %e'

        # Make the "offset" string at the right of the axis in the 
        # standard order for US English 
        ret_CDF.offset_formats = ['', '%Y', '%B %Y', '%B %e, %Y',
                                    '%B %e, %Y', '%B %e, %Y %H:%M']
    
    elif lang == 'ja':
        # Change date formatting to Japanese
        ret_CDF.formats = ['%y年', '%-m月', '%e日', # format yr/mo/day
                            '%H:%M', '%H:%M', '%S.%f'] # not using hr/min/sec
        
        # Set "zeros" to mostly the same formatting except for the 
        # beginning of the month amongst ticks of mostly days
        ret_CDF.zero_formats = [''] + ret_CDF.formats[:-1]
        ret_CDF.zero_formats[2] = '%-m月%e日'

        # Make the "offset" string at the right of the axis have
        # Japanese formatting as well 
        ret_CDF.offset_formats = ['', '%Y年', '%Y年%-m月', '%Y年%-m月%e日',
                                    '%Y年%-m月%e日', '%Y年%-m月%e日 %H:%M']
    
    return ret_CDF

def localize_df_data(df: pd.DataFrame, lang: str = 'en-US') -> pd.DataFrame:
    """Format a DataFrame using human-readable dates and durations 
    based on the user's language. 
    Currently only US English ('en-US') or Japanese ('ja').
    """
    format_df = df.copy()

    # Change the date column to a readable format for the locale 
    if lang == 'en-US':
        format_df['date'] = format_df['date'].dt.strftime('%a, %b %e, %Y')
    elif lang == 'ja':
        format_df['date'] = format_df['date'].dt.strftime('%Y年%-m月%e日（%a）')
        format_df = format_df.rename(columns={'date': '日付'})

    # Show in minutes if the max is 2 hours or under, otherwise show in 
    # hours
    format_df['duration'] = format_df['duration'].dt.total_seconds() / 60
    if max(format_df['duration']) <= 120:
        if lang == 'en-US':
            format_df = format_df.rename(columns={'duration': 'minutes'})
        elif lang == 'ja':
            format_df = format_df.rename(columns={'duration': '分間'})
    else:
        format_df['duration'] = format_df['duration'] / 60
        format_df['duration'] = format_df['duration'].round(1)
        if lang == 'en-US':
            format_df = format_df.rename(columns={'duration': 'hours'})
        elif lang == 'ja':
            format_df = format_df.rename(columns={'duration': '時間数'})
    
    return format_df
