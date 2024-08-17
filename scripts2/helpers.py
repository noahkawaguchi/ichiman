import datetime as dt
from  typing import Tuple
from time import sleep

import streamlit as st
import pandas as pd

from . import data_insights as data

def show_all_data_info(df: pd.DataFrame) -> None:
    """Display averages, goal progress, and a graph of the data."""

    df_copy = df.copy()

    # Ensure the 'date' column is of datetime type and the 
    # 'duration' column of timedelta type
    df_copy['date'] = pd.to_datetime(df_copy['date'])
    df_copy['duration'] = pd.to_timedelta(df_copy['duration'])

    c1, c2 = st.columns([1, 2])
    with c1:
        st.write('#### Daily averages')
        data.daily_averages(df_copy)
        st.divider()
        st.write('#### Progress toward goal')
        data.goal_progress(df_copy)
        st.divider()
    with c2:
        data.graph_data(df_copy)
    st.divider()
    with st.expander('Show all days'):
        data.display_data(df_copy)

def update_data2(
        df: pd.DataFrame, date_cursor: dt.date
        ) -> Tuple[pd.DataFrame, bool]:
    """Given the currently recorded dates and durations, prompt 
    the user to enter data for each day up to the present day. 
    With each iteration, return the data and a boolean of whether or 
    not the data is fully up to date. (This complexity is necessary 
    because of Streamlit's repeated top-down execution.)
    """
    # Initialize session_state variables for the parameters
    if 'new_df' not in st.session_state:
        st.session_state.new_df = df.copy()
    if 'date_cursor' not in st.session_state:
        st.session_state.date_cursor = date_cursor

    # Ensure the 'date' column is of datetime type and the 
    # 'duration' column of timedelta type
    st.session_state.new_df['date'] = pd.to_datetime(st.session_state.new_df['date'])
    st.session_state.new_df['duration'] = pd.to_timedelta(st.session_state.new_df['duration'])

    # Check if the data needs to be updated
    today = dt.datetime.today().date()
    if st.session_state.date_cursor > today:
        up_to_date = True
        return st.session_state.new_df, up_to_date
    else:
        st.write('### Enter time spent:')

        # Collect the hours and minutes from the user for the date in 
        # question
        c1, c2 = st.columns(2)
        with c1:
            new_duration_hours = st.number_input(
                'Hours (type or use − +):',
                min_value=0,
                max_value=23,
                value=0,
                step=1,
                format='%d',
                label_visibility='collapsed'
            )
        with c2:
            st.write('##### hour(s) and')
        c1, c2 = st.columns(2)
        with c1:
            new_duration_minutes = st.number_input(
                'Minutes (type or use − +):',
                min_value=0,
                max_value=59,
                value=0,
                step=1,
                format='%d',
                label_visibility='collapsed'
            )
        with c2:
            st.write('##### minute(s)')

        # Convert the user's input into a DataFrame
        new_duration = dt.timedelta(hours=new_duration_hours,
                                    minutes=new_duration_minutes)
        new_row = pd.DataFrame({'date': [st.session_state.date_cursor], 'duration': [new_duration]})
        new_row['date'] = pd.to_datetime(new_row['date'])

        # When the user presses save, save the data to the 
        # session_state DataFrame
        c1, c2 = st.columns(2)
        with c1:
            save_button = st.button('Save')
        if save_button:
            st.session_state.new_df = pd.concat(
                [st.session_state.new_df, new_row], 
                ignore_index=True,
                )

            # Temporarily display a confirmation message that the data 
            # for the given day has been saved
            short_date = st.session_state.date_cursor.strftime('%b %e')
            placeholder = st.empty()
            placeholder.text(f'{short_date} updated!')
            sleep(1.75)
            placeholder.empty()

            # Point to the following day
            st.session_state.date_cursor += dt.timedelta(days=1)

        # Display the date for which the user should enter data. (This 
        # has to be placed here in the code so that it will reflect the 
        # correct day as soon as it updates.)
        with c2:
            if st.session_state.date_cursor <= today:
                formatted_date = st.session_state.date_cursor.strftime('%a, %b %e, %Y')
                st.write(f'##### for {formatted_date}')

        # While the data is not yet up to date, show the latest data 
        # being updated
        if st.session_state.date_cursor <= today:
            if len(st.session_state.new_df) > 0:
                st.divider()
                reversed_df = st.session_state.new_df.iloc[::-1]
                data.display_data(reversed_df)

        # Once the data is up to date, show a button to end data entry 
        else:
            st.write('All up to date!')
            done_button = st.button('See results')
            if done_button:
                up_to_date = True
                return st.session_state.new_df, up_to_date
        
        # This is here because the caller function needs to repeatedly 
        # get valid return values even before any user input.
        up_to_date = False
        return st.session_state.new_df, up_to_date


