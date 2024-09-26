import streamlit as st
import controllers as c
import infra as i
from models import MUser
import views as views
import views.sidebar as vsidebar
import pandas as pd
import infra.data_base as idb


def page():
    i.check_login()

    st.set_page_config(
        page_title="商品信息管理",
        page_icon="🛍️",
    )

    vsidebar.head()
    i.check_admin()

    st.write("## 管理员-商品信息管理")
    st.write("### 商品信息编辑")

    df = pd.read_sql("SELECT * from product_info", idb.engine)
    # edit_df = st.data_editor(df, on_change=on_change, num_rows="dynamic")
    edit_df = st.data_editor(df, num_rows="dynamic")

    if st.button("保存"):
        edit_df.to_sql("product_info", idb.engine, if_exists="replace", index=False)

    vsidebar.footer()


def on_change():
    pass


if __name__ == "__main__":
    page()
