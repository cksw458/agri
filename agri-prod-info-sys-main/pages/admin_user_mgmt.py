import streamlit as st
import controllers as c
import infra as i
from models import MUser
import views as views
import views.sidebar as vsidebar
from streamlit_modal import Modal


def page():
    i.check_login()

    st.set_page_config(
        page_title="会员管理",
        page_icon="👥",
    )

    vsidebar.head()
    i.check_admin()

    st.write("## 管理员-会员管理")

    with st.container(border=True):

        col_username, col_date_joined, col_is_admin, col_action = st.columns(4)
        col_username.write("用户名")
        col_date_joined.write("注册时间")
        col_is_admin.write("是否管理员")
        col_action.write("操作")
        for user in c.dbsession.query(MUser).all():
            col_username.write(user.username)
            col_date_joined.write(user.date_joined)
            col_is_admin.write("是" if user.is_admin else "否")
            modal_edit_user = Modal("编辑用户", key=f"modal_edit_user_{user.id}")
            if col_action.button("编辑", key=f"edit_{user.id}"):
                modal_edit_user.open()
            if modal_edit_user.is_open():
                with modal_edit_user.container():
                    new_username = st.text_input("新用户名", user.username)
                    is_admin = st.checkbox("是否管理员", user.is_admin)
                    if st.button("确认修改"):
                        user.username = new_username
                        user.is_admin = is_admin
                        try:
                            c.dbsession.commit()
                            modal_edit_user.close()
                        except Exception:
                            c.dbsession.rollback()
                            st.error("修改失败")
                    if st.button("取消"):
                        modal_edit_user.close()
                    if st.button("删除用户", key=f"delete_{user.id}", type="primary"):
                        try:
                            c.dbsession.delete(user)
                            c.dbsession.commit()
                            modal_edit_user.close()
                        except Exception:
                            c.dbsession.rollback()
                            st.error("删除失败")

    vsidebar.footer()


if __name__ == "__main__":
    page()
