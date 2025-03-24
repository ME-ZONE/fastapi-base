from enum import Enum


class ProjectBuildTypes(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    TEST = "TEST"
    PRODUCTION = "PRODUCTION"


class SwaggerPaths(str, Enum):
    RE_DOC = "/api/redoc"
    DOCS = "/api/docs"


class ClassEnum(str, Enum):
    SERVER = "Server"
    PERMISSION = "Permission"
    ENDPOINT = "Endpoint"
    CONTROLLER = "Controller"
    SERVICE = "Service"
    REPOSITORY = "Repository"


class DateFormatEnum(str, Enum):
    DD_MM_YYYY = "%d/%m/%Y"
    HH_MM_SS_DD_MM_YYYY = "%H:%M:%S %d/%m/%Y"
