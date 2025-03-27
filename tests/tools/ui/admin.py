from typing import Any

from django.forms import ModelForm
from django.http import HttpRequest


def register_admin_models() -> None:
    from django.apps import apps
    from django.contrib import admin
    from import_export.admin import ImportExportModelAdmin
    from import_export.resources import ModelResource

    from app.utils import hash_data


    for model in apps.get_models():
        if model._meta.app_label == "ui" and not admin.site.is_registered(model):
            # Tạo một ModelAdmin tùy chỉnh
            class CustomModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
                # Tạo một ModelResource cho import/export
                resource_class = type(
                    f"{model.__name__}Resource",
                    (ModelResource,),
                    {
                        "Meta": type("Meta", (), {"model": model}),
                    },
                )

                def _create_log_entry(self, *args, **kwargs) -> None:
                    pass

                resource_class = resource_class
                exclude = ["created_at", "updated_at"]
                readonly_fields = ["created_at", "updated_at"]
                # Lấy danh sách tất cả các trường hợp lệ (không phải ManyToManyField và ForeignKey)
                fields = [
                    field.name
                    for field in model._meta.get_fields()
                    if not field.auto_created
                ]

                list_display = (
                    fields[:5] if fields else ["__str__"]
                )  # Nếu không có trường hợp hợp lệ, dùng __str__

                def save_model(self, request: HttpRequest, obj: Any, form: ModelForm, change: bool) -> None:
                    if hasattr(obj, "hashed_password") and "hashed_password" in form.changed_data:
                        obj.hashed_password = hash_data(obj.hashed_password)
                    super().save_model(request, obj, form, change)

            # Đăng ký model với ModelAdmin tùy chỉnh
            admin.site.register(model, CustomModelAdmin)
