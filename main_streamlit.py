import os
from glob import glob

import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')
st.title('ICHIMAN')
st.write('###### *a duration-based habit tracker developed by Noah Kawaguchi*')
st.divider()

data_dir = os.path.join(os.getcwd(), 'data')
csv_paths = glob(os.path.join(data_dir, '*.csv'))
existing_CSVs = [os.path.basename(csv) for csv in csv_paths]

def filename_to_habit_name(filename: str) -> str:
    return filename.removesuffix('.csv').replace('_', ' ')
existing_habit_names = [filename_to_habit_name(csv) for csv in existing_CSVs]

c1, c2, c3 = st.columns(3)
type_of_data = 'no data'
file_to_use = 'no file'

def clear_test_file():
    selected_test_data = None

with c1:
    st.write('#### Start a new habit')
    new_habit_name = st.text_input('Enter the name of the habit here:')
    if new_habit_name:
        st.write(f'New habit: {new_habit_name}!')
        type_of_data = 'new'
        file_to_use = 'PUT THE NAME OF THE NEW FILE HERE'
        clear_test_file()

with c2:
    st.write('#### Track an existing habit')
    uploaded_file = st.file_uploader(
        'Upload a CSV file previously created with this app:', 
        type='csv',
        )
    if uploaded_file is not None:
        st.write('We have a file!')
        type_of_data = 'upload'
        file_to_use = 'PUT THE NAME OF THE EXISTING FILE HERE'

with c3:
    st.write('#### Preview app features using test data')
    selected_test_data = st.selectbox(
        'short, medium, or long term', 
        ['(choose one)'] + existing_habit_names,
        )
    if selected_test_data != '(choose one)':
        st.write('You selected', selected_test_data)
        type_of_data = 'test'
        file_to_use = selected_test_data


st.divider()

st.write('Type of data:', type_of_data)
st.write('Current file:', file_to_use)

if type_of_data == 'test':
    filename = selected_test_data.replace(' ', '_') + '.csv'
    df = pd.read_csv('data/' + filename)
    df.set_index('date', inplace=True)

    df['duration'] = pd.to_timedelta(df['duration'])

    c1, c2 = st.columns([1, 2])
    with c1:
        st.write('#### Daily averages')        
        if len(df) < 2:
            st.write(("Not enough data for averages. Check back once "
                      "you've recorded more days."))
        else:
            avg_duration = df['duration'].mean()
            avg_duration_str = f"{avg_duration.components.hours} hours, {avg_duration.components.minutes} minutes"
            st.write(f'Overall average ({len(df)} days):', avg_duration_str)
        if len(df) > 7:
            last7 = df.tail(7)
            last7avg = last7['duration'].mean()
            last7avg_str = f"{last7avg.components.hours} hours, {last7avg.components.minutes} minutes"
            st.write(f'Average for the last 7 days:', last7avg_str)
        if len(df) > 30:
            last30 = df.tail(30)
            last30avg = last30['duration'].mean()
            last30avg_str = f"{last30avg.components.hours} hours, {last30avg.components.minutes} minutes"
            st.write(f'Average for the last 30 days:', last30avg_str)
        
        st.divider()
        st.write('#### Progress toward goal')
        user_goal = st.number_input(
            'Enter your goal in hours (type or use − +):',
            min_value=1,
            max_value=None,
            value=10000,
            step=1,
            format='%d',
        )
        calculate = st.button('Calculate')
        if calculate:
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
                st.write((f'You have completed {total_hours:.1f} out of {user_goal} '
            f'hours, or {percent_complete:.0f} percent. If you maintain '
            f'your average so far of {avg_hours:.1f} hours per day, it '
            f'will take {days_remaining:.0f} more days, or '
            f'{years_remaining:.2f} years, to reach your goal.'))






    # with c2:
        # st.line_chart(df)
    
    st.divider()
    st.dataframe(df)