# Get rid of this one soon
def update_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, bool]:
    """Given the currently recorded dates and durations, prompt 
    the user to enter data for each day up to the present day. 
    With each iteration, return the data and a boolean of whether or 
    not the data is fully up to date. (This complexity is necessary 
    because of Streamlit's repeated top-down execution.)
    """
    # Initialize a session_state DataFrame (so it will persist accross
    # reruns of the page)
    if 'new_df' not in st.session_state:
        st.session_state.new_df = df.copy()

    # Ensure the 'date' column is of datetime type and the 
    # 'duration' column of timedelta type
    st.session_state.new_df['date'] = pd.to_datetime(st.session_state.new_df['date'])
    st.session_state.new_df['duration'] = pd.to_timedelta(st.session_state.new_df['duration'])

    # Check if the data needs to be updated
    today = dt.datetime.today().date()
    latest_date = st.session_state.new_df['date'].iloc[-1].date()
    if latest_date >= today:
        up_to_date = True
        return st.session_state.new_df, up_to_date
    else:
        st.write('### Update data:')
        
        # Initialize a session_state variable for the next day to be 
        # pointed at
        if 'next_day' not in st.session_state:
            st.session_state.next_day = latest_date + dt.timedelta(days=1)
            st.session_state.formatted_date = st.session_state.next_day.strftime('%a, %b %e, %Y')

        # Collect the hours and minutes from the user for the date in 
        # question
        c1, c2 = st.columns(2)
        with c1:
            new_duration_hours = st.number_input(
                'Hours (type or use − +):',
                min_value=0,
                max_value=23,
                value=0,
                step=1,
                format='%d',
                label_visibility='collapsed'
            )
        with c2:
            st.write('##### hour(s) and')
        c1, c2 = st.columns(2)
        with c1:
            new_duration_minutes = st.number_input(
                'Minutes (type or use − +):',
                min_value=0,
                max_value=59,
                value=0,
                step=1,
                format='%d',
                label_visibility='collapsed'
            )
        with c2:
            st.write('##### minute(s)')

        # Convert the user's input into a DataFrame
        new_duration = dt.timedelta(hours=new_duration_hours,
                                    minutes=new_duration_minutes)
        new_row = pd.DataFrame({'date': [st.session_state.next_day], 'duration': [new_duration]})
        new_row['date'] = pd.to_datetime(new_row['date'])

        # When the user presses save, save the data to the 
        # session_state DataFrame
        c1, c2 = st.columns(2)
        with c1:
            save_button = st.button('Save')
        if save_button:
            st.session_state.new_df = pd.concat(
                [st.session_state.new_df, new_row], 
                ignore_index=True,
                )

            # Temporarily display a confirmation message that the data 
            # for the given day has been saved
            short_date = st.session_state.next_day.strftime('%b %e')
            placeholder = st.empty()
            placeholder.text(f'{short_date} updated!')
            sleep(1.75)
            placeholder.empty()

            # Point to the following day
            st.session_state.next_day += dt.timedelta(days=1)

        # Display the date for which the user should enter data. (This 
        # has to be placed here in the code so that it will reflect the 
        # correct day as soon as it updates.)
        with c2:
            if st.session_state.new_df['date'].iloc[-1].date() < today:
                st.session_state.formatted_date = st.session_state.next_day.strftime('%a, %b %e, %Y')
                st.write(f'##### for {st.session_state.formatted_date}')

        # While the data is not yet up to date, show the latest data 
        # being updated
        if st.session_state.new_df['date'].iloc[-1].date() < today:
            st.divider()
            reversed_df = st.session_state.new_df.iloc[::-1]
            data.display_data(reversed_df)

        # Once the data is up to date, show a button to end data entry 
        else:
            st.write('All up to date!')
            done_button = st.button('See results')
            if done_button:
                up_to_date = True
                return st.session_state.new_df, up_to_date
        
        # This is here because the caller function needs to repeatedly 
        # get valid return values even before any user input.
        up_to_date = False
        return st.session_state.new_df, up_to_date

def up_to_date_download(df: pd.DataFrame) -> None:
    """Display the updated status of the data.
    Format the DataFrame and create a CSV file.
    Display an interface to download the file.
    """
    # Copy the DataFrame and remove '0 days' from the 'duration' values
    remove_days = df.copy()
    def format_timedelta(td):
        return f'{td.components.hours:02}:{td.components.minutes:02}:{td.components.seconds:02}'
    remove_days['duration'] = (remove_days['duration']
                                .apply(format_timedelta))
    
    # Create a CSV file with the formatted data 
    csv = remove_days.to_csv(index=False)

    # Display the up-to-date status of the data
    c1, c2 = st.columns(2)
    with c1:
        earliest_date = df['date'].iloc[0].date().strftime('%a, %b %e, %Y')
        latest_date = df['date'].iloc[-1].date().strftime('%a, %b %e, %Y')
        st.write(f'#### This data is up to date from {earliest_date} to {latest_date}')
        if earliest_date == latest_date:
            st.write("(You only have one day's worth of data)")

    # Display a basic interface to download the CSV file 
    with c2:
        c1, c2 = st.columns(2)
        with c1:
            download_filename = st.text_input(
                'Name your file:',
                value='tracked_habit',
            )
            download_filename = download_filename.replace(' ', '_') + '.csv'
            st.download_button(
                label="Download (.csv)",
                data=csv,
                file_name=download_filename,
                mime='text/csv',
                )
        with c2:
            st.write("(Unfortunately, I can't store everyone's data, "
                    "so this is currently the only way to save your "
                     "progress between visits to this site. )")
