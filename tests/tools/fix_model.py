import os
import re


def update_model_file() -> None:
    try:
        # Lấy đường dẫn thư mục chứa script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(script_dir, "ui", "models")

        model_files = [f for f in os.listdir(models_dir) if f.endswith(".py") and f != "__init__.py"]
        model_classes = {}  # Lưu danh sách model để import vào __init__.py

        # Duyệt tất cả file trong app/models/ (trừ __init__.py)
        for file_name in model_files:
            file_path = os.path.join(models_dir, file_name)

            with open(file_path, encoding="utf-8") as f:
                lines = f.readlines()

            # Xóa dòng chứa "managed = False"
            lines = [line for line in lines if "managed = False" not in line]

            # Thay đổi `created_at`, `updated_at` và `DO_NOTHING` -> `CASCADE`
            updated_lines = []
            for line in lines:
                stripped_line = line.strip()
                stripped_line = re.sub(
                    r"created_at = models\.DateTimeField\(\)",
                    "created_at = models.DateTimeField(auto_now_add=True)",
                    line,
                )
                stripped_line = re.sub(
                    r"updated_at = models\.DateTimeField\(\)",
                    "updated_at = models.DateTimeField(auto_now=True)",
                    line,
                )
                stripped_line = re.sub(
                    r"models\.ForeignKey\((.+?),\s*models\.DO_NOTHING\)",
                    r"models.ForeignKey(\1, models.CASCADE)",
                    line,
                )

                # Lưu lại tên class model
                match = re.search(r"class (\w+)\(models.Model\):", stripped_line)
                if match:
                    model_classes[file_name] = model_classes.get(file_name, []) + [match.group(1)]

                updated_lines.append(stripped_line)

            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(updated_lines)

            print(f"✅  Đã cập nhật file: {file_path}")  # noqa: T201

        # Cập nhật __init__.py với các model cụ thể
        init_file = os.path.join(models_dir, "__init__.py")
        with open(init_file, "w", encoding="utf-8") as f:
            imports = [
                f"from .{os.path.splitext(file)[0]} import {', '.join(classes)}"
                for file, classes in model_classes.items()
            ]
            f.write("# ruff: noqa: F401\n")
            f.write("\n".join(imports) + "\n")

        print(f"✅  Đã cập nhật file: {init_file}")  # noqa: T201

    except Exception as e:
        print(f"❌  Lỗi: {e}")  # noqa: T201


if __name__ == "__main__":
    update_model_file()
