from uu import Error
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
import config as conf


engine = create_engine(conf.DATABASE_URL)
"""数据库引擎"""

DBSession = scoped_session(sessionmaker(bind=engine))
"""数据库会话工厂"""
