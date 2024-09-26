import streamlit as st
import controllers as c
import infra.st_session_str as sss


def hello_world():
    # st.sidebar.page_link("pages/demo_hello_world.py", label="🌎 Hello, world!")
    pass


def after_register_celebrations():
    """注册后的庆祝"""

    if sss.after_register_celebrations not in st.session_state:
        return

    st.session_state.pop(sss.after_register_celebrations)
    st.balloons()
    st.toast("🎉 恭喜您注册成功！")
