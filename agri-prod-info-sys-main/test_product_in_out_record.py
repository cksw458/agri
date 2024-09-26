from datetime import datetime
import pandas as pd
import controllers as c
from models import ProductInfo, ProductInOutRecord

df = pd.read_csv("test_product_in_out_record.csv")

# 循环df的所有行
for index, row in df.iterrows():
    pr = ProductInOutRecord(
        product_id=row["product_id"],
        quantity=row["quantity"],
        date=datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S"),
    )
    c.dbsession.add(pr)
    p = c.dbsession.query(ProductInfo).filter(ProductInfo.id == pr.product_id).first()
    p.quantity += pr.quantity
    c.dbsession.commit()
