from app.common.enums import GenderEnum, RoleEnum
from app.utils import convert_enum_to_list


class UserEndpointDefinition:
    LIST_SUMMARY = "List user"
    LIST_DESCRIPTION = (
        "API này cho phép lấy danh sách các người dùng đã đăng ký trong hệ thống.\n\n"
        "Kết quả trả về bao gồm thông tin tóm tắt của từng người dùng, chẳng hạn như tên, email, "
        "và trạng thái hoạt động, giúp quản trị viên hoặc người dùng có thể duyệt qua danh sách một cách nhanh chóng."
    )

    CREATE_SUMMARY = "Create user"
    CREATE_DESCRIPTION = (
        "API này cho phép người dùng tạo tài khoản mới bằng cách cung cấp thông tin hợp lệ."
        "\n\nSau khi tạo tài khoản thành công, hệ thống có thể yêu cầu xác minh "
        "hoặc cung cấp thông tin bổ sung tùy theo cấu hình."
    )


class UserExampleDefinition:
    USERNAME = ["admin", "user", "guest"]
    PASSWORD = ["admin123", "user123", "guest123"]
    ROLE = convert_enum_to_list(enum=RoleEnum)

    FULL_NAME = [
        "Nguyễn Thanh Minh",
        "Trần Quốc Anh",
        "Lê Khánh Bình",
        "Hoàng Nhật Duy",
        "Phạm Đình Trang",
        "Vũ Thế Nam",
        "Bùi Gia Hạnh",
        "Hồ Tuấn Quang",
        "Đặng Bảo Lan",
        "Ngô Công Phương",
    ]
    GENDER = convert_enum_to_list(enum=GenderEnum)


class UserRequestDefinition:
    USERNAME = "Nhập tên đăng nhập"
    PASSWORD = "Nhập mật khẩu"  # noqa: S105
    ROLE = "Nhập vai trò"

    FULL_NAME = "Nhập họ và tên"
    GENDER = "Nhập giới tính"
