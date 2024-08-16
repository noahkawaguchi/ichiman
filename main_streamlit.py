import os
from glob import glob

import streamlit as st
import pandas as pd

import scripts2.data_insights as data

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
        if uploaded_file is not None:
            st.write('We have a file!')
        

elif mode == 'Preview app features using test data':
    data_dir = os.path.join(os.getcwd(), 'data')
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
        filename = selected_test_data.replace(' ', '_') + '.csv'
        df = pd.read_csv('data/' + filename)

        # Ensure the 'date' column is of datetime type and the 
        # 'duration' column of timedelta type.
        df['date'] = pd.to_datetime(df['date'])
        df['duration'] = pd.to_timedelta(df['duration'])

        c1, c2 = st.columns([1, 2])
        with c1:
            st.write('#### Daily averages')
            data.daily_averages(df)
            st.divider()
            st.write('#### Progress toward goal')
            data.goal_progress(df)
            st.divider()
        with c2:
            data.graph_data(df)
        st.divider()
        with st.expander('Show all days'):
            data.display_data(df)

