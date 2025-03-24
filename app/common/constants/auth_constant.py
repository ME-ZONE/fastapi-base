ACCESS_TOKEN_EXPIRES_IN_SECONDS: int = 3600 # 1h
REFRESH_TOKEN_EXPIRES_IN_SECONDS: int = 604800 # 7d
JWT_ALGORITHM: str = "HS256"

AUTH_KEY_MAP_TRANSLATE: dict[str, str] = {
    "username": "tên đăng nhập",
    "password": "mật khẩu"
}
