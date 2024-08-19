import streamlit as st

import scripts.menu_options as modes


st.set_page_config(
    page_title='ICHIMAN | duration-based habit tracker',
    page_icon='⏱️',
    layout='wide',
    )

c1, c2 = st.columns([2, 1])
with c1:
    st.title('ichiman')
    '[ee-chee-mon]　*noun*'
    st.caption('1. the number ten thousand in Japanese \n2. a duration-'
               'based habit tracker developed by Noah Kawaguchi')
with c2:
    mode = st.radio(
        'Select a mode to begin:',
        ('(welcome screen)',
         'Start a new habit',
         'Track an existing habit',
         'Preview data features using test data',
         ),
    )

st.divider()

if mode == '(welcome screen)':
    '#### Welcome — try out any of the modes above'
    'or...'
    '###### [Read more on GitHub](https://github.com/noahkawaguchi/ichiman)'
    '###### [Contact me through my website](https://www.noahkawaguchi.com/)'

elif mode == 'Start a new habit':
    modes.new_habit()
   
elif mode == 'Track an existing habit':
    modes.track_habit()

elif mode == 'Preview data features using test data':
    modes.data_preview()

st.divider()
st.caption('Copyright © 2024 Noah Kawaguchi. All rights reserved.')
