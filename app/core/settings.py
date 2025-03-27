from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.common.enums import ProjectBuildTypes


class BaseAppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None, env_file_encoding="utf-8")
    project_build_type: ProjectBuildTypes = Field(default=ProjectBuildTypes.DEVELOPMENT)

    @property
    def env_file(self) -> str:
        env_prefix = (
            self.project_build_type.value[:3].lower()
            if self.project_build_type == ProjectBuildTypes.DEVELOPMENT
            else self.project_build_type.value[:4].lower()
        )
        return f".env.{env_prefix}"


class AppSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_file=BaseAppSettings().env_file, env_file_encoding="utf-8")

    #### Compose ####
    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin"  # noqa: S105
    POSTGRES_DB: str = "postgres"
    PGDATA: str = "/data/postgres"
    TZ: str = "Asia/Ho_Chi_Minh"

    @property
    def POSTGRES_ASYNC_URL(self) -> str:  # noqa: N802
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def POSTGRES_URL(self) -> str:  # noqa: N802
        return self.POSTGRES_ASYNC_URL.replace("postgresql+asyncpg://", "postgresql://")

    # PGAdmin
    PGADMIN_DEFAULT_EMAIL: str = "admin@admin.com"
    PGADMIN_DEFAULT_PASSWORD: str = "admin"  # noqa: S105

    #### App ####
    # Project
    PROJECT_NAME: str = "FastAPI Management System"
    PROJECT_DESCRIPTION: str = """Powered by Tensor 🚀"""
    VERSION: str = "0.1-SNAPSHOT"
    DEBUG: bool = False
    PROJECT_BUILD_TYPE: ProjectBuildTypes = ProjectBuildTypes.DEVELOPMENT
    ALLOW_ORIGINS: list[str] = []

    # SQLAlchemy
    SQLALCHEMY_DEBUG: bool = False
    POOL_SIZE: int = 100
    MAX_OVERFLOW: int = 100
    POOL_TIMEOUT: int = 100

    # Crypto
    CRYPTO_SECRET: str = "MK0m16elYbO8GEILxzhXW84ioZx_9ULdolcMXaYQEwg="  # noqa: S105

    # JWT
    JWT_SECRET: str = "jBV17jpzB2ryGF5a_HjyZnXOrZvt0pTBA3ubLnsOvfU"  # noqa: S105

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # OPA
    OPA_HOST: str = "localhost"
    OPA_PORT: int = 8181

    # Test
    TEST_POSTGRES_HOST: str = "localhost"
    TEST_POSTGRES_PORT: int = 5499
    TEST_ALLURE_PORT: int = 5252

settings = AppSettings()
