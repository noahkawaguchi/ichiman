import streamlit as st

import scripts.menu_options as modes


def main():
    st.set_page_config(
        page_title='ICHIMAN | duration-based habit tracker',
        page_icon='⏱️',
        layout='wide',
        )

    c1, c2 = st.columns([2, 1])
    with c1:
        st.title('ichiman')
        '[ee-chee-mon]　*noun*'
        st.caption('1. the number ten thousand in Japanese\n'
                   '2. a duration-based habit tracking web app')
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
        '### Welcome — try out any of the modes above'
        'or...'
        st.write('##### [Check out this project on GitHub]'
                 '(https://github.com/noahkawaguchi/ichiman)')

    elif mode == 'Start a new habit':
        modes.new_habit()
    
    elif mode == 'Track an existing habit':
        modes.track_habit()

    elif mode == 'Preview data features using test data':
        modes.data_preview()

    st.divider()
    st.caption('© 2024. All rights reserved.')

if __name__ == "__main__":
    main()
