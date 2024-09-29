import os

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm

from config import Lang
from scripts.i18n import get_translation as gt
from scripts.i18n import localize_ConciseDateFormatter

def daily_averages(df: pd.DataFrame) -> None:
    """Display average time spent per day.
    Overall - if there are at least 2 days.
    Last 7 days - if there are over 7 days.
    Last 30 days - if there are over 30 days.
    """
    st.write(gt('avg.heading', Lang.lang))
    if len(df) < 2:
        st.write(gt('avg.not_enough', Lang.lang))
    else:
        avg_duration = df['duration'].mean()
        st.write(gt('avg.overall', Lang.lang).format(
            len(df),
            avg_duration.components.hours,
            avg_duration.components.minutes,
            ))
    if len(df) > 7:
        last7 = df.tail(7)
        last7avg = last7['duration'].mean()
        st.write(gt('avg.last7', Lang.lang).format(
            last7avg.components.hours,
            last7avg.components.minutes,
            ))
    if len(df) > 30:
        last30 = df.tail(30)
        last30avg = last30['duration'].mean()
        st.write(gt('avg.last30', Lang.lang).format(
            last30avg.components.hours,
            last30avg.components.minutes,
            ))

def goal_progress(df: pd.DataFrame) -> None:
    """Prompt the user to enter their goal number of hours. 
    Display information on how much they have already completed and 
    how far they have left to go.
    """
    st.write(gt('goal.heading', Lang.lang))

    # Get a positive integer goal from the user.
    user_goal = st.number_input(
        gt('goal.enter', Lang.lang),
        min_value=1,
        max_value=None,
        value=10000,
        step=1,
        format='%d',
    )

    # When the user clicks the Calculate button, as long as they 
    # haven't already completed their goal, display how far they've 
    # come and how far they have left to go.
    calculate = st.button(gt('goal.calculate', Lang.lang))
    if calculate:
        avg_duration = df['duration'].mean()
        time_completed = df['duration'].sum()
        total_hours = time_completed.total_seconds() / 3600
        if total_hours > user_goal:
            st.write(gt('goal.reached', Lang.lang))
        else:
            percent_complete = total_hours / user_goal * 100
            hours_remaining = user_goal - total_hours
            avg_hours = avg_duration.total_seconds() / 3600
            days_remaining = hours_remaining / avg_hours
            years_remaining = days_remaining / 365
            st.write(gt('goal.progress', Lang.lang).format(
                f'{total_hours:.1f}', f'{user_goal}',
                f'{percent_complete:.0f}', f'{avg_hours:.1f}',
                f'{days_remaining:.0f}', f'{years_remaining:.2f}',
                ))

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
        y_unit = gt('misc.minutes', Lang.lang)
    else:
        graph_df['duration'] = graph_df['duration'] / 60
        y_unit = gt('misc.hours', Lang.lang)

    # Resample the data by week and calculate the means for each week 
    # and month
    weekly_average = graph_df.resample('W').mean()
    monthly_average = graph_df.resample('ME').mean()

    if Lang.lang == 'ja':
        # Set up the pyplot font to properly display Japanese
        font_path = os.path.join('fonts', 'NotoSansJP-VariableFont_wght.ttf')
        if not os.path.exists(font_path):
            st.error('Font file not found:', font_path)
        else:
            font_prop = fm.FontProperties(fname=font_path)
            fm.fontManager.addfont(font_path)
            plt.rcParams['font.family'] = font_prop.get_name()
            plt.rcParams['font.weight'] = '400' # Regular
            plt.rcParams['axes.unicode_minus'] = False # Use ASCII minus

    # Set up the graph depending on the size of the data set
    plt.figure(figsize=(7,5), dpi=150)
    if len(graph_df) < 15:
        plt.plot(graph_df.index, graph_df['duration'], color='red', 
                 marker='o', label=gt('graph.daily', Lang.lang))
    elif len(graph_df) < 62:
        plt.scatter(graph_df.index, graph_df['duration'], color='blue',
                    marker='.', label=gt('graph.daily', Lang.lang))
        plt.plot(weekly_average.index, weekly_average['duration'], color='red', 
                 marker='o', label=gt('graph.weekly', Lang.lang))
    else:
        plt.scatter(graph_df.index, graph_df['duration'], color='gray',
                    marker='.', label=gt('graph.daily', Lang.lang))
        plt.plot(weekly_average.index, weekly_average['duration'],
                 color='blue', marker='.', linestyle='--',
                 label=gt('graph.weekly', Lang.lang))
        plt.plot(monthly_average.index, monthly_average['duration'], 
                 color='red', marker='o', label=gt('graph.monthly', Lang.lang))
    
    plt.title(gt('graph.title', Lang.lang))
    plt.xlabel(gt('graph.dates', Lang.lang))
    plt.ylabel(y_unit)

    # Use AutoDateLocator to automatically select appropriate date 
    # intervals
    locator = mdates.AutoDateLocator()
    plt.gca().xaxis.set_major_locator(locator)

    # Use ConciseDateFormatter to make the date labels more readable 
    # depending on the user's language
    formatter = mdates.ConciseDateFormatter(locator)
    formatter = localize_ConciseDateFormatter(formatter, Lang.lang)
    plt.gca().xaxis.set_major_formatter(formatter)
    
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
