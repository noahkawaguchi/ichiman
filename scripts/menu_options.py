import os
import datetime as dt
from glob import glob

import streamlit as st
import pandas as pd

from scripts.helpers import show_all_data_info, update_data, up_to_date_download
from scripts.i18n import get_translation as gt
from scripts.i18n import test_name_to_japanese
from config import Lang


def new_habit() -> None:
    """Prompt the user to start a new habit and record the duration for 
    today. Display data insights and a download option.
    """
    # Initialize a persistent session_state variable so the time entry 
    # interface can stay displayed
    if 'starting_new' not in st.session_state:
        st.session_state.starting_new = False

    st.write(gt('menu.new', Lang.lang))
    st.write(gt('menu.journey', Lang.lang))

    # The button clears other habits and displays the duration entry 
    # interface 
    start_button = st.button(
        gt('menu.letsgo', Lang.lang), 
        on_click=st.session_state.clear,
        )
    if start_button:
        st.session_state.starting_new = True

    st.divider()

    # Prompt the user to enter data for today
    if st.session_state.starting_new:
        today = dt.datetime.today().date()
        empty_df = pd.DataFrame(columns=['date', 'duration'])
        new_df = update_data(empty_df, today)

        # Display a download option and data insights
        if len(new_df) > 0:
            up_to_date_download(new_df)
            st.divider()
            show_all_data_info(new_df)

def track_habit() -> None:
    """Prompt the user to upload a CSV file previously created with 
    this site and update the duration data up to and including today.
    Display data insights and a download option.
    """
    # Show a basic file upload interface
    c1, c2 = st.columns([1,2])
    with c1:
        st.write(gt('menu.track', Lang.lang))
        st.write(gt('menu.nice2CU', Lang.lang))
    with c2:
        uploaded_file = st.file_uploader(
            gt('menu.uploadCSV', Lang.lang), 
            type='csv',
            on_change=lambda: st.session_state.clear()
            )
    
    st.divider()

    # Read in the user's CSV file
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Initialize session_state variables 
            if 'tracking_df' not in st.session_state:
                st.session_state.tracking_df = df.copy()

            # Ensure 'date' has datetime objects and 'duration' has 
            # timedelta objects
            st.session_state.tracking_df['date'] = (
                pd.to_datetime(st.session_state.tracking_df['date'])
                )
            st.session_state.tracking_df['duration'] = (
                pd.to_timedelta(st.session_state.tracking_df['duration'])
                )

            # Check if the data is up to date
            today = dt.datetime.today().date()
            latest_date = st.session_state.tracking_df['date'].iloc[-1].date()
            if latest_date < today:
                # Update the session_state DataFrame
                next_date = latest_date + dt.timedelta(days=1)
                st.session_state.tracking_df = (update_data(df, next_date))

            # Check again due to Streamlit's execution flow
            latest_date = st.session_state.tracking_df['date'].iloc[-1].date()
            if latest_date >= today:
                # Display a download option and data insights
                up_to_date_download(st.session_state.tracking_df)
                st.divider()
                show_all_data_info(st.session_state.tracking_df)

        except (ValueError, pd.errors.ParserError):
            st.error(gt('menu.upload_error', Lang.lang))

def data_preview() -> None:
    """Give the user the option of several test data sets. 
    Display insights for the selected data set.
    """
    # Get all the CSV filenames in the 'test_data' subdirectory and 
    # convert them to strings with spaces and no extension
    data_dir = os.path.join(os.getcwd(), 'test_data')
    csv_paths = glob(os.path.join(data_dir, '*.csv'))
    existing_CSVs = [os.path.basename(csv) for csv in csv_paths]
    def filename_to_test_name(filename: str) -> str:
        return filename.removesuffix('.csv').replace('_', ' ')
    existing_test_names = [
        filename_to_test_name(csv) for csv in existing_CSVs]

    # Convert test names to Japanese if necessary
    if Lang.lang == 'ja':
        existing_test_names = [
            test_name_to_japanese(tn) for tn in existing_test_names]

    # Let the user choose one of the sets of test data
    c1, c2 = st.columns([1,2])
    with c1:
        st.write(gt('menu.preview', Lang.lang))
    with c2:
        selected_test_data = st.selectbox(
            '<this is a hidden label>', 
            [gt('menu.choose', Lang.lang)] + existing_test_names,
            label_visibility='hidden'
            )
    
    st.divider()

    if selected_test_data != gt('menu.choose', Lang.lang):
        # Read in the CSV file corresponding to the chosen name and 
        # display data insights
        filename = existing_CSVs[
            existing_test_names.index(selected_test_data)]
        df = pd.read_csv('test_data/' + filename)
        show_all_data_info(df)
