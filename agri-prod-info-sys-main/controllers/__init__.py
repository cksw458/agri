import atexit
from uu import Error
from models import MUser
from infra.data_base import DBSession
from infra.password import create_salt, hash_password

dbsession = DBSession()
"""数据库会话"""

atexit.register(dbsession.close)  # 程序结束时关闭数据库会话


class CError(Error):
    """控制器异常"""

    pass


class CUser:
    """用户"""

    def __init__(self, user: MUser):
        self._user = user

    def get_usernames(self):
        """获取用户名"""
        return self._user.username

    def set_usernames(self, username: str):
        """设置用户名"""
        self._user.username = username
        try:
            dbsession.commit()
        except Exception:
            dbsession.rollback()
            raise CError("用户名已存在！")

    def set_password(self, old_password: str, new_password: str):
        """更新密码"""
        if self._user.password != hash_password(old_password, self._user.salt):
            raise CError("原密码错误！")
        self._user.salt = create_salt()
        self._user.password = hash_password(new_password, self._user.salt)
        try:
            dbsession.commit()
        except Exception:
            dbsession.rollback()
            raise CError("密码更新失败！")

    def get_register_time(self):
        """获取注册时间"""
        return self._user.date_joined
    
    def is_admin(self):
        """是否管理员"""
        return self._user.is_admin

    _user: MUser


class CSession:
    """会话"""

    def __init__(self):
        user_id = self._session_state_get_user_id()
        if user_id is not None:
            muser = dbsession.query(MUser).filter(MUser.id == user_id).first()
            if muser is not None:
                self.user = CUser(muser)

    def is_login(self) -> bool:
        """是否登录"""
        return self.user is not None

    def login(self, username: str, password: str):
        """登录"""
        user = dbsession.query(MUser).filter(MUser.username == username).first()

        if username == "":
            raise CError("用户名不能为空！")
        if password == "":
            raise CError("密码不能为空！")
        if user is None:
            raise CError("用户名不存在！")
        else:
            if user.password != hash_password(password, user.salt):
                raise CError("密码错误！")

        self._session_state_set_user_id(user.id)
        self.user = CUser(user)

    def logout(self):
        """登出"""
        self._session_state_set_user_id(None)
        self.user = None

    def register(self, username: str, password: str):
        """注册"""
        if username == "" or password == "":
            raise CError("用户名或密码不能为空！")
        if (
            dbsession.query(MUser).filter(MUser.username == username).first()
            is not None
        ):
            raise CError("用户名已存在！")

        user = MUser()
        user.username = username
        user.salt = create_salt()
        user.password = hash_password(password, user.salt)

        dbsession.add(user)
        dbsession.commit()

    def _session_state_get_user_id(self) -> int:
        import streamlit as st
        import infra.st_session_str as sss

        if sss.user_id not in st.session_state:
            return None
        return st.session_state[sss.user_id]

    def _session_state_set_user_id(self, user_id: int):
        import streamlit as st
        import infra.st_session_str as sss

        if user_id is None:
            if sss.user_id in st.session_state:
                st.session_state.pop(sss.user_id)
        else:
            st.session_state[sss.user_id] = user_id

    user: CUser = None


# --------------------------------------------------------------------------------------


session = CSession()
"""会话"""


def user() -> CUser:
    """获取用户"""
    return session.user
