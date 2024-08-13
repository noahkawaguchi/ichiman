import csv
import datetime as dt
from typing import List, Tuple
import glob

# requires installing matplotlib in a virtual environment
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# CSV file read/write/append functions

def read_csv(filename: str) -> Tuple[List[dt.date], List[dt.timedelta]]:
    """Read in the CSV file with the provided name 
    and return lists of the dates and durations.
    """
    try:
        with open(filename, mode='r', newline='') as csv_data:
            csv_reader = csv.reader(csv_data)
            fields = next(csv_reader)
            # print('Fields:', fields)
            dates = []
            durations = []
            for row in csv_reader:
                dates.append(dt.date.fromisoformat(row[0]))
                h, m = map(int, row[1].split(':'))
                durations.append(dt.timedelta(hours=h, minutes=m))
        return dates, durations
    except FileNotFoundError:
        print('Error: file not found')
        return ([],[])

def write_csv(
        filename: str, dates: List[dt.date], 
        durations: List[dt.timedelta]) -> None:
    """Format the provided dates and durations and write them to a new
    CSV file with the given name.
    (Checking that the filename doesn't already exist to avoid 
    overwriting should be performed in a different function.)
    """
    data = [['date', 'duration']]
    for date, duration in zip(dates, durations):
        date_str = date.strftime('%Y-%m-%d')
        total_minutes = int(duration.total_seconds() / 60)
        hours, minutes = divmod(total_minutes, 60)
        duration_str = f'{hours:02}:{minutes:02}'
        data.append([date_str, duration_str])
    
    with open(filename, mode='w', newline='') as new_csv:
        writer = csv.writer(new_csv)
        writer.writerows(data)

def append_csv(
        filename: str, dates: List[dt.date], 
        durations: List[dt.timedelta]) -> None:
    """Format the provided dates and durations and append them to the 
    CSV file with the given name.
    """
    try:
        with open(filename, mode='a', newline='') as existing_csv:
            csv_writer = csv.writer(existing_csv)
            data = []
            for date, duration in zip(dates, durations):
                date_str = date.strftime('%Y-%m-%d')
                total_minutes = int(duration.total_seconds() / 60)
                hours, minutes = divmod(total_minutes, 60)
                duration_str = f'{hours:02}:{minutes:02}'
                data.append([date_str, duration_str])
            csv_writer.writerows(data)
    except FileNotFoundError:
        print('Error: file not found')


# user input functions

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


# menu option helper functions

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

def graph_data(dates: List[dt.date], durations: List[dt.timedelta]) -> None:
    """Show a line graph of the provided dates and durations."""

    # Convert timedeltas into minutes
    minutes = [int(duration.total_seconds() / 60) for duration in durations]
    
    # Use minutes for 2 hours and under, otherwise use hours
    if max(minutes) <= 120:
        y_durations = minutes
        unit = 'Minutes'
    else:
        y_durations = [minutes_duration / 60 for minutes_duration in minutes]
        unit = 'Hours'
    
    # Set up a graph
    plt.figure(figsize=(7,5), dpi=150)
    plt.plot(dates, y_durations, marker='o')
    plt.title('Dates and Durations')
    plt.xlabel('Dates')
    plt.ylabel(f'Durations ({unit})')

    # Use AutoDateLocator to automatically select appropriate date intervals
    locator = mdates.AutoDateLocator()
    plt.gca().xaxis.set_major_locator(locator)

    # Use ConciseDateFormatter to make the date labels more readable
    plt.gca().xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

    plt.grid(True)
    plt.show()


# menu option functions

def new_habit() -> None:
    """Get the name of the new habit, making sure there is not already a
    habit of the same name that would be overwritten.
    Get the amount of time spent today and create a new CSV file.
    """
    print("Let's start a new habit!")
    print()

    # Prompt the user to enter a new filename until they provide one
    # that does not already exist.
    existing_CSVs = glob.glob('*.csv')
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
    write_csv(user_habit_name, [today], [todays_duration])
    print('New habit started. Congratulations!')
    print()

