import controllers as c
import streamlit as st
import views.sidebar as vsidebar


def page():
    st.set_page_config(
        page_title="Hello, world!",
        page_icon="🌎",
    )

    if c.session.is_login():
        vsidebar.head()
    else:
        vsidebar.head_login()
    """
    # Hello, world!

    演示页面
    """

    # f"""
    # ## Session State

    # """

    # st.write(st.session_state)

    # """## debug"""

    # st.write("c.session.is_login()-->", c.session.is_login())

    # if c.session.is_login():
    #     vsidebar.footer()


if __name__ == "__main__":
    page()
