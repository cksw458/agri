import streamlit as st
import controllers as c
import infra as i
import views as views
import views.sidebar as vsidebar
import models
import pandas as pd
import infra.data_base as idb
import numpy as np


def page():
    i.check_login()

    st.set_page_config(
        page_title="农业商品信息管理",
        page_icon="🌾",
    )

    st.write("## 主页")

    views.after_register_celebrations()
    vsidebar.head()

    st.sidebar.success("🌾 欢迎使用农业商品信息管理系统！")
    st.success("🌾 欢迎使用农业商品信息管理系统！")

    """### 商品展示"""
    pinfos = c.dbsession.query(models.ProductInfo).all()
    for pinfo in pinfos:
        with st.container(border=True):
            st.write(f"#### {pinfo.name}")
            st.write(f"价格：{pinfo.price} 元")
            st.write(f"库存：{pinfo.quantity} 个")
            st.write(f"{pinfo.description}")

    """
    ### 库存统计
    *统计当前库存数量*
    """
    df_inventoryCount = pd.read_sql(
        """
SELECT name, quantity FROM product_info
    """,
        idb.engine,
    )
    st.bar_chart(
        df_inventoryCount,
        x="name",
        y=["quantity"],
        color=["#83c9ff"],
    )
    """
    ### 出入库统计

    *统计最近30天的出入库*
    """
    df_inventoryTransactions = pd.read_sql(
        """
SELECT date as 日期, SUM(IIF(type = '入库', quantity, 0)) as 入库, SUM(IIF(type = '出库', quantity, 0)) as 出库
FROM (
	SELECT DATE(pr.date) as date, IIF(pr.quantity > 0, '入库', '出库') as type, pr.quantity
	FROM product_in_out_record as pr
	LEFT JOIN product_info as p
		on pr.product_id = p.id
    WHERE pr.date >= DATE('now', '-30 day')
)
GROUP BY date
    """,
        idb.engine,
    )

    st.bar_chart(
        df_inventoryTransactions,
        x="日期",
        y=["入库", "出库"],
        color=["#ff2b2b", "#2a81d2"],
    )

    """
    ### 出库趋势
    *统计最近30天的出库趋势*
    """
    dfoutboundTrend = pd.read_sql(
        """
SELECT date as '日期', SUM(quantity) as '数量', name as '产品名'
FROM (
	SELECT DATE(pr.date) as date, pr.quantity, p.name
	FROM product_in_out_record as pr
	LEFT JOIN product_info as p
		on pr.product_id = p.id
    WHERE pr.quantity > 0 and pr.date >= DATE('now', '-30 day')
)
GROUP BY date, name
    """,
        idb.engine,
    )
    st.line_chart(dfoutboundTrend, x="日期", y="数量", color="产品名")

    vsidebar.footer()


if __name__ == "__main__":
    page()
