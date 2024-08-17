import datetime as dt

import streamlit as st
import pandas as pd

from . import data_insights as data

def show_all_data_info(df: pd.DataFrame) -> None:
    
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

def update_data(df: pd.DataFrame) -> pd.DataFrame:
    
    # Initialize a session_state DataFrame (so it will persist accross
    # reruns of the page)
    if 'new_df' not in st.session_state:
        st.session_state.new_df = df.copy()

    # Ensure the 'date' column is of datetime type and the 
    # 'duration' column of timedelta type
    st.session_state.new_df['date'] = pd.to_datetime(st.session_state.new_df['date'])
    st.session_state.new_df['duration'] = pd.to_timedelta(st.session_state.new_df['duration'])

    # Check if the data is up to date (This is the only return 
    # statement and will eventually return the updated data)
    latest_date = st.session_state.new_df['date'].iloc[-1].date()
    today = dt.datetime.today().date()
    if latest_date >= today:
        def format_timedelta(td):
            return f'{td.components.hours:02}:{td.components.minutes:02}:{td.components.seconds:02}'
        remove_days = st.session_state.new_df.copy()
        remove_days['duration'] = (remove_days['duration']
                                   .apply(format_timedelta))
        csv = remove_days.to_csv(index=False)
        c1, c2 = st.columns(2)
        with c1:
            st.write(f'#### This data is up to date! ({today.strftime('%B %e')})')
        with c2:
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='tracked_habit.csv',
                mime='text/csv',
                )
            st.write("(Unfortunately, I can't store everyone's data, "
                     "so this is currently the only way to save your "
                     "progress between visits to this site. )")
        return st.session_state.new_df
    else:
        st.write('#### This data is not up to date')
        if 'today_reached' not in st.session_state:
            st.session_state.today_reached = False

        if 'next_day' not in st.session_state:
            st.session_state.next_day = latest_date + dt.timedelta(days=1)

        if not st.session_state.today_reached:
            if today in st.session_state.new_df['date'].values:
                st.session_state.today_reached = True
            
            formatted_date = st.session_state.next_day.strftime('%a, %b %e, %Y')
            st.write(f'Enter the amount of time for {formatted_date}:')
            new_duration = None
            c1, c2, c3 = st.columns([2,2,1])
            with c1:
                new_duration_hours = st.number_input(
                    'Hours (type or use − +):',
                    min_value=0,
                    max_value=23,
                    value=0,
                    step=1,
                    format='%d',
                )
            with c2:
                    new_duration_minutes = st.number_input(
                    'Minutes (type or use − +):',
                    min_value=0,
                    max_value=59,
                    value=0,
                    step=1,
                    format='%d',
                )
            with c3:
                st.write('')
                st.write('')
                c1, c2 = st.columns(2)
                with c1:
                    save_button = st.button('Save')
                    if save_button:
                        new_duration = dt.timedelta(
                            hours=new_duration_hours, 
                            minutes=new_duration_minutes,
                            )
                with c2: 
                    st.button('Next')

            if new_duration is not None:
                new_row = pd.DataFrame({'date': [st.session_state.next_day], 
                                        'duration': [new_duration]})
                new_row['date'] = pd.to_datetime(new_row['date'])
                st.session_state.new_df = pd.concat([st.session_state.new_df, new_row], ignore_index=True)
                st.write(formatted_date, 'updated!')
                st.session_state.next_day += dt.timedelta(days=1)


            reversed_df = st.session_state.new_df.iloc[::-1]
            data.display_data(reversed_df)
