# Standard library imports
import datetime as dt
import os
from glob import glob

# Third party imports
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Local project imports
from . import csv_utils
from .menu_helpers import get_user_duration, new_data, read_chosen_file, avg_duration_str


def new_habit() -> None:
    """Get the name of the new habit, making sure there is not already a
    habit of the same name that would be overwritten.
    Get the amount of time spent today and create a new CSV file.
    """
    # Find all the CSV files in the sibling "data" directory.
    data_dir = os.path.join(os.getcwd(), 'data')
    csv_paths = glob(os.path.join(data_dir, '*.csv'))
    existing_CSVs = [os.path.basename(csv) for csv in csv_paths]
    
    # Prompt the user to enter a new filename until they provide one
    # that does not already exist.
    print("Let's start a new habit!")
    print()
    while True:
        user_habit_name = input('Enter the name of the new habit: ') + '.csv'
        print()
        if user_habit_name in existing_CSVs:
            print(('You are already tracking a habit with that name. '
                   'Please enter something different to start a new habit.'))
            print()
        else:
            break
    
    # Prompt the user to enter the amount of time for today and write
    # the data to a new CSV file.
    print('A journey of ten thousand hours begins with a single day.')
    print()
    today = dt.datetime.now().date()
    todays_duration = get_user_duration(today)
    csv_utils.write_csv(user_habit_name, [today], [todays_duration])
    print('New habit started. Congratulations!')
    print()

def track_habit() -> None:
    """Prompt the user to select one of their existing habits and update
    its data up to the present day.
    Append the data to the corresponding CSV file.
    """
    # Find all the CSV files in the sibling "data" directory.
    data_dir = os.path.join(os.getcwd(), 'data')
    csv_paths = glob(os.path.join(data_dir, '*.csv'))
    existing_CSVs = [os.path.basename(csv) for csv in csv_paths]

    # Prompt the user to choose one of the habits.
    print("The habits you're currently tracking are:")
    for filename in existing_CSVs:
        print(filename[:-4])
    print()
    while True:
        chosen_filename = input('Which one would you like to update? ') + '.csv'
        print()
        if chosen_filename in existing_CSVs:
            break
        else:
            print("Habit not found. Please enter one of the options above.")
            print()

    # Update the data.
    old_dates, old_durations = csv_utils.read_csv(chosen_filename)
    new_dates, new_durations = new_data(old_dates, old_durations)
    csv_utils.append_csv(chosen_filename, new_dates, new_durations)

def calculate_avg() -> None:
    """Prompt the user to select one of the habits they're currently
    tracking and the number of days to calculate the average for. 
    Print the average as a human-readable string.
    """
    # Get the data for a habit of the user's choosing.
    dates, durations = read_chosen_file()

    # Prompt the user for the number of days to calculate the average 
    # for and print the result.
    while True:
        try:
            days = int(input('For how many days would you like to '
                             'calculate the average? '))
            print()
            if days > len(durations):
                days = len(durations)
                print(f'You only have {days} days recorded.')
            avg_str = avg_duration_str(durations[-days:])
            print((f'The average for the last {days} recorded days is '
                   f'{avg_str}.'))
            print()
            break
        except ValueError:
            print()
            print('Invalid input. Please enter a number only.')
            print()

def goal_progress() -> None:
    """Prompt the user to select one of the habits they're currently
    tracking and for their goal number of hours. Print information on 
    how much they have already completed and how far they have left to go.
    """
    # Get the data for a habit of the user's choosing.
    dates, durations = read_chosen_file()

    # Calculate how much the user has already completed and how much
    # they complete per day on average.
    time_completed = sum(durations, dt.timedelta(0))
    hours_completed = time_completed.total_seconds() / 3600
    avg_delta = sum(durations, dt.timedelta(0)) / len(durations)
    avg_hours = avg_delta.total_seconds() / 3600

    # Get the user's goal number of hours.
    print(("A common goal is 10,000 hours, popularized by Malcolm "
           "Gladwell. You can use that number if you can't think of "
           "anything better, but many people don't actually need that "
           "long to achieve what they want to achieve."))
    print()
    while True:
        try:
            user_goal = int(
                input("What's your goal (in hours)? ").replace(',', '')
                )
            print()
            if user_goal <= 0:
                print("Invalid input. Please enter a positive number.")
                print()
            else:
                break
        except ValueError:
            print()
            print('Invalid input. Please enter a number only.')
            print()
    
    # As long as the user hasn't already completed their goal, calculate
    # and print how far they've come and how far they have left to go.
    if user_goal <= hours_completed:
        print("You've already reached your goal. Congrats!")
        print()
    else:
        percent_complete = (hours_completed / user_goal) * 100
        hours_remaining = user_goal - hours_completed
        days_remaining = hours_remaining / avg_hours
        years_remaining = days_remaining / 365
        print((f'You have completed {hours_completed:.1f} out of {user_goal} '
            f'hours, or {percent_complete:.0f} percent. If you maintain '
            f'your average so far of {avg_hours:.1f} hours per day, it '
            f'will take {days_remaining:.0f} more days, or '
            f'{years_remaining:.2f} years, to reach your goal.'))
        print()

def create_graph() -> None:
    """Prompt the user to select one of the habits they're currently
    tracking and display a graph of the data.
    """
    # Get the data for a habit of the user's choosing.
    dates, durations = read_chosen_file()
    
    # Convert timedeltas into minutes
    minutes = [int(duration.total_seconds() / 60) for duration in durations]
    
    # Use minutes for 2 hours and under, otherwise use hours
    if max(minutes) <= 120:
        y_durations = minutes
        y_unit = 'Minutes'
    else:
        y_durations = [minutes_duration / 60 for minutes_duration in minutes]
        y_unit = 'Hours'

    # Create a DataFrame
    df = pd.DataFrame({'Date': dates, 'Duration': y_durations})

    # Ensure the 'Date' column is of datetime type
    df['Date'] = pd.to_datetime(df['Date'])

    # Set the 'Date' column as the index
    df.set_index('Date', inplace=True)

    # Resample the data by week and calculate the means for each week and month
    weekly_average = df.resample('W').mean()
    monthly_average = df.resample('ME').mean()

    # Set up the graph depending on the size of the data set
    plt.figure(figsize=(7,5), dpi=150)
    if len(dates) < 15:
        plt.plot(dates, y_durations, color='red', marker='o', label='Daily Data')
    elif len(dates) < 62:
        plt.scatter(dates, y_durations, color='blue', marker='.', label='Daily Data')
        plt.plot(weekly_average.index, weekly_average['Duration'], color='red', 
                 marker='o', label='Weekly Averages')
    else:
        plt.scatter(dates, y_durations, color='gray', marker='.', label='Daily Data')
        plt.plot(weekly_average.index, weekly_average['Duration'], color='blue', 
                 marker='.', linestyle='--', label='Weekly Averages')
        plt.plot(monthly_average.index, monthly_average['Duration'], 
                 color='red', marker='o', label='Monthly Averages')
    plt.title('Time Spent Per Day')
    plt.xlabel('Dates')
    plt.ylabel(y_unit)

    # Use AutoDateLocator to automatically select appropriate date intervals
    locator = mdates.AutoDateLocator()
    plt.gca().xaxis.set_major_locator(locator)

    # Use ConciseDateFormatter to make the date labels more readable
    plt.gca().xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

    plt.legend()
    plt.grid(True)
    plt.show()
    