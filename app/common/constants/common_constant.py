from pathlib import Path

BasePath: str = "/api"
APP_DIR_PATH = str(Path(__file__).resolve().parents[3])
LOG_DIR_PATH: str = f"{APP_DIR_PATH}/deployments/data/logs"

COMMON_RESPONSES: dict = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "name": "BAD_REQUEST",
                        "message": "Yêu cầu không hợp lệ. Vui lòng kiểm tra lại dữ liệu đầu vào và "
                                   "đảm bảo rằng yêu cầu của bạn tuân theo định dạng đúng."
                    }
                }
            }
        },
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "name": "INTERNAL_SERVER_ERROR",
                        "message": "Đã xảy ra lỗi máy chủ. Vui lòng thử lại sau."
                    }
                }
            }
        },
    },
}

PAGINATE_KEY_MAP_TRANSLATE: dict[str, str] = {
    "offset": "Số lượng bỏ qua",
    "limit": "Số lượng giới hạn",
}

MODEL_KEY_MAP_TRANSLATE: dict[str, str] = {
    "User": "tài khoản"
}

