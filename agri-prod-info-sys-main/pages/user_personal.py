import streamlit as st
import controllers as c
import infra as i
import views as views
import views.sidebar as vsidebar
from streamlit_modal import Modal


def page():
    i.check_login()

    st.set_page_config(
        page_title="个人中心",
        page_icon="🧑‍💼",
    )

    vsidebar.head()

    modal_change_username = Modal("修改用户名", key="modal_change_username")
    modal_change_password = Modal("修改密码", key="modal_change_password")

    st.write("## 个人中心")
    st.write("### 用户信息")

    st.write("注册时间：", c.session.user.get_register_time())
    st.write(
        "用户名：",
        c.session.user.get_usernames(),
        "`管理员`" if c.session.user.is_admin() else "",
    )

    if st.button("修改用户名"):
        modal_change_username.open()
    if modal_change_username.is_open():
        with modal_change_username.container():
            new_username = st.text_input("新用户名", c.session.user.get_usernames())
            if st.button("确认修改"):
                try:
                    c.session.user.set_usernames(new_username)
                    modal_change_username.close()
                except c.CError as e:
                    st.error(e)
            if st.button("取消"):
                modal_change_username.close()

    if st.button("修改密码"):
        modal_change_password.open()
    if modal_change_password.is_open():
        with modal_change_password.container():
            old_password = st.text_input("原密码", type="password")
            new_password = st.text_input("新密码", type="password")
            new_password2 = st.text_input("确认密码", type="password")
            if st.button("确认修改"):
                try:
                    if new_password != new_password2:
                        raise c.CError("新密码两次输入不一致！")
                    c.session.user.set_password(old_password, new_password)
                    modal_change_password.close()
                except c.CError as e:
                    st.error(e)
            if st.button("取消"):
                modal_change_password.close()

    vsidebar.footer()


if __name__ == "__main__":
    page()
