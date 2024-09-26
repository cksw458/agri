from sqlalchemy import *
import infra.data_base as idb
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from infra.password import create_salt, hash_password

Base = declarative_base()
"""declarative_base()"""

# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@127.0.0.1/old_care?charset=utf8&auth_plugin=mysql_native_password'
# DATABASE_CONNECT_OPTIONS = {}

class MUser(Base):
    """用户"""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_joined = Column(DateTime, default=func.now())
    username = Column(String(length=30), index=True, unique=True)
    salt = Column(String(length=128))
    password = Column(String(length=256))
    is_admin = Column(Boolean, default=False)


class ProductInfo(Base):
    """商品信息"""

    __tablename__ = "product_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=30), index=True, unique=True)
    price = Column(Float)
    quantity = Column(Integer, default=0)
    description = Column(String(length=256))


class ProductInOutRecord(Base):
    """商品出入库记录"""

    __tablename__ = "product_in_out_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("product_info.id"))
    quantity = Column(Integer)
    date = Column(DateTime, default=func.now())


Base.metadata.create_all(idb.engine)

# 创建数据库默认数据
with Session(idb.engine) as session:
    # 创建管理员
    if session.query(MUser).first() is None:
        salt = create_salt()
        session.add(
            MUser(
                username="admin",
                salt=salt,
                password=hash_password("admin", salt),
                is_admin=True,
            )
        )
    session.commit()
    # 创建商品信息
    if session.query(ProductInfo).first() is None:
        session.add(
            ProductInfo(
                name="苹果",
                price=4,
                description="苹果，作为全球广泛种植的温带水果，以其丰富的品种、鲜艳的颜色和独特的风味而备受喜爱。这种水果不仅直接食用时口感脆甜，还能加工成果汁、果酱、苹果派等多样化的食品，为人们的饮食生活增添了无限可能。苹果含有丰富的维生素C、纤维和抗氧化剂，对促进消化健康和增强身体抵抗力具有显著作用。此外，苹果在全球范围内的种植和消费，不仅体现了其经济价值，还因其在不同文化中的象征意义而具有深远的文化影响。无论是作为日常饮食的一部分，还是作为健康生活方式的代表，苹果都是一种不可或缺的水果。",
                quantity=0,
            )
        )
        session.add(
            ProductInfo(
                name="香蕉",
                price=5,
                description="香蕉是一种在全球范围内广受欢迎的热带水果，以其独特的甜味、软糯的质地和易于食用的特性而闻名。这种水果不仅美味，还富含多种营养素，包括维生素、矿物质和膳食纤维，对健康大有裨益。香蕉的高钾含量有助于维持心脏健康和血压稳定，同时它们也是能量的快速来源，尤其适合运动员和需要快速补充能量的人群。此外，香蕉的成熟度不同，其口感和甜度也会有所变化，从青香蕉的淀粉质感到熟香蕉的奶油般柔软，提供了多样化的食用体验。香蕉在世界各地的气候条件下都能生长，是许多国家和地区重要的经济作物，对当地农业和经济发展具有重要意义。无论是作为早餐的一部分、零食，还是用于烹饪和烘焙，香蕉都是一个多功能且美味的选择。",
                quantity=0,
            )
        )
        session.add(
            ProductInfo(
                name="橙子",
                price=6,
                description="""橙子是一种色泽鲜艳、味道酸甜可口的柑橘类水果，它不仅为人们带来味觉上的享受，还提供了丰富的营养价值。橙子含有丰富的维生素C，有助于增强免疫力和促进皮肤健康，同时它所含的膳食纤维有助于消化。此外，橙子还含有多种抗氧化剂，如类黄酮和维生素P，这些成分对预防某些慢性疾病有积极作用。

橙子的皮富含香气，常被用于制作精油，用于香水和食品调味。而橙子本身除了可以直接食用外，也常用于制作果汁、果酱、果冻和其他甜点。橙子的品种繁多，包括甜橙、脐橙、血橙等，每种都有其独特的风味和颜色。

在全球范围内，橙子是重要的经济作物，尤其在地中海地区和美国佛罗里达州等地，橙子的种植和加工产业非常发达。橙子的收获季节通常在冬季，这使得它成为冬季市场上的常见水果。无论是作为健康饮食的一部分，还是作为烹饪和烘焙的原料，橙子都是一种受欢迎且多用途的水果。""",
                quantity=0,
            )
        )
        session.add(
            ProductInfo(
                name="猕猴桃",
                price=7,
                description="猕猴桃，这种外表毛茸茸、内里翠绿多汁的水果，以其酸甜口感和丰富的营养价值备受青睐。作为维生素C的超级来源，它能有效增强免疫力并促进皮肤健康，同时含有丰富的维生素E、维生素K、钾和膳食纤维，对心血管健康和消化系统都有积极影响。猕猴桃的柔软质地使其成为直接食用或用于制作果汁、果酱和甜点的理想选择。品种多样，从常见的绿色果肉到较为稀有的黄色果肉，猕猴桃不仅是健康饮食的优选，也是烹饪创新的有趣食材。在全球市场上，尤其是新西兰生产的猕猴桃，以其“奇异果”之名享誉世界，成为健康和活力的象征。",
                quantity=0,
            )
        )
        session.add(
            ProductInfo(
                name="火龙果",
                price=8,
                description="火龙果，这种外观独特、色彩鲜艳的热带水果，以其白色或红色果肉和遍布的黑色种子而备受欢迎。它不仅味道温和、甜而不腻，而且营养价值丰富，含有维生素C、膳食纤维以及钾和镁等矿物质，对促进消化健康和增强身体抗氧化能力有显著益处。火龙果的清新口感使其成为水果沙拉、果汁和冰沙的理想选择，同时，它的红色品种更因其甜美的风味而受到偏爱。作为一种健康且多用途的食材，火龙果在全球市场上越来越受到消费者的喜爱，其独特的食用体验和文化意义也为其增添了几分魅力。",
                quantity=0,
            )
        )
        session.commit()
