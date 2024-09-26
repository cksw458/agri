import streamlit as st
import controllers as c
import views.sidebar as vsidebar
import infra.st_session_str as sss


def page():
    if c.session.is_login():
        st.switch_page("index.py")

    st.set_page_config(page_title="注册", page_icon="🔒")

    vsidebar.head_login()

    with st.form(key="login"):
        st.write("#### 农业商品信息管理系统 - 注册")
        username = st.text_input("用户名", type="default")
        password = st.text_input("密码", type="password")
        password2 = st.text_input("确认密码", type="password")
        if st.form_submit_button("注册并登录"):
            try:
                if password != password2:
                    raise c.CError("两次输入的密码不一致！")
                c.session.register(username, password)
                c.session.login(username, password)
                st.session_state[sss.after_register_celebrations] = True
                st.switch_page("index.py")
            except c.CError as e:
                st.error(str(e))


if __name__ == "__main__":
    page()
