def check_login():
    import controllers as c
    import streamlit as st

    if not c.session.is_login():
        st.switch_page("pages/user_login.py")


def check_admin():
    import controllers as c
    import streamlit as st

    if not c.session.user.is_admin():
        st.error("非管理員无法访问此页面")
        st.stop()
