import streamlit as st
import infra as i
import views as views
import views.sidebar as vsidebar


def page():
    i.check_login()

    st.set_page_config(
        page_title="README",
        page_icon="😊",
    )

    views.after_register_celebrations()
    vsidebar.head()

    st.sidebar.success("🌾 欢迎使用农业商品信息管理系统！")

    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.read()
    st.markdown(readme_content)

    vsidebar.footer()


if __name__ == "__main__":
    page()
