import os
from glob import glob

import streamlit as st
import pandas as pd

from scripts2.helpers import show_all_data_info, update_data

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
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write('### Start a new habit')
        st.write('A journey of ten thousand hours begins with a single day.')
    with c2:
        new_habit_name = st.text_input('Enter the name of the habit here:')
        if new_habit_name:
            st.write('New habit:',new_habit_name)

elif mode == 'Track an existing habit':
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write('### Track an existing habit')
        st.write('Nice to see you again.')
    with c2:
        uploaded_file = st.file_uploader(
            'Upload a CSV file previously created with this app:', 
            type='csv',
            )
    st.divider()
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        updated_df = update_data(df)
        st.divider()
        if updated_df is None:
            show_all_data_info(df)
        else:
            show_all_data_info(updated_df)


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
