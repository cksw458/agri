import streamlit as st
import controllers as c
import views.sidebar as vsidebar


def page():
    if c.session.is_login():
        st.switch_page("index.py")

    st.set_page_config(
        page_title="登录",
        page_icon="🔑",
    )

    vsidebar.head_login()

    with st.form(key="login"):
        st.write("#### 农业商品信息管理系统 - 登录")
        username = st.text_input("用户名", type="default")
        password = st.text_input("密码", type="password")
        submit = st.form_submit_button("登录")

        if submit:
            try:
                c.session.login(username, password)
                st.switch_page("index.py")
            except c.CError as e:
                st.error(str(e))


if __name__ == "__main__":
    page()
