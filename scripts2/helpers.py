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
