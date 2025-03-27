from django.apps import AppConfig

from .admin import register_admin_models


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ui"

    def ready(self) -> None:
        register_admin_models()