def track_habit() -> None:
    """Prompt the user to select one of their existing habits and update
    its data up to the present day.
    Append the data to the corresponding CSV file.
    """
    existing_CSVs = glob.glob('*.csv')
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

    old_dates, old_durations = read_csv(chosen_filename)
    new_dates, new_durations = new_data(old_dates, old_durations)
    append_csv(chosen_filename, new_dates, new_durations)

def calculate_avg() -> None:
    """Prompt the user to select one of the habits they're currently
    tracking and the number of days to calculate the average for. 
    Print the average as a human-readable string.
    """
     # Prompt the user to select an existing habit
    existing_CSVs = glob.glob('*.csv')
    print("The habits you're currently tracking are:")
    for filename in existing_CSVs:
        print(filename[:-4])
    print()
    while True:
        chosen_filename = input('Which one would you like to '
                                'calculate the average for? ') + '.csv'
        print()
        if chosen_filename in existing_CSVs:
            break
        else:
            print("Habit not found. Please enter one of the above options.")
            print()
    
    dates, durations = read_csv(chosen_filename)

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
    # Prompt the user to select an existing habit
    existing_CSVs = glob.glob('*.csv')
    print("The habits you're currently tracking are:")
    for filename in existing_CSVs:
        print(filename[:-4])
    print()
    while True:
        chosen_filename = input('Which one would you like to '
                                'calculate goal progress for? ') + '.csv'
        print()
        if chosen_filename in existing_CSVs:
            break
        else:
            print("Habit not found. Please enter one of the above options.")
            print()

    dates, durations = read_csv(chosen_filename)

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
    # Prompt the user to select an existing habit
    existing_CSVs = glob.glob('*.csv')
    print("The habits you're currently tracking are:")
    for filename in existing_CSVs:
        print(filename[:-4])
    print()
    while True:
        chosen_filename = input('Which one would you like to graph? ') + '.csv'
        print()
        if chosen_filename in existing_CSVs:
            break
        else:
            print("Habit not found. Please enter one of the above options.")
            print()
    
    # Graph the data for the chosen habit
    dates, durations = read_csv(chosen_filename)
    graph_data(dates, durations)
    

# print-only functions

def welcome(width: int) -> None:
    """Print the welcome message."""
    print()
    print('*' * width)
    print()
    print('Welcome to'.center(width))
    print('ICHIMAN'.center(width))
    print()
    print('a duration-based'.center(width))
    print('habit tracking program'.center(width))
    print()
    print('developed by'.center(width))
    print('Noah Kawaguchi'.center(width))
    print()
    print('*' * width)
    print()

def main_menu(width: int) -> None:
    """Print the main menu."""
    print('-' * width)
    print('MAIN MENU'.center(width))
    print('-' * width)
    print('1 - Start a New Habit')
    print('2 - Track an Existing Habit')
    print('3 - Calculate Averages')
    print('4 - Calculate Goal Progress')
    print('5 - Create Graphs')
    print('0 - Quit')
    print()



# below this is the main function and the if __name__ == "__main__" conditional

def main():
    WIDTH = 30
    welcome(WIDTH)
    show_menu = True
    while True:
        if show_menu:
            main_menu(WIDTH)
        user_choice = input('Enter the number of your choice: ')
        print()
        show_menu = True
        if user_choice == '1':
            new_habit()
        elif user_choice == '2':
            track_habit()
        elif user_choice == '3':
            calculate_avg()
        elif user_choice == '4':
            goal_progress()
        elif user_choice == '5':
            create_graph()
        elif user_choice == '0':
            print('See you tomorrow!')
            print()
            break
        else:
            print('Invalid input. Please enter one of the above numbers.')
            print()
            show_menu = False



if __name__ == "__main__":
    main()
