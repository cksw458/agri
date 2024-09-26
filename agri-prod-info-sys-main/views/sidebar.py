import streamlit as st
import controllers as c
from views import *


def head():
    if st.sidebar.button("登出", type="primary"):
        c.session.logout()
        st.rerun()
    st.sidebar.write("")

    hello_world()
    st.sidebar.page_link("pages/README.py", label="😊 README")
    st.sidebar.page_link("index.py", label="🌾 主页")
    st.sidebar.page_link("pages/user_personal.py", label="🧑‍💼 个人中心")
    if c.session.user.is_admin():
        st.sidebar.page_link("pages/admin_user_mgmt.py", label="👥 管理员-会员管理")
        st.sidebar.page_link(
            "pages/admin_productInfo_mgmt.py", label="🛍️ 管理员-商品信息管理"
        )
        st.sidebar.page_link(
            "pages/admin_product_in_out_record.py", label="📦 管理员-商品出入库"
        )
    st.sidebar.write("")


def head_login():
    hello_world()
    st.sidebar.page_link("pages/user_login.py", label="🔑 登录")
    st.sidebar.page_link("pages/user_register.py", label="🔒 注册")


def footer():
    # st.sidebar
    # st.sidebar.markdown(
    #     """
    #     ---

    #     这里是页脚
    #     """
    # )
    pass
