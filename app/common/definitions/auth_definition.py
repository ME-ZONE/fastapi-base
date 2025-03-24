class AuthEndpointDefinition:
    LOGIN_SUMMARY = "Login cookie"
    LOGIN_DESCRIPTION = (
        "API này cho phép người dùng đăng nhập bằng cách gửi thông tin xác thực hợp lệ."
        "\n\nSau khi đăng nhập thành công, hệ thống sẽ gắn cookie chứa thông tin phiên đăng nhập vào trình duyệt."
    )


class AuthExampleDefinition:
    USERNAME = ["admin", "user", "guest"]
    PASSWORD = ["admin123", "user123", "guest123"]
    ENCRYPTED = ["q1w2e3r4t5y6u7i8", "a1s2d3f4g5h6j7k8", "z1x2c3v4b5n6m7o8"]


class AuthRequestDefinition:
    USERNAME = "Nhập tên đăng nhập tối thiếu 4 ký tự, tối đa 50 ký tự"
    PASSWORD = "Nhập mật khẩu tối thiếu 6 ký tự, tối đa 100 ký tự"  # noqa: S105
    ENCRYPTED = "Nhập dữ liệu đã được mã hóa"
