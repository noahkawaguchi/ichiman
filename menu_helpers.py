import datetime as dt
import glob
from typing import List, Tuple

import csv_utils

def get_user_duration(date_in_question: dt.date) -> dt.timedelta:
    """Prompt the user until they return a valid duration of time for 
    the given date.
    Return that duration as a timedelta.
    """
    formatted_date = date_in_question.strftime('%a, %b %d, %Y')
    print((f'Enter the amount of time for {formatted_date} in '
            'hours and minutes.'))
    while True:
        hours_string = input('How many hours? ')
        minutes_string = input('How many minutes? ')
        print()
        try:
            return dt.timedelta(hours=int(hours_string), 
                                minutes=int(minutes_string))
        except ValueError:
            print('Invalid input. Please enter numbers only.')
            print()

def new_data(
        old_dates: List[dt.date], old_durations: List[dt.timedelta],
        ) -> Tuple[List[dt.date], List[dt.timedelta]]:
    """Given the currently recorded dates and durations, prompt 
    the user to enter data for each day up to the present day. 
    Return lists of the new dates and durations. 
    """

    # No need to change anything if the data is already up to date
    today = dt.datetime.now().date()
    latest_date = old_dates[-1]
    if latest_date >= today:
        print('Already up to date!')
        print()
        return [], []
    
    # Get data for every missing day up to and including today
    else:
        print("Let's get our data up to date!")
        print()
        next_day = latest_date + dt.timedelta(days=1)
        new_dates = []
        new_durations = []
        while today not in new_dates:
            new_durations.append(get_user_duration(next_day))
            new_dates.append(next_day)
            next_day += dt.timedelta(days=1)
        print('Habit tracked!')
        print()
        return new_dates, new_durations

def read_chosen_file() -> Tuple[List[dt.date], List[dt.timedelta]]:
    """Prompt the user to select an existing habit.
    Read and return the data for that habit.
    """
    # Prompt the user to select an existing habit
    existing_CSVs = glob.glob('*.csv')
    print("The habits you're currently tracking are:")
    for filename in existing_CSVs:
        print(filename[:-4])
    print()
    while True:
        chosen_filename = input('Which one would you like to use? ') + '.csv'
        print()
        if chosen_filename in existing_CSVs:
            break
        else:
            print("Habit not found. Please enter one of the above options.")
            print()
    
    # Read and return the data from the CSV file corresponding to the
    # user's choice.
    dates, durations = csv_utils.read_csv(chosen_filename)
    return dates, durations

def avg_duration_str(durations: List[dt.timedelta]) -> str:
    """Calculate the mean of the provided durations.
    Return the result as a human-readable string.
    Ex: "2 hours and 35 minutes"; "1 minute"
    """
    avg_delta = sum(durations, dt.timedelta(0)) / len(durations)
    total_minutes = int(avg_delta.total_seconds() / 60)
    hours, minutes = divmod(total_minutes, 60)

    if hours == 0:
        if minutes == 0:
            readable = '0 minutes'
        elif minutes == 1:
            readable = '1 minute'
        else:
            readable = f'{minutes} minutes'
    elif hours == 1:
        if minutes == 0:
            readable = '1 hour'
        elif minutes == 1:
            readable = '1 hour and 1 minute'
        else:
            readable = f'1 hour and {minutes} minutes'
    else:
        if minutes == 0:
            readable = f'{hours} hours'
        elif minutes == 1:
            readable = f'{hours} hours and 1 minute'
        else:
            readable = f'{hours} hours and {minutes} minutes'
    
    return readable
