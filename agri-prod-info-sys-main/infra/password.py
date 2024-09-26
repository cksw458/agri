def create_salt() -> str:
    """生成盐值"""
    import secrets

    return secrets.token_hex(64)  # 生成128字符长度的随机字符串


def hash_password(password: str, salt: str) -> str:
    """哈希密码"""
    import hashlib

    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
