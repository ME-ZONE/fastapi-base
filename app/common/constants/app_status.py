from enum import Enum

from fastapi import status


class AppStatus(Enum):
    ## Custom ##
    # User #
    USER_200_LIST_OK = status.HTTP_200_OK, "OK", "Lấy danh sách tài khoản thành công."
    USER_200_CREATE_OK = status.HTTP_200_OK, "OK", "Tạo tài khoản thành công."

    # Auth #
    AUTH_200_LOGIN_OK = status.HTTP_200_OK, "OK", "Đăng nhập thành công."
    AUTH_400_DECRYPT_DATA_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "Định dạng dữ liệu không hợp lệ.",
    )
    AUTH_400_LOGIN_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "Tên đăng nhập hoặc mật khẩu không chính xác.",
    )
    AUTH_400_TOKEN_INVALID_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "Mã token không hợp lệ.",
    )
    AUTH_400_TOKEN_EXPIRED_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "Mã token đã hết hạn.",
    )
    AUTH_400_USER_INACTIVE_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "Tài khoản chưa được kích hoạt.",
    )

    # OPA #
    OPA_405_METHOD_NOT_ALLOWED = (
        status.HTTP_405_METHOD_NOT_ALLOWED,
        "METHOD_NOT_ALLOWED",
        "Bạn không được phép thực hiện hành động này.",
    )

    # Base Repo #
    BASE_REPO_400_OBJECT_COUNT_MISMATCH_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "Số lượng đối tượng đầu vào không khớp với số lượng bản ghi hiện có.",
    )
    BASE_REPO_400_RELATIONSHIP_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "{relationship_name} không phải là một mối quan hệ hợp lệ.",
    )
    BASE_REPO_400_MODEL_ALREADY_EXISTS_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "{model_name} đã tồn tại.",
    )
    BASE_REPO_404_MODEL_NOT_FOUND = (
        status.HTTP_404_NOT_FOUND,
        "NOT_FOUND",
        "Không tìm thấy {model_name}.",
    )
    BASE_REPO_404_Field_NOT_FOUND = (
        status.HTTP_404_NOT_FOUND,
        "NOT_FOUND",
        "Trường {field_name} không tồn tại ở bảng này và các bảng liên quan.",
    )

    ## Common ##
    COMMON_200_LIST_OK = status.HTTP_200_OK, "OK", "Lấy danh sách {object_name} thành công."
    COMMON_200_READ_OK = status.HTTP_200_OK, "OK", "Lấy {object_name} thành công."
    COMMON_200_CREATE_OK = status.HTTP_200_OK, "OK", "Tạo {object_name} thành công."
    COMMON_200_UPDATE_OK = status.HTTP_200_OK, "OK", "Cập nhật {object_name} thành công."
    COMMON_200_DELETE_OK = status.HTTP_200_OK, "OK", "Xóa {object_name} thành công."

    COMMON_400_MIN_LENGTH_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "Trường {field_name} cần có ít nhất {min} ký tự.",
    )
    COMMON_400_MAX_LENGTH_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "Trường {field_name} chỉ được tối đa {max} ký tự.",
    )
    COMMON_400_MIN_VALUE_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "Giá trị của {field_name} phải lớn hơn hoặc bằng {min}.",
    )
    COMMON_400_MAX_VALUE_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "Giá trị của {field_name} không được vượt quá {max}.",
    )
    COMMON_400_RANGE_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "Giá trị của {field_name} phải nằm trong khoảng từ {min} đến {max}.",
    )

    ## Init ##
    INIT_200_OK = status.HTTP_200_OK, "OK", "Yêu cầu đã được xử lý thành công."
    INIT_400_BAD_REQUEST = (
        status.HTTP_400_BAD_REQUEST,
        "BAD_REQUEST",
        "Yêu cầu không hợp lệ. Vui lòng kiểm tra lại dữ liệu đầu vào và "
        "đảm bảo rằng yêu cầu của bạn tuân theo định dạng đúng.",
    )
    INIT_403_FORBIDDEN = (
        status.HTTP_403_FORBIDDEN,
        "FORBIDDEN",
        "Bạn không có quyền thực hiện hành động này. Nếu bạn tin rằng đây là lỗi, "
        "hãy liên hệ với quản trị viên để được hỗ trợ.",
    )
    INIT_404_NOT_FOUND = (
        status.HTTP_404_NOT_FOUND,
        "NOT_FOUND",
        (
            "Không tìm thấy tài nguyên yêu cầu. Vui lòng đảm "
            "bảo rằng URL hoặc yêu cầu là chính xác và tương "
            "ứng với một tài nguyên hiện có trong hệ thống của "
            "chúng tôi. Nếu bạn tin rằng đây là lỗi, "
            "xin vui lòng liên hệ với đội hỗ trợ của chúng tôi "
            "để được hỗ trợ thêm. Chúng tôi xin lỗi vì bất kỳ "
            "sự bất tiện nào."
        ),
    )
    INIT_405_METHOD_NOT_ALLOWED = (
        status.HTTP_405_METHOD_NOT_ALLOWED,
        "METHOD_NOT_ALLOWED",
        "Bạn không được phép thực hiện hành động này.",
    )
    INIT_429_TOO_MANY_REQUESTS = (
        status.HTTP_429_TOO_MANY_REQUESTS,
        "TOO_MANY_REQUESTS",
        "Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau.",
    )
    INIT_500_INTERNAL_SERVER_ERROR = (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "INTERNAL_SERVER_ERROR",
        "Đã xảy ra lỗi máy chủ nội bộ. Đây là vấn đề từ phía chúng tôi, và chúng tôi đang tích cực "
        "làm việc để giải quyết nó. Chúng tôi xin lỗi vì bất kỳ sự bất tiện nào điều này có thể đã gây ra. "
        "Nếu bạn cần hỗ trợ ngay lập tức hoặc có bất kỳ câu hỏi nào, "
        "xin vui lòng liên hệ với đội hỗ trợ của chúng tôi, "
        "và họ sẽ hỗ trợ bạn giải quyết vấn đề. Cảm ơn bạn đã kiên nhẫn.",
    )

    @property
    def status_code(self) -> int:
        return self.value[0]

    @property
    def name(self) -> str:
        return self.value[1]

    @property
    def message(self) -> str:
        return self.value[2]
