import os
import datetime as dt
from glob import glob

import streamlit as st
import pandas as pd

from scripts2.helpers import show_all_data_info, update_data, up_to_date_download, update_data2

st.set_page_config(
    page_title='ICHIMAN | duration-based habit tracker',
    page_icon='⏱️',
    layout='wide',
    )

c1, c2 = st.columns([2, 1])
with c1:
    st.title('ICHIMAN')
    st.write(('###### *a duration-based habit tracker developed by '
              'Noah Kawaguchi*'))
with c2:
    mode = st.radio(
        'Select a mode to begin:',
        ('(welcome screen)',
         'Start a new habit',
         'Track an existing habit',
         'Preview app features using test data',
         ),
    )

st.divider()

if mode == 'Start a new habit':

    # Initialize a persistent session_state variable so the time entry 
    # interface can stay displayed
    if 'starting_new' not in st.session_state:
        st.session_state.starting_new = False

    st.write('### Start a new habit')
    st.write('A journey of ten thousand hours begins with a single day.')

    # The button clears other habits and displays the duration entry 
    # interface 
    start_button = st.button(
        "Let's go!", 
        on_click=lambda: st.session_state.clear(),
        )
    if start_button:
        st.session_state.starting_new = True

    st.divider()

    # Prompt the user to enter data for today
    if st.session_state.starting_new:
        today = dt.datetime.today().date()
        empty_df = pd.DataFrame(columns=['date', 'duration'])
        new_df, up_to_date = update_data2(empty_df, today)

        # Display a download option and data insights
        if up_to_date:
            up_to_date_download(new_df)
            st.divider()
            show_all_data_info(new_df)

elif mode == 'Track an existing habit':
    
    # Show a basic file upload interface
    c1, c2 = st.columns([1,2])
    with c1:
        st.write('### Track an existing habit')
        st.write('Nice to see you again.')
    with c2:
        uploaded_file = st.file_uploader(
            'Upload a CSV file previously created with this app:', 
            type='csv',
            on_change=lambda: st.session_state.clear()
            )
    
    st.divider()

    # Read in the user's CSV file
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Initialize session_state variables 
        if 'tracking_df' not in st.session_state:
            st.session_state.tracking_df = df.copy()
        if 'up_to_date' not in st.session_state:
            st.session_state.up_to_date = False

        # Ensure 'date' has datetime objects and 'duration' has 
        # timedelta objects
        st.session_state.tracking_df['date'] = (
            pd.to_datetime(st.session_state.tracking_df['date'])
            )
        st.session_state.tracking_df['duration'] = (
            pd.to_timedelta(st.session_state.tracking_df['duration'])
            )

        # Check if the data is up to date
        latest_date = st.session_state.tracking_df['date'].iloc[-1].date()
        today = dt.datetime.today().date()
        if latest_date < today:
            # Update the session_state DataFrame
            next_date = latest_date + dt.timedelta(days=1)
            st.session_state.tracking_df, st.session_state.up_to_date = (
                update_data2(df, next_date)
                )
        else:
            st.session_state.up_to_date = True
        
        # Once the data is up to date show the download option and the 
        # data insights.
        if st.session_state.up_to_date:
            up_to_date_download(st.session_state.tracking_df)
            st.divider()
            show_all_data_info(st.session_state.tracking_df)

elif mode == 'Preview app features using test data':
    # Get all the CSV filenames in the 'test_data' subdirectory and 
    # convert them to strings with spaces and no extension
    data_dir = os.path.join(os.getcwd(), 'test_data')
    csv_paths = glob(os.path.join(data_dir, '*.csv'))
    existing_CSVs = [os.path.basename(csv) for csv in csv_paths]
    def filename_to_habit_name(filename: str) -> str:
        return filename.removesuffix('.csv').replace('_', ' ')
    existing_habit_names = [filename_to_habit_name(csv) for csv in existing_CSVs]

    c1, c2 = st.columns([1,2])
    with c1:
        st.write('### Preview app features using test data')
    with c2:
        selected_test_data = st.selectbox(
            'short, medium, or long term', 
            ['(choose one)'] + existing_habit_names,
            )
    
    st.divider()

    if selected_test_data != '(choose one)':
        # Read in the CSV file corresponding to the chosen name
        filename = selected_test_data.replace(' ', '_') + '.csv'
        df = pd.read_csv('test_data/' + filename)

        show_all_data_info(df)
