import streamlit as st
import controllers as c
import infra as i
from models import MUser
import views as views
import views.sidebar as vsidebar
import pandas as pd
import infra.data_base as idb
import models


def page():
    i.check_login()

    st.set_page_config(
        page_title="商品出入库",
        page_icon="📦",
    )

    vsidebar.head()
    i.check_admin()

    st.write("## 管理员-商品出入库")
    st.write("### 操作")

    col1, col2 = st.columns(2)

    with col1.popover("入库", use_container_width=True):
        with st.form(key="in", border=False):
            product_name = st.selectbox("商品名称", get_productnames())
            quantity = st.number_input("数量", min_value=1, step=1)
            if st.form_submit_button("确定"):
                pinfo = (
                    c.dbsession.query(models.ProductInfo)
                    .filter_by(name=product_name)
                    .first()
                )
                pr = models.ProductInOutRecord(product_id=pinfo.id, quantity=quantity)
                c.dbsession.add(pr)
                pinfo.quantity += quantity
                try:
                    c.dbsession.commit()
                    st.toast("🎉入库成功")
                except Exception as e:
                    c.dbsession.rollback()
                    st.toast("❌入库失败")

    with col2.popover("出库", use_container_width=True):
        with st.form(key="out", border=False):
            product_name = st.selectbox("商品名称", get_productnames())
            quantity = st.number_input("数量", min_value=1, step=1)
            if st.form_submit_button("确定"):
                pinfo = (
                    c.dbsession.query(models.ProductInfo)
                    .filter_by(name=product_name)
                    .first()
                )
                pr = models.ProductInOutRecord(product_id=pinfo.id, quantity=-quantity)
                if pinfo.quantity < quantity:
                    st.toast("❌库存不足")
                else:
                    c.dbsession.add(pr)
                    pinfo.quantity -= quantity
                    try:
                        c.dbsession.commit()
                        st.toast("🎉出库成功")
                    except Exception as e:
                        c.dbsession.rollback()
                        st.toast("❌出库失败")

    with st.columns(3)[0].popover("撤销最近的一次操作", use_container_width=True):
        if st.button("确定?", type="primary"):
            pr = (
                c.dbsession.query(models.ProductInOutRecord)
                .order_by(models.ProductInOutRecord.id.desc())
                .first()
            )
            if pr is None:
                st.toast("❌无操作可撤销")
            else:
                c.dbsession.delete(pr)
                pinfo = (
                    c.dbsession.query(models.ProductInfo)
                    .filter_by(id=pr.product_id)
                    .first()
                )
                pinfo.quantity -= pr.quantity
                try:
                    c.dbsession.commit()
                    st.toast("🎉撤销成功")
                except Exception as e:
                    c.dbsession.rollback()
                    st.toast("❌撤销失败")

    st.write("### 出入库记录")

    product_in_out_records = (
        c.dbsession.query(models.ProductInOutRecord)
        .order_by(models.ProductInOutRecord.date.desc())
        .limit(100)
        .all()
    )
    if product_in_out_records:
        st.write("*最多显示最近的100条记录*")
        df = pd.DataFrame(
            [
                {
                    "操作": "入库" if pr.quantity > 0 else "出库",
                    "商品名称": (
                        c.dbsession.query(models.ProductInfo)
                        .filter_by(id=pr.product_id)
                        .first()
                        .name
                    ),
                    "单价": (
                        c.dbsession.query(models.ProductInfo)
                        .filter_by(id=pr.product_id)
                        .first()
                        .price
                    ),
                    "数量": abs(pr.quantity),
                    "总价": (
                        c.dbsession.query(models.ProductInfo)
                        .filter_by(id=pr.product_id)
                        .first()
                        .price
                        * abs(pr.quantity)
                    ),
                    "日期": pr.date,
                }
                for pr in product_in_out_records
            ]
        )
        st.dataframe(df)
    else:
        st.write("*暂无记录*")

    vsidebar.footer()


def get_productnames() -> list:
    return [p.name for p in c.dbsession.query(models.ProductInfo).all()]


def on_change():
    pass


if __name__ == "__main__":
    page()
