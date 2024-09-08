import streamlit as st

import scripts.menu_options as modes
from scripts.i18n import get_translation as gt
from config import Lang


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
            Lang.lang = 'ja'
        else:
            Lang.lang = 'en'
    with c3:
        mode = st.radio(
            gt('main.select', Lang.lang),
            (gt('main.welcome', Lang.lang),
            gt('main.new', Lang.lang),
            gt('main.track', Lang.lang),
            gt('main.preview', Lang.lang),
            ),
        )

    st.divider()

    if mode == gt('main.welcome', Lang.lang):
        st.write(gt('main.welcome_try', Lang.lang))
        st.write(gt('main.github', Lang.lang))

    elif mode == gt('main.new', Lang.lang):
        modes.new_habit()
    
    elif mode == gt('main.track', Lang.lang):
        modes.track_habit()

    elif mode == gt('main.preview', Lang.lang):
        modes.data_preview()

    st.divider()
    st.caption('© 2024. All rights reserved.')

if __name__ == "__main__":
    main()
