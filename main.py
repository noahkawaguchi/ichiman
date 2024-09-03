import streamlit as st

import scripts.menu_options as modes
from scripts.i18n import get_translation as gt


def main():
    st.set_page_config(
        page_title='ICHIMAN | duration-based habit tracker',
        page_icon='⏱️',
        layout='wide',
        )

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.title('ichiman')
        '[ee-chee-mon]　*noun*'
        st.caption('1. the number ten thousand in Japanese\n'
                   '2. a duration-based habit tracking web app')
    with c2:
        lang_selection = st.radio('Language / 言語', ('English', '日本語'))
        if lang_selection == '日本語':
            lang = 'ja'
        else:
            lang = 'en'
    with c3:
        mode = st.radio(
            gt('select mode', lang),
            (gt('welcome screen', lang),
            gt('start new', lang),
            gt('track existing', lang),
            gt('data preview', lang),
            ),
        )

    st.divider()

    if mode == gt('welcome screen', lang):
        '### Welcome — try out any of the modes above'
        'or...'
        st.write('##### [Check out this project on GitHub]'
                 '(https://github.com/noahkawaguchi/ichiman)')

    elif mode == gt('start new', lang):
        modes.new_habit()
    
    elif mode == gt('track existing', lang):
        modes.track_habit()

    elif mode == gt('data preview', lang):
        modes.data_preview()

    st.divider()
    st.caption('© 2024. All rights reserved.')

if __name__ == "__main__":
    main()
