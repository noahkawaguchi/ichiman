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
            gt('main.select', lang),
            (gt('main.welcome', lang),
            gt('main.new', lang),
            gt('main.track', lang),
            gt('main.preview', lang),
            ),
        )

    st.divider()

    if mode == gt('main.welcome', lang):
        st.write(gt('main.welcome_try', lang))
        st.write(gt('main.github', lang))

    elif mode == gt('main.new', lang):
        modes.new_habit()
    
    elif mode == gt('main.track', lang):
        modes.track_habit()

    elif mode == gt('main.preview', lang):
        modes.data_preview()

    st.divider()
    st.caption('© 2024. All rights reserved.')

if __name__ == "__main__":
    main()
