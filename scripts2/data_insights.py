import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def daily_averages(df: pd.DataFrame) -> None:
    """Display average time spent per day.
    Overall - if there are at least 2 days.
    Last 7 days - if there are over 7 days.
    Last 30 days - if there are over 30 days.
    """
    if len(df) < 2:
        st.write(("Not enough data for averages. Check back once "
                "you've recorded more days."))
    else:
        avg_duration = df['duration'].mean()
        avg_duration_str = (f'{avg_duration.components.hours} hr '
                            f'{avg_duration.components.minutes} min')
        st.write(f'Overall average ({len(df)} days):', avg_duration_str)
    if len(df) > 7:
        last7 = df.tail(7)
        last7avg = last7['duration'].mean()
        last7avg_str = (f'{last7avg.components.hours} hr '
                        f'{last7avg.components.minutes} min')
        st.write(f'Average for the last 7 recorded days:', last7avg_str)
    if len(df) > 30:
        last30 = df.tail(30)
        last30avg = last30['duration'].mean()
        last30avg_str = (f'{last30avg.components.hours} hr '
                         f'{last30avg.components.minutes} min')
        st.write(f'Average for the last 30 recorded days:', last30avg_str)

def goal_progress(df: pd.DataFrame) -> None:
    """Prompt the user to enter their goal number of hours. 
    Display information on how much they have already completed and 
    how far they have left to go.
    """
    # Get a positive integer goal from the user.
    user_goal = st.number_input(
        'Enter your goal in hours (type or use − +):',
        min_value=1,
        max_value=None,
        value=10000,
        step=1,
        format='%d',
    )

    # When the user clicks the Calculate button, as long as they 
    # haven't already completed their goal, display how far they've 
    # come and how far they have left to go.
    calculate = st.button('Calculate')
    if calculate:
        avg_duration = df['duration'].mean()
        time_completed = df['duration'].sum()
        total_hours = time_completed.total_seconds() / 3600
        if total_hours > user_goal:
            st.write("You've already reached your goal. Congrats!")
        else:
            percent_complete = total_hours / user_goal * 100
            hours_remaining = user_goal - total_hours
            avg_hours = avg_duration.total_seconds() / 3600
            days_remaining = hours_remaining / avg_hours
            years_remaining = days_remaining / 365
            st.write((f'You have completed {total_hours:.1f} out of '
                      f'{user_goal} hours, or {percent_complete:.0f} '
                      'percent. If you maintain your average so far of '
                      f'{avg_hours:.1f} hours per day, it will take '
                      f'{days_remaining:.0f} more days, or '
                      f'{years_remaining:.2f} years, to reach your '
                      'goal.'))

def graph_data(df: pd.DataFrame) -> None:
    """Display a graph of the data.
    Daily data - for any number of days.
    Weekly averages - if there are at least 15 days.
    Monthly averages - if there are at lease 62 days.
    """
    graph_df = df.copy()

    # Set the 'date' column as the index
    graph_df.set_index('date', inplace=True)

    # Convert the 'duration' column to minutes if under 2 hours or 
    # hours otherwise
    graph_df['duration'] = graph_df['duration'].dt.total_seconds() / 60
    if max(graph_df['duration']) <= 120:
        y_unit = 'Minutes'
    else:
        graph_df['duration'] = graph_df['duration'] / 60
        y_unit = 'Hours'


    # Resample the data by week and calculate the means for each week 
    # and month
    weekly_average = graph_df.resample('W').mean()
    monthly_average = graph_df.resample('ME').mean()

    # Set up the graph depending on the size of the data set
    plt.figure(figsize=(7,5), dpi=150)
    if len(graph_df) < 15:
        plt.plot(graph_df.index, graph_df['duration'], color='red', marker='o', label='Daily Data')
    elif len(graph_df) < 62:
        plt.scatter(graph_df.index, graph_df['duration'], color='blue', marker='.', label='Daily Data')
        plt.plot(weekly_average.index, weekly_average['duration'], color='red', 
                 marker='o', label='Weekly Averages')
    else:
        plt.scatter(graph_df.index, graph_df['duration'], color='gray', marker='.', label='Daily Data')
        plt.plot(weekly_average.index, weekly_average['duration'], color='blue', 
                 marker='.', linestyle='--', label='Weekly Averages')
        plt.plot(monthly_average.index, monthly_average['duration'], 
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
    st.pyplot(plt)

def display_data(df: pd.DataFrame) -> None:
    """Display a DataFrame using human-readable dates and durations."""
    format_df = df.copy()
    format_df['date'] = format_df['date'].dt.strftime('%a, %b %e, %Y')

    # Show in minutes if the max is 2 hours or under, otherwise show in 
    # hours
    format_df['duration'] = format_df['duration'].dt.total_seconds() / 60
    if max(format_df['duration']) <= 120:
        format_df = format_df.rename(columns={'duration': 'minutes'})
    else:
        format_df['duration'] = format_df['duration'] / 60
        format_df['duration'] = format_df['duration'].round(1)
        format_df = format_df.rename(columns={'duration': 'hours'})
    
    st.dataframe(format_df, use_container_width=True)
