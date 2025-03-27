import allure


class LoginTestCase:
    API_PATH = "/api/auth/login"
    EPIC = "Authentication API"
    FEATURE = "Login Feature"
    STORY = "Login Story"
    SEVERITY = allure.severity_level.CRITICAL
    DESCRIPTION = ("This test case verifies the login functionality by attempting to authenticate"
                   " using various credential sets. The test checks the system's response to both valid"
                   " and invalid login attempts, ensuring proper handling of errors and"
                   " successful authentication for valid credentials.")
    PARAMS = ["test_title", "username", "password", "expected_status", "expected_response"]
    REQUESTS = [
        (
            "Login successful",
            "superuser",
            "superuser",
            200,
            {
                "detail": {
                    "name": "OK",
                    "message": "Đăng nhập thành công.",
                    "data": None,
                    "meta": None,
                }
            },
        ),
        (
            "Login successful",
            "admin123",
            "admin123",
            200,
            {
                "detail": {
                    "name": "OK",
                    "message": "Đăng nhập thành công.",
                    "data": None,
                    "meta": None,
                }
            },
        ),
        (
            "Login failed",
            "invalid_user",
            "wrong_pass",
            400,
            {"detail": {"name": "BAD_REQUEST", "message": "Tên đăng nhập hoặc mật khẩu không chính xác."}},
        ),
    ]
    STEPS = [
        {"step": "📌 Gửi request đăng nhập với username='{username}', password='*****'", "error_message": ""},
        {
            "step": "📌 Kiểm tra response status code",
            "error_message": "❌ Lỗi: Response code mong đợi {expected_status} nhưng nhận {status_code}!",
        },
        {
            "step": "📌 Kiểm tra toàn bộ response JSON",
            "error_message": "❌ Lỗi: Response không khớp!\n{response_json}",
        },
    ]
